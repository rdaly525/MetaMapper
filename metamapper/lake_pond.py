from lake.top.extract_tile_info import get_interface, extract_top_config
from lake.top.pond import Pond
from lake.utils.sram_macro import SRAMMacroInfo
from lake.passes.passes import change_sram_port_names
from hwtypes.adt import Tuple, Product
from peak import family, family_closure, Peak, name_outputs, Const

import kratos as kts


def gen_Pond_fc(data_width=16,  # CGRA Params
                 mem_depth=32,
                 default_iterator_support=2,
                 interconnect_input_ports=1,  # Connection to int
                 interconnect_output_ports=1,
                 config_data_width=32,
                 config_addr_width=8,
                 cycle_count_width=16,
                 add_clk_enable=True,
                 add_flush=True):
    lake_name = "Pond_pond"
    pond_dut = Pond(data_width=data_width,  # CGRA Params
                            mem_depth=mem_depth,
                            default_iterator_support=default_iterator_support,
                            interconnect_input_ports=interconnect_input_ports,  # Connection to int
                            interconnect_output_ports=interconnect_output_ports,
                            config_data_width=config_data_width,
                            config_addr_width=config_addr_width,
                            cycle_count_width=cycle_count_width,
                            add_clk_enable=add_clk_enable,
                            add_flush=add_flush)

    circ = kts.util.to_magma(pond_dut,
                            flatten_array=True,
                            check_multiple_driver=False,
                            optimize_if=False,
                            check_flip_flop_always_ff=False)
    core_interface = get_interface(pond_dut)
    cfgs = extract_top_config(pond_dut)
    
    def BV(width):
        return family.MagmaFamily().BitVector[width]

    peak_outputs = {}

    for io_info in core_interface:
        if not io_info.is_ctrl:
            if io_info.port_dir != "PortDirection.In":
                if io_info.expl_arr:
                    if io_info.port_size[0] > 1:
                        for idx in range(io_info.port_size[0]):
                            peak_outputs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
                    else:
                        peak_outputs[f"{io_info.port_name}"] = BV(io_info.port_width)
                else:
                    peak_outputs[io_info.port_name] = BV(io_info.port_width)

    peak_configs = {}
    for io_info in cfgs:
        if io_info.expl_arr:
            assert (io_info.port_size[0] > 1)

            for idx in range(io_info.port_size[0]):
                peak_configs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
        else:
            peak_configs[io_info.port_name] = BV(io_info.port_width)

    configs_adt = Product.from_fields('configs', peak_configs)

    output_attrs = []
    for k in circ.interface.ports:
        if k in peak_outputs:
            output_attrs.append(k)

    @family_closure
    def Pond_fc(family):

        BV = family.BitVector
        Bit = family.Bit


        @family.assemble(locals(), globals())
        class Pond(Peak):
            # def __init__(self):
            #     self.circ = circ()

            @name_outputs(
                data_out_pond_0=BV[16],
                valid_out_pond=Bit
            )
            def __call__(
                self,
                flush: Bit,
                clk_en: Bit,
                data_in_pond_0: BV[16]
            ) -> (BV[16], Bit):

                circ_inputs = {}
                circ_inputs["data_in_pond"] = data_in_pond_0
                circ_inputs["clk_en"] = clk_en.ite(BV[1](1), BV[1](0))
                circ_inputs["flush"] = flush.ite(BV[1](1), BV[1](0))

                # circ_outputs = self.circ(**circ_inputs)

                # outputs = {}
                # for port, circ_output in zip(output_attrs, circ_outputs):
                #     outputs[port] = circ_output

                return (
                    data_in_pond_0,
                    flush
                )

        return Pond

    return Pond_fc
