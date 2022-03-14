from lake.top.extract_tile_info import get_interface, extract_top_config
from lake.top.lake_top import LakeTop
from lake.utils.sram_macro import SRAMMacroInfo
from lake.passes.passes import change_sram_port_names
from hwtypes.adt import Tuple, Product
from peak import family, family_closure, Peak, name_outputs, Const
from ast_tools.passes import apply_passes, if_inline, loop_unroll
from ast_tools.macros import inline, unroll
import kratos as kts

def gen_MEM_fc(data_width=16,  # CGRA Params
                 mem_width=64,
                 mem_depth=512,
                 banks=1,
                 input_iterator_support=6,  # Addr Controllers
                 output_iterator_support=6,
                 config_width=16,
                 interconnect_input_ports=2,  # Connection to int
                 interconnect_output_ports=2,
                 mem_input_ports=1,
                 mem_output_ports=1,
                 use_sim_sram=True,
                 sram_macro_info=SRAMMacroInfo("TS1N16FFCLLSBLVTC512X32M4S",
                                               wtsel_value=0, rtsel_value=1),
                 read_delay=1,  # Cycle delay in read (SRAM vs Register File)
                 rw_same_cycle=False,  # Does the memory allow r+w in same cycle?
                 agg_height=4,
                 config_data_width=32,
                 config_addr_width=8,
                 num_tiles=1,
                 fifo_mode=True,
                 add_clk_enable=True,
                 add_flush=True,
                 override_name=None,
                 gen_addr=True,
                 GF=True):

    mem_tile = LakeTop(data_width=data_width,
                              mem_width=mem_width,
                              mem_depth=mem_depth,
                              banks=banks,
                              input_iterator_support=input_iterator_support,
                              output_iterator_support=output_iterator_support,
                              config_width=config_width,
                              interconnect_input_ports=interconnect_input_ports,
                              interconnect_output_ports=interconnect_output_ports,
                              use_sim_sram=use_sim_sram,
                              sram_macro_info=sram_macro_info,
                              read_delay=read_delay,
                              rw_same_cycle=rw_same_cycle,
                              agg_height=agg_height,
                              config_data_width=config_data_width,
                              config_addr_width=config_addr_width,
                              num_tiles=num_tiles,
                              fifo_mode=fifo_mode,
                              add_clk_enable=add_clk_enable,
                              add_flush=add_flush,
                              name="LakeTop",
                              gen_addr=gen_addr,
                              GF=GF)


    change_sram_port_pass = change_sram_port_names(use_sim_sram, sram_macro_info)
    circ = kts.util.to_magma(mem_tile.dut,
                                     flatten_array=True,
                                     check_multiple_driver=False,
                                     optimize_if=False,
                                     check_flip_flop_always_ff=False,
                                     additional_passes={"change_sram_port": change_sram_port_pass})
    
    core_interface = get_interface(mem_tile.dut)
    cfgs = extract_top_config(mem_tile.dut)
    
    def BV(width):
        if width == 1:
            return family.MagmaFamily().Bit
        else:
            return family.MagmaFamily().BitVector[width]

    def BV_out(width):
        #if width == 1:
        #    return family.MagmaFamily().Bit
        #else:
        return family.MagmaFamily().BitVector[width]

    peak_inputs = {}
    peak_outputs = {}
    peak_configs = {}

    for io_info in core_interface:
        if io_info.is_ctrl:
            assert(not io_info.expl_arr)
            assert(io_info.port_size[0] == 1)
            assert(io_info.port_dir == "PortDirection.In")
            peak_inputs[io_info.port_name] = BV(io_info.port_width)
        else:
            if io_info.port_dir == "PortDirection.In":
                if io_info.expl_arr and io_info.port_size[0] > 1:
                    for idx in range(io_info.port_size[0]):
                        peak_inputs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
                else:
                    peak_inputs[io_info.port_name] = BV(io_info.port_width)
            else:
                if io_info.expl_arr and io_info.port_size[0] > 1:
                    for idx in range(io_info.port_size[0]):
                        peak_outputs[f"{io_info.port_name}_{idx}"] = BV_out(io_info.port_width)
                else:
                    peak_outputs[io_info.port_name] = BV_out(io_info.port_width)


    for io_info in cfgs:
        if io_info.expl_arr and io_info.port_size[0] > 1:
            for idx in range(io_info.port_size[0]):
                peak_configs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
        else:
            peak_configs[io_info.port_name] = BV(io_info.port_width)
    
    inputs_adt = Product.from_fields('inputs', peak_inputs)
    configs_adt = Product.from_fields('configs', peak_configs)
    
    sorted_peak_outputs = {}

    output_attrs = []
    for k in circ.interface.ports:
        if k in peak_outputs:
            output_attrs.append(k)
            sorted_peak_outputs[k] = peak_outputs[k]

    outputs_adt = Product.from_fields('outputs', sorted_peak_outputs)
    outputs_c = family.MagmaFamily().get_constructor(outputs_adt)

    @family_closure
    def MEM_fc(family):
        @family.assemble(locals(), globals())
        class MEM(Peak):
            def __init__(self):
                self.circ = circ

            @apply_passes([loop_unroll()])
            @name_outputs(outputs=outputs_adt)
            def __call__(self, configs: Const(configs_adt), inputs: inputs_adt) -> (outputs_adt):

                circ_inputs = {}

                for port_idx in unroll(range(len(peak_inputs))):
                    port = list(peak_inputs)[port_idx]
                    circ_inputs[port] = getattr(inputs, port)

                for port_idx in unroll(range(len(peak_configs))):
                    port = list(peak_configs)[port_idx]
                    circ_inputs[port] = getattr(configs, port)

                breakpoint()
                circ_outputs = self.circ(**circ_inputs)

                outputs = []
                for output_idx in unroll(range(len(output_attrs))):
                    port = output_attrs[output_idx]
                    circ_output = circ_outputs[port]
                    outputs.append(circ_output)

                return outputs_c(*outputs)

        return MEM


    return MEM_fc
