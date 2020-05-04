from .visitor import Visited, Dag
import abc
import typing as tp

#I should possibly have Dag is a kind of Node. I am basically recreating coreir
#Passes will be run on this
class DagNode(Visited):
    def __init__(self, *children):
        self.set_children(*children)

    def set_children(self, *children):
        assert len(children) == self.num_inputs(), f"{len(children)} != {self.num_inputs()}"
        self._children = children

    def children(self):
        yield from self._children

    def inputs(self):
        return self._children

    @classmethod
    def num_inputs(cls):
        return len(cls.input_names())

    @classmethod
    def num_outputs(cls):
        return len(cls.output_names())

    @classmethod
    @abc.abstractmethod
    def input_names(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def output_names(cls):
        pass

    @abc.abstractmethod
    def copy(self):
        pass

#A container for all the kinds of nodes (DagNodes, peakNodes, and modules)
#Each container has a particular name (CoreIR, Lassen, etc...) and has an associated unique DagNode Class <class CoreIR(DagNode): pass>
class Nodes:
    _cache = {}
    def __new__(cls, name):
        if not name in cls._cache:
            self = super().__new__(cls)
            self.__init__(name)
            cls._cache[name] = self
        return cls._cache[name]

    def __init__(self, name):
        self.name = name
        self.dag_node_cls = type(name, (DagNode,), {})
        self._node_names = set()
        self.dag_nodes = {}
        self.peak_nodes = {}
        self.coreir_modules = {}
        self.coreir_names = {}

    #returns Node name from coreir module name
    def get_from_coreir(self, cmod) -> str:
        raise NotImplementedError("need coreir module name")

    #returns Node name from coreir module name
    def get_from_peak(self, peak_fc) -> str:
        raise NotImplementedError("need coreir module name")

    #Adds all 3 kinds of nodes under one name
    def add(self, node_name, dag_node, peak_node, mod):
        if node_name in self._node_names:
            raise ValueError(f"{node_name} already exists")
        self.dag_nodes[node_name] = dag_node
        self.peak_nodes[node_name] = peak_node
        self.coreir_modules[node_name] = mod
        self._node_names.add(node_name)

    def create_dag_node(self, node_name, inputs, outputs, attrs: tp.List = []):
        node_cls = self.dag_node_cls
        assert isinstance(inputs, list)
        assert isinstance(outputs, list)
        assert len(outputs) <=1, "NYI"

        def __init__(self, *args, **kwargs):
            self.set_children(*args)
            self.set_kwargs(**kwargs)

        def set_kwargs(self, **kwargs):
            assert len(kwargs) == len(attrs), f"{kwargs} != {attrs}"
            assert all(attr in kwargs for attr in attrs)
            for attr in attrs:
                setattr(self, attr, kwargs[attr])

        def copy(self):
            args = self.children()
            kwargs = {attr:getattr(self, attr) for attr in attrs}
            return type(self)(*args, **kwargs)

        @classmethod
        def input_names(cls):
            return inputs

        @classmethod
        def output_names(cls):
            return outputs

        node = type(node_name, (node_cls,), dict(
            _attrs_=attrs,
            __init__=__init__,
            set_kwargs=set_kwargs,
            copy=copy,
            input_names=input_names,
            output_names=output_names,
        ))
        return node

#Defining a few common DagNodes
CommonNodes = Nodes("Common")
Input = CommonNodes.create_dag_node("Input", [], [0], ("idx",))
#Output = CommonNodes.create_dag_node("Output", [0], [])
Select = CommonNodes.create_dag_node("Select", [0], [0], ("sel_idx",))
Constant = CommonNodes.create_dag_node("Constant", [], [0], ("value",))
