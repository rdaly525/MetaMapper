class Visited(object):

    #Defaults to the class name
    def kind(self) -> str:
        return [type(self).__name__]

    def children(self):
        raise NotImplemented()


class Dag:
    def __init__(self, outputs, inputs):
        self.inputs = inputs
        self.outputs = outputs
        self._parents = outputs

    def outputs(self):
        return self._parents

    def parents(self):
        yield from self._parents

    @property
    def num_outputs(self):
        return self.num_parents

    @property
    def num_inputs(self):
        return len(self.inputs)

    @property
    def num_parents(self):
        return len(self._parents)


class VisitorMeta(type):
    def __new__(self, name, bases, dct):
        if bases and "visit" in dct:
            raise SyntaxError("Cannot override visit")
        return type.__new__(self, name, bases, dct)


class Visitor(metaclass=VisitorMeta):
    def __init__(self, dag: Dag):
        assert isinstance(dag, Dag)
        self._dag_cache = set()
        for output in dag.parents():
            self.visit(output)

    def visit(self, node: Visited):
        assert isinstance(node, Visited)
        if node in self._dag_cache:
            return
        visited = False
        for kind_str in node.kind():
            visit_name = f"visit_{kind_str}"
            if hasattr(self, visit_name):
                getattr(self, visit_name)(node)
                visited = True
                break
        if not visited:
            self.generic_visit(node)
        self._dag_cache.add(node)

    def generic_visit(self, node):
        #Do nothing for current node
        for child in node.children():
            self.visit(child)


#Semantics are if you return None, then do not change anything
#If you return something then replace current node with that thing
#TODO Does replacing even work if you are replacing a Node that has multiple parents??
class Transformer(metaclass=VisitorMeta):
    def __init__(self, dag: Dag):
        assert isinstance(dag, Dag)
        self._dag_cache = {}
        self._dag = {}
        for output in dag.parents():
            self.generic_visit(output)

    def visit(self, node):
        if node in self._dag_cache:
            return self._dag_cache[node]
        visited = False
        for kind_str in node.kind():
            visit_name = f"visit_{kind_str}"
            if hasattr(self, visit_name):
                ret = getattr(self, visit_name)(node)
                visited = True
                break
        if not visited:
            ret = self.generic_visit(node)
        if ret is None:
            ret = node
        self._dag_cache[node] = ret
        #TODO inputs and outputs should be replaced appropriately ??
        return ret

    def generic_visit(self, node):
        #Modify the current node with the new children
        new_children = []
        for child in node.children():
            new_child = self.visit(child)
            assert new_child is not None
            new_children.append(new_child)
        node.set_children(*new_children)
        return node

