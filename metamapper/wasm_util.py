from .node import Dag, Nodes

def peak_to_wasm_dag(WasmNodes: Nodes, CoreIRNodes: Nodes, peak_fc) -> Dag:
    raise NotImplementedError()

def rr_from_node(nodes: Nodes, name):
    node = nodes.dag_nodes[name]
    peak_fc = nodes.peak_nodes[name]
    replace = peak_to_wasm_dag(peak_fc)
