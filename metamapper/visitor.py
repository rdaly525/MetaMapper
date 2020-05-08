import typing as tp

class Visited(object):

    #Defaults to the class name
    def kind(self) -> str:
        return [cls.__name__ for cls in type(self).mro()][:-1]

    def children(self):
        raise NotImplemented()

class AbstractDag:
    def __init__(self, *parents):
        self._parents = parents

    def parents(self):
        yield from self._parents

class VisitorMeta(type):
    def __new__(self, name, bases, dct):
        if bases and ("visit" in dct or "run" in dct):
            raise ValueError("Cannot override visit")
        return type.__new__(self, name, bases, dct)

class Visitor(metaclass=VisitorMeta):
    def run(self, dag: AbstractDag):
        assert isinstance(dag, AbstractDag), f"{dag}"
        self._dag_cache = set()
        for parent in dag.parents():
            assert parent is not None
            self.visit(parent)
        #For chaining
        return self

    def visit(self, node: Visited):
        assert node is not None
        assert isinstance(node, Visited), f"{node}"
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
        assert node is not None
        #Do nothing for current node
        for child in node.children():
            self.visit(child)


#Semantics are if you return None, then do not change anything
#If you return something then replace current node with that thing
#TODO Does replacing even work if you are replacing a Node that has multiple parents??
class Transformer(metaclass=VisitorMeta):
    def run(self, dag: AbstractDag):
        assert isinstance(dag, AbstractDag)
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

