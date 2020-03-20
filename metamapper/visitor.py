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
        self._dag_cache = set()
        for output in dag.parents():
            self.visit(output)

    def visit(self, data_obj):
        if data_obj in self._dag_cache:
            return
        visited = False
        for kind_str in data_obj.kind():
            visit_name = f"visit_{kind_str}"
            if hasattr(self, visit_name):
                getattr(self, visit_name)(data_obj)
                visited = True
                break
        if not visited:
            self.generic_visit(data_obj)
        self._dag_cache.add(data_obj)

    def generic_visit(self, data_obj):
        #Do nothing for current node
        for child in data_obj.children():
            self.visit(child)


#Semantics are if you return None, then do not change anything
#If you return something then replace current node with that thing
class Transformer(metaclass=VisitorMeta):
    def __init__(self, dag: Dag):
        self._dag_cache = {}
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

