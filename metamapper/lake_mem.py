from lake.top.extract_tile_info import get_interface, extract_top_config
from lake.top.lake_top import LakeTop
from lake.utils.sram_macro import SRAMMacroInfo
from lake.passes.passes import change_sram_port_names
from hwtypes.adt import Tuple, Product
from peak import family, family_closure, Peak, name_outputs, Const

import kratos as kts


def gen_MEM_fc(data_width=16,  # CGRA Params
               mem_width=64,
               mem_depth=512,
               banks=1,
               input_iterator_support=6,  # Addr Controllers
               output_iterator_support=6,
               input_config_width=16,
               output_config_width=16,
               interconnect_input_ports=2,  # Connection to int
               interconnect_output_ports=2,
               mem_input_ports=1,
               mem_output_ports=1,
               use_sram_stub=True,
               sram_macro_info=SRAMMacroInfo("TS1N16FFCLLSBLVTC512X32M4S",
                                             wtsel_value=0, rtsel_value=1),
               read_delay=1,  # Cycle delay in read (SRAM vs Register File)
               rw_same_cycle=False,  # Does the memory allow r+w in same cycle?
               agg_height=4,
               tb_sched_max=16,
               config_data_width=32,
               config_addr_width=8,
               num_tiles=1,
               fifo_mode=True,
               add_clk_enable=True,
               add_flush=True,
               override_name=None,
               gen_addr=True):
    lake_name = "LakeTop"
    mem_tile = LakeTop(data_width=data_width,
                       mem_width=mem_width,
                       mem_depth=mem_depth,
                       banks=banks,
                       input_iterator_support=input_iterator_support,
                       output_iterator_support=output_iterator_support,
                       input_config_width=input_config_width,
                       output_config_width=output_config_width,
                       interconnect_input_ports=interconnect_input_ports,
                       interconnect_output_ports=interconnect_output_ports,
                       use_sram_stub=use_sram_stub,
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
                       name=lake_name,
                       gen_addr=gen_addr)

    change_sram_port_pass = change_sram_port_names(use_sram_stub, sram_macro_info)
    circ = kts.util.to_magma(mem_tile,
                             flatten_array=True,
                             check_multiple_driver=False,
                             optimize_if=False,
                             check_flip_flop_always_ff=False,
                             additional_passes={"change_sram_port": change_sram_port_pass})

    core_interface = get_interface(mem_tile)
    cfgs = extract_top_config(mem_tile)

    def BV(width):

        return family.MagmaFamily().BitVector[width]

    peak_inputs = {}
    peak_outputs = {}
    peak_configs = {}

    for io_info in core_interface:
        if io_info.is_ctrl:
            assert (not io_info.expl_arr)
            assert (io_info.port_size[0] == 1)
            assert (io_info.port_dir == "PortDirection.In")
            peak_inputs[io_info.port_name] = BV(io_info.port_width)
        else:
            if io_info.port_dir == "PortDirection.In":
                if io_info.expl_arr:
                    assert (io_info.port_size[0] > 1)

                    for idx in range(io_info.port_size[0]):
                        peak_inputs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
                else:
                    peak_inputs[io_info.port_name] = BV(io_info.port_width)
            else:
                if io_info.expl_arr:
                    assert (io_info.port_size[0] > 1)

                    for idx in range(io_info.port_size[0]):
                        peak_outputs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
                else:
                    peak_outputs[io_info.port_name] = BV(io_info.port_width)

    for io_info in cfgs:
        if io_info.expl_arr:
            assert (io_info.port_size[0] > 1)

            for idx in range(io_info.port_size[0]):
                peak_configs[f"{io_info.port_name}_{idx}"] = BV(io_info.port_width)
        else:
            peak_configs[io_info.port_name] = BV(io_info.port_width)

    for k, v in peak_inputs.items(): print(k, v)
    inputs_adt = Product.from_fields('inputs', peak_inputs)
    outputs_adt = Product.from_fields('outputs', peak_outputs)
    configs_adt = Product.from_fields('configs', peak_configs)
    outputs_c = family.MagmaFamily().get_constructor(outputs_adt)

    output_attrs = []
    for k in circ.interface.ports:
        if k in peak_outputs:
            output_attrs.append(k)

    @family_closure
    def MEM_fc(family):

        BV = family.BitVector
        Bit = family.Bit


        @family.assemble(locals(), globals())
        class MEM(Peak):
            def __init__(self):
                self.circ = circ()

            @name_outputs(
                data_out_1=BV[16],
                empty=Bit,
                stencil_valid=Bit,
                full=Bit,
                data_out_0=BV[16],
                sram_ready_out=Bit,
                valid_out_0=Bit,
                valid_out_1=Bit,
                config_data_out=BV[32],
            )
            def __call__(
                self,
                configs: Const(configs_adt),
                chain_data_in_0: BV[16],
                chain_data_in_1: BV[16],
                flush: Bit,
                config_read: Bit,
                ren_in_0: Bit,
                ren_in_1: Bit,
                config_en: BV[2],
                config_write: Bit,
                config_data_in: BV[32],
                clk_en: Bit,
                wen_in: BV[2],
                config_addr_in: BV[8],
                addr_in_0: BV[16],
                addr_in_1: BV[16],
                data_in_0: BV[16],
                data_in_1: BV[16],
            ) -> (BV[16], Bit, Bit, Bit, BV[16], Bit, Bit, Bit, BV[32]):

                circ_inputs = {}
                for port in peak_configs:
                    circ_inputs[port] = getattr(configs, port)

                circ_inputs["addr_in_0"] = addr_in_0
                circ_inputs["addr_in_1"] = addr_in_1
                circ_inputs["config_write"] = config_write.ite(BV[1](1), BV[1](0))
                circ_inputs["config_en"] = config_en
                circ_inputs["config_data_in"] = config_data_in
                ren0 = ren_in_0.ite(BV[1](1), BV[1](0))
                ren1 = ren_in_1.ite(BV[1](1), BV[1](0))
                ren_in = BV[2].concat(ren0, ren1)
                circ_inputs["ren_in"] = ren_in
                circ_inputs["data_in_0"] = data_in_0
                circ_inputs["data_in_1"] = data_in_1
                circ_inputs["wen_in"] = wen_in
                circ_inputs["config_read"] = config_read.ite(BV[1](1), BV[1](0))
                circ_inputs["clk_en"] = clk_en.ite(BV[1](1), BV[1](0))
                circ_inputs["flush"] = flush.ite(BV[1](1), BV[1](0))
                circ_inputs["chain_data_in_0"] = chain_data_in_0
                circ_inputs["chain_data_in_1"] = chain_data_in_1
                circ_inputs["config_addr_in"] = config_addr_in

                circ_outputs = self.circ(**circ_inputs)

                outputs = {}

                for port, circ_output in zip(output_attrs, circ_outputs):
                    print("test", port, type(circ_output))
                    outputs[port] = circ_output

                empty = outputs["empty"] == BV[1](1)
                stencil_valid = outputs["stencil_valid"] == BV[1](1)
                full = outputs["full"] == BV[1](1)
                sram_ready_out = outputs["sram_ready_out"] == BV[1](1)
                valid_out_0 = outputs["valid_out"][0]
                valid_out_1 = outputs["valid_out"][1]
                return (
                    outputs["data_out_1"],
                    empty,
                    stencil_valid,
                    full,
                    outputs["data_out_0"],
                    sram_ready_out,
                    valid_out_0,
                    valid_out_1,
                    outputs["config_data_out_1"],
                )

        return MEM

    return MEM_fc
