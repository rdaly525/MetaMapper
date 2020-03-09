class Visited(object):

    #Defaults to the class name
    def kind(self) -> str:
        return [type(self).__name__]

    def children(self):
        raise NotImplemented()

class Dag:
    def __init__(self, parents):
        self._parents = parents

    def parents(self):
        return self._parents

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
