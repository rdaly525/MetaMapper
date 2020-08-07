from functools import lru_cache

from DagVisitor import Visited, AbstractDag
import abc
import typing as tp
import coreir

from hwtypes.modifiers import is_modified
from hwtypes.adt import Product, Tuple, Sum, TaggedUnion
from . import CoreIRContext


#Passes will be run on this
class DagNode(Visited):
    def __init__(self, *args, **kwargs):
        if "type" in kwargs:
            assert not is_modified(kwargs["type"])
        self.set_kwargs(**kwargs)
        self.set_children(*args)
        self._selects = set()

    def set_children(self, *children):
        expected_children = self.num_children
        if expected_children >=0 and len(children) != expected_children:
            raise ValueError(f"len({children}) != {expected_children} for {self}")
        for i, child in enumerate(children):
            if not isinstance(child, DagNode):
                raise ValueError(f"The {i}th child {child} is not a DagNode")
        self._children = children

    def set_kwargs(self, **kwargs):
        if "iname" not in kwargs:
            kwargs.update({"iname": f"i{id(self)}"})

        assert len(kwargs) == len(self.attributes), f"{kwargs} != {self.attributes}"
        assert all(attr in kwargs for attr in self.attributes), f"{kwargs} != {self.attributes}"
        for attr in self.attributes:
            setattr(self, attr, kwargs[attr])

    def children(self):
        return self._children

    @property
    @abc.abstractmethod
    def attributes(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def num_children(self):
        raise NotImplementedError()

    @lru_cache(None)
    def select(self, field):
        self._selects.add(field)
        return Select(self, field=field)

    def copy(self):
        args = self.children()
        kwargs = {attr:getattr(self, attr) for attr in self.attributes}
        return type(self)(*args, **kwargs)


#This holds a single RTL dag. The first source/sink pair represents the interface whereas the rest represent instances with state
class Dag(AbstractDag):
    def __init__(self, sources: tp.List[Visited], sinks: tp.List[Visited]):
        if len(sources) != len(sinks):
            raise ValueError("each output must have a matching input")
        if not all(isinstance(source, Source) for source in sources):
            raise ValueError("Each source needs to be instance of Source")
        if not all(isinstance(sink, Sink) for sink in sinks):
            raise ValueError("Each source needs to be instance of Source")
        if len(sources) < 1 or not isinstance(sources[0], Input):
            raise ValueError("First Source needs to be an Input")
        if not isinstance(sinks[0], Output):
            raise ValueError("First Sink needs to be an Output")

        self.sources = sources
        self.sinks = sinks
        super().__init__(*sinks)
        #self.outputs = sinks[0]
        #self.input = srcs[0]

    @property
    def input(self):
        return self.sources[0]

    @property
    def output(self):
        return self.sinks[0]


#A container for all the kinds of nodes (DagNodes, peakNodes, and modules)
#Each container has a particular name (CoreIR, Lassen, etc...) and has an associated unique DagNode Class <class CoreIR(DagNode): pass>
class Nodes:
    _cache = {}
    def __new__(cls, name):
        c = CoreIRContext()
        cls._cache.setdefault(c, {})
        if not name in cls._cache[c]:
            self = super().__new__(cls)
            self.__init__(name)
            cls._cache[c][name] = self
        return cls._cache[c][name]

    def __init__(self, name):
        self.name = name
        self._node_names = set()

        #if node is stateful, it points to a tuple(Source, Sink)
        self.dag_nodes = {}
        self.peak_nodes = {}
        self.coreir_modules: tp.Mapping[str, coreir.Module] = {}

    def __str__(self):
        return f"Nodes<{self.name}>"

    def is_stateful(self, node_name):
        return node_name in self.dag_nodes and isinstance(self.dag_nodes[node_name], tuple)

    #returns Node name from coreir module name
    def name_from_coreir(self, cmod) -> str:
        names = [k for k,v in self.coreir_modules.items() if v == cmod]
        assert len(names) <2
        if len(names) == 1:
            return names[0]
        return None

    #returns Node name from coreir module name or None if not found
    def name_from_peak(self, peak_fc) -> str:
        names = [k for k,v in self.peak_nodes.items() if v is peak_fc]
        assert len(names) <2
        if len(names) == 1:
            return names[0]
        return None

    #Adds all 3 kinds of nodes under one name
    def add(self, node_name: str, peak_node, cmod: coreir.Module, dag_nodes):
        if cmod is not None:
            assert isinstance(cmod, coreir.Module)
        if node_name in self._node_names:
            raise ValueError(f"{node_name} already exists")
        if isinstance(dag_nodes, DagNode):
            #This cannot be stateful
            if isinstance(dag_nodes, State):
                raise ValueError("State nodes need to come in pairs")
        elif isinstance(dag_nodes, tuple):
            assert len(dag_nodes) == 2
            if not isinstance(dag_nodes[0], Source):
                raise ValueError("Needs to be source")
            if not isinstance(dag_nodes[1], Sink):
                raise ValueError("Needs to be source")
        self.dag_nodes[node_name] = dag_nodes
        self.peak_nodes[node_name] = peak_node
        self.coreir_modules[node_name] = cmod
        self._node_names.add(node_name)

    # TODO Thoughts
    #If this is state, then it creates two nodes a source and sink
    def create_dag_node(self, node_name, num_children, stateful: bool, attrs: tp.List = (), parents=()) -> DagNode:
        if stateful:
            raise NotImplementedError("TODO")

        if "iname" in attrs:
            raise ValueError("Cannot have 'iname' in attrs")

        attrs += ("iname",)
        node = type(node_name, parents + (DagNode,), dict(
            num_children=num_children,
            nodes=self,
            node_name=node_name,
            attributes=attrs,
        ))
        return node

#Select gotes 1 ->1
#Input goes 0 -> 1
#Output goes N->0

Common = Nodes("Common")
Select = Common.create_dag_node("Select", 1, False, ("field",))

from hwtypes import AbstractBitVector, AbstractBit
from peak.mapper.utils import rebind_type
from peak.assembler import AssembledADT, Assembler
from peak.mapper import Unbound
from metamapper.family import fam
class ConstAssemble:
    def assemble(self, family):
        if family is fam().SMTFamily():
            T = rebind_type(self.type, family)
        else:
            T = self.type
        aadt = AssembledADT[T, Assembler, family.BitVector]
        if self.value is Unbound:
            value = 0
        else:
            value = self.value

        if issubclass(aadt, (AbstractBit, AbstractBitVector)):
            val = aadt(value)
        else:
            val = aadt(family.BitVector[aadt._assembler_.width](value))
        return val

Constant = Common.create_dag_node("Constant", 0, False, ("value", "type"), (ConstAssemble,))



class State(object): pass
class Source(State): pass
class Sink(State): pass
Input = Common.create_dag_node("Input", 0, False, ("type",), (Source,))
Output = Common.create_dag_node("Output", -1, False, ("type",), (Sink,))

Input.sink_t = Output
Output.source_t = Input

#This node represents kind of a like a passthrough node in CoreIR.
#The inputs of this node are specified using the selects tuple
#selects = (path0, path1, ..., pathn)
class Bind(DagNode):
    def __init__(self, *children, iname, type, paths):
        super().__init__(*children, paths=paths, type=type, iname=iname,)

    @property
    def num_children(self):
        return len(self.paths)

    @property
    def attributes(self):
        return ("paths", "type", "iname")

    nodes = Common

#This node represents a way to construct generic types from its fields
#The inputs of this node are specified using the selects tuple
#selects = (path0, path1, ..., pathn)
class Combine(DagNode):
    def __init__(self, *children, iname, type, tu_field=None):
        super().__init__(*children, type=type, iname=iname,)
        if issubclass(type, (Sum, TaggedUnion)):
            if tu_field is None:
                raise ValueError("Combine Tagged union must have a field")
            if tu_field not in type.field_dict:
                raise ValueError(f"{tu_field} not in {type}")
            self.tu_field = tu_field

    @property
    def num_children(self):
        if issubclass(self.type, (Product, Tuple)):
            return len(self.type.field_dict)
        elif issubclass(self.type, (Sum, TaggedUnion)):
            return 1

    @property
    def attributes(self):
        return ("type", "iname")

    nodes = Common
