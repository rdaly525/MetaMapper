from functools import lru_cache

from DagVisitor import Visited, AbstractDag
import abc
import typing as tp
import coreir

from hwtypes.modifiers import is_modified
from hwtypes.adt import Product, Tuple, Sum, TaggedUnion
import hwtypes as ht
from . import CoreIRContext

unique_name = 0

#Passes will be run on this
class DagNode(Visited):
    def __init__(self, *args, **kwargs):
        if "type" in kwargs:
            t = kwargs['type']
            if t is None:
                raise ValueError("Need to specify a type")
            if is_modified(kwargs['type']):
                raise ValueError(f"{self}, {kwargs['type']} cannot be modified")
        elif "type" in self.static_attributes and is_modified(self.static_attributes["type"]):
            raise ValueError(f"{self} {self.static_attributes['type']}")
        self.set_kwargs(**kwargs)
        self.set_children(*args)
        self._selects = set()

    def __str__(self):
        return f"{type(self).__name__}"

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
            global unique_name
            kwargs.update({"iname": f"i{unique_name}"})
            unique_name += 1
        if "type" in self.static_attributes and "type" in kwargs:
            kt =  kwargs["type"]
            sat = self.static_attributes["type"]
            #assert kt == sat
            del kwargs["type"]
        assert len(kwargs) == len(self.attributes), f"{kwargs} != {self.attributes}"
        assert all(attr in kwargs for attr in self.attributes), f"{kwargs} != {self.attributes}"
        for attr in self.attributes:
            assert isinstance(attr, str)
            setattr(self, attr, kwargs[attr])
        for attr, val in self.static_attributes.items():
            setattr(self, attr, val)

    def add_metadata(self, md):
        self._metadata_ = md

    def children(self):
        return self._children

    @property
    def child(self):
        if len(self.children()) != 1:
            raise ValueError("Cannot select singular child")
        return list(self.children())[0]

    @property
    @abc.abstractmethod
    def attributes(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def num_children(self):
        raise NotImplementedError()

    @lru_cache(None)
    def select(self, field, original=None):
        # This is a hack for selecting one bit
        if isinstance(field, int):
            if self.type[field] == ht.BitVector[16]:
                return Select(self, field=field, type=self.type[field])
            return Select(self, field=field, type=ht.Bit)
        key_list = {f"O{i}": k for i, k in enumerate(self.type.field_dict.keys())}
        new_field = key_list.get(field)
        if original is None and new_field is not None:
            field = new_field
        self._selects.add(field)
        if original is None:
            original = field
        if original not in self.type.field_dict:
            raise ValueError(f"{original} not in {list(self.type.field_dict.items())}")
        return Select(self, field=field, type=self.type.field_dict[original])


    def copy(self):
        args = self.children()
        kwargs = {attr:getattr(self, attr) for attr in self.attributes}
        node = type(self)(*args, **kwargs)
        if hasattr(self, "_metadata_"):
            node.add_metadata(self._metadata_)
        return node


#This holds a single RTL dag. The first source/sink pair represents the interface whereas the rest represent instances with state
class Dag(AbstractDag):
    def __init__(self, sources: tp.List[Visited], sinks: tp.List[Visited]):
        if len(sources) != len(sinks):
            raise ValueError("each output must have a matching input")
        if not all(isinstance(source, Source) for source in sources):
            raise ValueError("Each source needs to be instance of Source")
        if not all(isinstance(sink, Sink) for sink in sinks):
            raise ValueError("Each sink needs to be instance of Sink")
        if len(sources) < 1 or not isinstance(sources[0], Input):
            raise ValueError("First Source needs to be an Input")
        if not isinstance(sinks[0], Output):
            raise ValueError("First Sink needs to be an Output")
        for source, sink in list(zip(sources, sinks))[1:]:
            assert type(source).sink_t is type(sink)
            assert type(sink).source_t is type(source)
        for source, sink in zip(sources, sinks):
            source.set_sink(sink)
            sink.set_source(source)


        self.sources = sources
        self.sinks = sinks
        super().__init__(*sinks)

    @property
    def input(self):
        return self.sources[0]

    @property
    def output(self):
        return self.sinks[0]

#Allows arbitrary number of inputs and outputs
class IODag(AbstractDag):
    def __init__(self, inputs, outputs, sources: tp.List[Visited] = [], sinks: tp.List[Visited] = []):
        for source, sink in zip(sources, sinks):
            source.set_sink(sink)
            sink.set_source(source)

        self.non_input_sources = sources
        self.non_output_sinks = sinks
        self.inputs = inputs
        self.outputs = outputs
        self.sources = [*inputs, *sources]
        self.sinks = [*outputs, *sinks]
        super().__init__(*self.sinks)
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
        self.custom_nodes = []
        self.custom_inline = {}
        self.coreir_modules: tp.Mapping[str, coreir.Module] = {}

    def __str__(self):
        return f"Nodes<{self.name}>"

    def is_stateful(self, node_name):
        return node_name in self.dag_nodes and isinstance(self.dag_nodes[node_name], tuple)

    #returns Node name from coreir module name
    def name_from_coreir(self, cmod) -> str:
        if f"{cmod.namespace.name}.{cmod.name}" in self.custom_nodes and f"{cmod.namespace.name}.{cmod.name}" in self.dag_nodes:
            return f"{cmod.namespace.name}.{cmod.name}"
        names = [k for k,v in self.coreir_modules.items() if v == cmod]
        if len(names) > 0:
            return names[0]
        if f"{cmod.namespace.name}.{cmod.name}" in self.coreir_modules:
            return f"{cmod.namespace.name}.{cmod.name}"
        return None


    #returns Node name from coreir module name or None if not found
    def name_from_peak(self, peak_fc, name = None) -> str:
        if name in self.custom_nodes and name in self.dag_nodes:
            return name

        names = [k for k,v in self.peak_nodes.items() if v is peak_fc]
        assert len(names) <2, names
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
            if not issubclass(dag_nodes[0], Source):
                raise ValueError("Needs to be source")
            if not issubclass(dag_nodes[1], Sink):
                raise ValueError("Needs to be source")
        self.dag_nodes[node_name] = dag_nodes
        self.peak_nodes[node_name] = peak_node
        self.coreir_modules[node_name] = cmod
        self._node_names.add(node_name)


    def add_from_nodes(self, nodes, node_name):
        self.add(node_name, nodes.peak_nodes[node_name], nodes.coreir_modules[node_name], nodes.dag_nodes[node_name])

    #add a copy of nodes[node_name] to self
    def copy(self, nodes, node_name):
        peak_node = nodes.peak_nodes[node_name]
        cmod = nodes.coreir_modules[node_name]
        dag_nodes = nodes.dag_nodes[node_name]
        self.add(node_name, peak_node, cmod, dag_nodes)

    #TODO just change staticattrs to pass in input_t and output_t
    #Have that indicate whether there is dynamic type or not
    #If this is state, then it creates two nodes a source and sink
    def create_dag_node(self, node_name, num_children, stateful: bool, attrs: tp.List = (), static_attrs: tp.Dict = {}, parents=(), modparams=()):
        assert isinstance(static_attrs, dict)
        if "iname" in attrs:
            raise ValueError("Cannot have 'iname' in attrs")

        attrs += ("iname",)

        if "type" in static_attrs and is_modified(static_attrs["type"]):
            raise ValueError(f"{T} cannot be modified")
        parents += (DagNode,)
        if stateful:
            assert "type" not in static_attrs
            input_t = static_attrs["input_t"] if "input_t" in static_attrs else None
            output_t = static_attrs["output_t"] if "output_t" in static_attrs else None
            assert (input_t is None and output_t is None) or (input_t is not None and output_t is not None)
            snk_static_attrs = {}
            src_static_attrs = {}
            if (input_t is not None):
                snk_static_attrs = dict(type=input_t)
            if (output_t is not None):
                src_static_attrs = dict(type=output_t)
            sink_node = type(node_name + "Sink", parents + (Sink,), dict(
                num_children=num_children,
                nodes=self,
                node_name=node_name,
                attributes=attrs,
                static_attributes=snk_static_attrs,
                modparams=modparams
            ))
            #Create the 'source node'
            src_node = type(node_name + "Source", parents + (Source,), dict(
                num_children=0,
                nodes=self,
                node_name=node_name,
                attributes=attrs,
                static_attributes=src_static_attrs,
                modparams=()
            ))
            sink_node.source_t = src_node
            src_node.sink_t = sink_node
            return src_node, sink_node
        else:
            if "type" not in attrs and "type" not in static_attrs:
                attrs += ("type",)
            node = type(node_name, parents, dict(
                num_children=num_children,
                nodes=self,
                node_name=node_name,
                attributes=attrs,
                static_attributes=static_attrs,
                modparams=modparams
            ))
            return node

#Select gotes 1 ->1
#Input goes 0 -> 1
#Output goes N->0

Common = Nodes("Common")
Select = Common.create_dag_node("Select", 1, False, ("field",))
Select.__str__ = lambda self: f"Select<{self.field}>"

#Represents a delay of 1 cycle
PipelineRegister = Common.create_dag_node("PipelineRegister", 1, False, ("type",))




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


Constant = Common.create_dag_node("Constant", 0, False, attrs=("value",), parents=(ConstAssemble,))
Constant.__str__ = lambda self: f"C<{self.value}>"

class State(object): pass
class Source(State):
    def set_sink(self, sink):
        self.sink = sink
class Sink(State):
    def set_source(self, source):
        self.source =source


Input = Common.create_dag_node("Input", 0, False, parents=(Source,))
Output = Common.create_dag_node("Output", -1, False, parents=(Sink,))
Input.sink_t = Output
Output.source_t = Input


#Generic register that could have backedges
RegisterSource, RegisterSink = Common.create_dag_node("Register", 1, True, attrs=("type",))


InstanceInput = Common.create_dag_node("InstanceInput", 0, False, parents=(Source,))
InstanceOutput = Common.create_dag_node("InstanceOutput", -1, False, parents=(Sink,))
InstanceInput.sink_t = InstanceOutput
InstanceOutput.source_t = InstanceInput

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

    static_attributes = {}
    nodes = Common

#This node represents a way to construct generic types from its fields
#The inputs of this node are specified using the selects tuple
#selects = (path0, path1, ..., pathn)
class Combine(DagNode):
    def __init__(self, *children, type, iname = None, tu_field=None):
        if iname is None:
            super().__init__(*children, type=type)
        else:
            super().__init__(*children, type=type, iname=iname,)
        if issubclass(type, (Sum, TaggedUnion)):
            if tu_field is None:
                raise ValueError("Combine Tagged union must have a field")
            if tu_field not in type.field_dict:
                raise ValueError(f"{tu_field} not in {type}")
            self.tu_field = tu_field
        else:
            self.tu_field = None

    @property
    def num_children(self):
        if issubclass(self.type, (Product, Tuple)):
            return len(self.type.field_dict)
        elif issubclass(self.type, (Sum, TaggedUnion)):
            return 1

    @property
    def attributes(self):
        attrs = ("type", "iname")
        if hasattr(self, "tu_field"):
            attrs = (*attrs, "tu_field")
        return attrs

    static_attributes = {}
    nodes = Common
    node_name = "Combine"
