from .visitor import Visited, AbstractDag
import abc
import typing as tp
import coreir

#Passes will be run on this
class DagNode(Visited):
    def __init__(self, *children):
        self.set_children(*children)

    def set_children(self, *children):
        expected_children = type(self).num_children
        if expected_children >=0 and len(children) != expected_children:
            raise ValueError(f"len({children}) != {expected_children}")
        self._children = children

    def children(self):
        return self._children

    #def inputs(self):
    #    return self._children

    # Convenience
    def select(self, field):
        return Select(self, field=field)

    @abc.abstractmethod
    def copy(self):
        pass

    #def coreir_output_name(self, idx):
    #    if self.num_outputs()==1:
    #        return "O"
    #    else:
    #        raise NotImplementedError("TODO")

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

    #def outputs(self):
    #    return self._parents

    #@property
    #def num_outputs(self):
    #    return self.num_parents

    #@property
    #def num_inputs(self):
    #    return len(self.inputs)

    #@property
    #def num_parents(self):
    #    return len(self._parents)


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
        self._node_names = set()

        #if node is stateful, it points to a tuple(Source, Sink)
        self.dag_nodes = {}
        self.peak_nodes = {}
        self.coreir_modules = {}

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
    # The latter is useful because state has two parts to it. In nodes I really need to go from dag_nodes to multiple things
    #If this is state, then it creates two nodes a source and sink
    def create_dag_node(self, node_name, num_children, stateful: bool , attrs: tp.List = (), parents=()):
        if stateful:
            raise NotImplementedError("TODO")

        if "iname" in attrs:
            raise ValueError("Cannot have 'iname' in attrs")

        attrs += ("iname",)
        def __init__(self, *args, **kwargs):
            self.set_children(*args)
            self.set_kwargs(**kwargs)

        def set_kwargs(self, **kwargs):
            if "iname" not in kwargs:
                kwargs.update({"iname":str(id(self))})

            assert len(kwargs) == len(attrs), f"{kwargs} != {attrs}"
            assert all(attr in kwargs for attr in attrs), f"{kwargs} != {attrs}"
            for attr in attrs:
                setattr(self, attr, kwargs[attr])

        def copy(self):
            args = self.children()
            kwargs = {attr:getattr(self, attr) for attr in attrs}
            return type(self)(*args, **kwargs)

        node = type(node_name, parents + (DagNode,), dict(
            _attrs_=attrs,
            __init__=__init__,
            set_kwargs=set_kwargs,
            num_children=num_children,
            copy=copy,
            nodes=self,
            node_name=node_name
        ))
        return node

#Select gotes 1 ->1
#Input goes 0 -> 1
#Output goes N->0

Common = Nodes("Common")
Select = Common.create_dag_node("Select", 1, False, ("field",))
Constant = Common.create_dag_node("Constant", 0, False, ("value",))

class State(object): pass
class Source(State): pass
class Sink(State): pass
#TODO Input/Output should be stateful. Issue is that I want them to be called Input/Output instead of just inheriting from Source/Sink
Input = Common.create_dag_node("Input", 0, False, (), (Source,))
Output = Common.create_dag_node("Output", -1, False, (), (Sink,))
#TODO is this needed
Input.sink_t = Output
Output.source_t = Input
