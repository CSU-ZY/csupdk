from gdsfactory.generic_tech.layer_map import LAYER
from gdsfactory.technology import LayerLevel, LayerStack, LogicalLayer
from gdsfactory.technology.processes import (
    Anneal,
    Etch,
    Grow,
    ImplantPhysical,
    Planarize,
    ProcessStep,
)

nm = 1e-3


class LayerStackParameters:
    """values used by get_layer_stack and get_process."""
    """用于层栈和工艺"""

    thickness_substrate: float = 675                   #基板厚度um
    thickness_bottom_clad: float = 15                  #下包层——镀层厚度um
    thickness_wg: float = 220 * nm                     #波导层厚度(core)
    thickness_slab_full_etch: float = 0 * nm           #相当于trench层，全刻蚀，刻蚀深度220nm(SiO_WG_1_Core)
    thickness_slab_deep_etch: float = 90 * nm          #深刻蚀，刻蚀深度130nm(SiO_WG_2_Core)
    thickness_slab_shallow_etch: float = 150 * nm      #浅刻蚀，刻蚀深度70nm(SiO_WG_3_Core)
    thickness_top_clad: float = 20                     #上包层——镀层厚度um

    thickness_metal_TiN: float = 2000 * nm             #TiN加热层厚度：？
    zmin_heater: float = 1.1                           #?
    thickness_heater_clad: float = 20                  #加热层TiN_氧化层um
    thickness_metal_Ti: float = 1400 * nm              #间隔层厚度
    zmin_metal_Ti: float = 1.1                        #?
    thickness_metal_Al: float = 700 * nm               #电极层Al的厚度：？
    zmin_metal_Al: float = 2.3                         #?
    thickness_SiN: float = 350 * nm                    #保护层SiN厚度：？



def get_layer_stack(
    thickness_substrate: float = LayerStackParameters.thickness_substrate,
    thickness_bottom_clad: float = LayerStackParameters.thickness_bottom_clad,    
    thickness_wg: float = LayerStackParameters.thickness_wg,
    thickness_slab_full_etch: float = LayerStackParameters.thickness_slab_full_etch,
    thickness_slab_deep_etch: float = LayerStackParameters.thickness_slab_deep_etch,
    thickness_slab_shallow_etch: float = LayerStackParameters.thickness_slab_shallow_etch,
    thickness_top_clad: float = LayerStackParameters.thickness_top_clad,  
    thickness_metal_TiN: float = LayerStackParameters.thickness_metal_TiN,
    zmin_heater: float = LayerStackParameters.zmin_heater,
    thickness_heater_clad: float = LayerStackParameters.thickness_heater_clad,
    zmin_metal_Ti: float = LayerStackParameters.zmin_metal_Ti,
    thickness_metal_Ti: float = LayerStackParameters.thickness_metal_Ti,
    zmin_metal_Al: float = LayerStackParameters.zmin_metal_Al,
    thickness_metal_Al: float = LayerStackParameters.thickness_metal_Al,
    thickness_SiN: float = LayerStackParameters.thickness_SiN,

    layer_Si_Sub: LogicalLayer = LogicalLayer(layer=LAYER.Si_Sub), #Si基板
    layer_bottom_clad: LogicalLayer = LogicalLayer(layer=LAYER.SiO_Bottom_Clad), #氧化层下包层
    layer_core: LogicalLayer = LogicalLayer(layer=LAYER.WG), #波导核心部分
    layer_slab_full_etch: LogicalLayer = LogicalLayer(layer=LAYER.SiO_WG_1_Slab),
    layer_full_etch: LogicalLayer = LogicalLayer(layer=LAYER.SiO_WG_1_Clad), 
    layer_slab_shallow_etch: LogicalLayer = LogicalLayer(layer=LAYER.SiO_WG_3_Slab),
    layer_shallow_etch: LogicalLayer = LogicalLayer(layer=LAYER.SiO_WG_3_Clad),
    layer_slab_deep_etch: LogicalLayer = LogicalLayer(layer=LAYER.SiO_WG_2_Slab),
    layer_deep_etch: LogicalLayer = LogicalLayer(layer=LAYER.SiO_WG_2_Clad),
    layer_top_clad: LogicalLayer = LogicalLayer(layer=LAYER.SiO_ToP_Clad),
    layer_metal_TiN: LogicalLayer = LogicalLayer(layer=LAYER.Metal_TiN),
    layer_heater_clad: LogicalLayer = LogicalLayer(layer=LAYER.SiO_Oxide_1),
    layer_metal_Ti: LogicalLayer = LogicalLayer(layer=LAYER.Metal_Ti),
    layer_metal_Al: LogicalLayer = LogicalLayer(layer=LAYER.Metal_Al),
    layer_SiN: LogicalLayer = LogicalLayer(layer=LAYER.SiN),
) -> LayerStack:
    """Returns generic LayerStack.

    based on paper https://www.degruyter.com/document/doi/10.1515/nanoph-2013-0034/html

    Args:
        thickness_substrate: substrate thickness in um.
        thickness_bottom_clad: bottom cladding thickness in um.
        thickness_wg: waveguide thickness in um.
        
        thickness_slab_full_etch: slab thickness after full etch in um. equal to thickness of trench.
        thickness_slab_deep_etch: slab thickness after deep etch in um.
        thickness_slab_shallow_etch: slab thickness after shallow etch in um.
        thickness_top_clad: top cladding thickness in um.
        thickness_metal_TiN: metal TiN thickness.
        zmin_heater: TiN heater.
        thickness_heater_clad: heater cladding thickness in um.
        zmin_metal_Ti: metal Ti.
        thickness_metal_Ti: metal Ti thickness.
        zmin_metal_Al: metal Al.
        thickness_metal_Al: metal Al thickness.
        thickness_SiN: SiN thickness.

        layer_Si_Sub: substrate layer.
        layer_bottom_clad: SiO2 bottom cladding layer.
        layer_core: waveguide layer.
        layer_slab_full_etch: full etch slab layer.    
        layer_full_etch: full etch layer.
        layer_slab_deep_etch: deep etch slab layer.        
        layer_deep_etch: deep etch layer.      
        layer_slab_shallow_etch: shallow etch slab layer.
        layer_shallow_etch: shallow etch layer.
        layer_top_clad: SiO2 top cladding layer.
        layer_metal_TiN: heater TiN layer.
        layer_heater_clad: SiO2 heater cladding layer.
        layer_metal_Ti: metal Ti layer.
        layer_metal_Al: metal Al layer.
        layer_SiN: SiN layer for protection.
    """
    thickness_full_etch = thickness_wg - thickness_slab_full_etch         #全刻蚀深度
    thickness_deep_etch = thickness_wg - thickness_slab_deep_etch         #深刻蚀深度
    thickness_shallow_etch = thickness_wg - thickness_slab_shallow_etch   #浅刻蚀深度

    layers = dict(
        substrate=LayerLevel(
            layer=layer_Si_Sub,
            thickness=thickness_substrate,
            zmin=-thickness_substrate - 0, #box_thickness
            material="si",
            mesh_order=101,#?
        ),
        box=LayerLevel(
            layer=layer_Si_Sub,
            thickness= 0, #box_thickness
            zmin= 0, #-box_thickness
            material="sio2",
            mesh_order=9,
        ),        
        bottom_clad=LayerLevel(
            layer=layer_bottom_clad,    
            zmin=0.0,
            material="sio2",
            thickness=thickness_bottom_clad,
            mesh_order=10,
        ),
        core=LayerLevel(
            layer=layer_core - layer_deep_etch - layer_shallow_etch,  #???
            thickness=thickness_wg,
            zmin=0.0,
            material="si",
            mesh_order=2,
           #sidewall_angle=sidewall_angle_wg,
            width_to_z=0.5,
            derived_layer=LogicalLayer(layer=LAYER.WG),
        ),
        shallow_etch=LayerLevel(
            layer=layer_shallow_etch & layer_core,    #???
            thickness=thickness_shallow_etch,
            zmin=0.0,
            material="si",
            mesh_order=1,
            derived_layer=LogicalLayer(layer=LAYER.SiO_WG_3_Slab),#???
        ),
        deep_etch=LayerLevel(
            layer=layer_deep_etch,
            thickness=thickness_deep_etch,
            zmin=0.0,
            material="si",
            mesh_order=1,
            derived_layer=layer_slab_deep_etch, ##???
        ),
        full_etch=LayerLevel(
            layer=layer_full_etch,
            thickness=thickness_full_etch,
            zmin=0.0,
            material="si",
            mesh_order=1,
            derived_layer=layer_slab_full_etch, ##??
        ),
        slab_shallow_etch=LayerLevel(            #slab150
            layer=layer_slab_shallow_etch,
            thickness=150e-3,
            zmin=0,
            material="si",
            mesh_order=3,
        ),
        slab_deep_etch=LayerLevel(                  #slab90
            layer=layer_slab_deep_etch,
            thickness=thickness_slab_deep_etch,
            zmin=0.0,
            material="si",
            mesh_order=2,
        ),
        slab_full_etch=LayerLevel(                  #???slab0，全刻蚀后不存在slab了
            layer=layer_slab_full_etch,
            thickness=thickness_slab_full_etch,
            zmin=0.0,
            material="si",
            mesh_order=2,
        ),
        top_clad=LayerLevel(
            layer=layer_top_clad,                    
            zmin=0.0,
            material="sio2",
            thickness=thickness_top_clad,
            mesh_order=10,
        ),
        TiN=LayerLevel(                        
            layer=layer_metal_TiN,
            thickness=thickness_metal_TiN,
            zmin=thickness_wg + 0, #gap_silicon_to_nitride??
            material="TiN",
            mesh_order=2,
        ),
        heater_clad=LayerLevel(
            layer=layer_heater_clad,               
            zmin=0.0,
            material="sio2",
            thickness=thickness_heater_clad,
            mesh_order=10,
        ),
        Ti=LayerLevel(
            layer=layer_metal_Ti,
            thickness=thickness_metal_Ti,
            zmin=zmin_metal_Ti,
            material="Titanium",
            mesh_order=1,
        ),
        Al=LayerLevel(
            layer=layer_metal_Al,
            thickness=thickness_metal_Al,
            zmin=zmin_metal_Al,          
            material="Aluminum",
            mesh_order=1,
        ),
        SiN=LayerLevel(
            layer=layer_SiN,
            thickness=thickness_SiN,
            zmin=zmin_heater,
            material="SiN",
            mesh_order=2,
        ),
    )

    return LayerStack(layers=layers)


LAYER_STACK = get_layer_stack()

WAFER_STACK = LayerStack(
    layers={
        k: get_layer_stack().layers[k]
        for k in (
            "substrate",
            "box",
            #"core",
        )
    }
)


def get_process() -> tuple[ProcessStep, ...]:
    """Returns generic process to generate LayerStack.

    Represents processing steps that will result in the GenericLayerStack, starting from the waferstack LayerStack.

    based on paper https://www.degruyter.com/document/doi/10.1515/nanoph-2013-0034/html
    """
    return (
        Etch(
            name="strip_etch",           #220nm波导层
            layer=LAYER.WG,
            layers_or=[LAYER.SiO_WG_2_Slab],
            #mask open = WG + SiO_WG_2_Slab
            depth=LayerStackParameters.thickness_wg
            + 0.01,  # slight overetch for numerics 轻微刻深一点
            material="silicon",
            resist_thickness=1.0,     #光刻胶厚度
            positive_tone=False,      #flase代表负胶
        ),
        Etch(
            name="slab_etch",             #波导上的刻蚀，slab
            layer=LAYER.SiO_WG_2_Slab,
            layers_diff=[LAYER.WG],
            depth=LayerStackParameters.thickness_wg
            - LayerStackParameters.thickness_slab_deep_etch,
            material="silicon",
            resist_thickness=1.0,
        ),
        #这部分需要添加一些其他的刻蚀，，，

        #掺杂部分,物理植入过程。将特定的离子（如磷离子）注入到硅等材料中，以改变材料的电学性质。
        #注意区分轻中重掺杂！！
        # See gplugins.process.implant tables for ballpark numbers
        # Adjust to your process

        #量子阱，轻掺
        ImplantPhysical(
            name="deep_NWD_implant",
            layer=LAYER.NWD,
            energy=100, #指定离子的能量，单位通常是电子伏特（eV）
            ion="P", #注入的离子种类，用于N型掺杂
            #"As",表示注入的是砷离子。
            #"P",表示注入的是磷离子（Phosphorus）。磷离子通常用于掺杂硅以调节其导电性。
            dose=1e12,
            #dose 参数表示注入的离子数量，单位通常是每单位面积的离子数量。这里设置为 1e12，即每单位面积注入 10的12次方个离子。
            resist_thickness=1.0,#光刻胶的厚度
        ),
        ImplantPhysical(
            name="shallow_NWD_implant",
            layer=LAYER.NWD,
            energy=50,
            ion="P",
            dose=1e12,
            resist_thickness=1.0,
        ),
        ImplantPhysical(
            name="deep_PWD_implant",
            layer=LAYER.PWD,
            energy=50,
            ion="B", #用于P型掺杂
            #"B",表示硼离子
            #"Al",铝离子也可以用于P型掺杂
            dose=1e12,
            resist_thickness=1.0,
        ),
        ImplantPhysical(
            name="shallow_PWD_implant",
            layer=LAYER.PWD,
            energy=15,
            ion="B",
            dose=1e12,
            resist_thickness=1.0,
        ),
        #PN结，中掺
        ImplantPhysical(
            name="PD1_implant",
            layer=LAYER.PD1,
            energy=15,
            ion="B",
            dose=5e12,
            resist_thickness=1.0,
        ),
        ImplantPhysical(
            name="ND1_implant",
            layer=LAYER.ND1,
            energy=50,
            ion="P",
            dose=5e12,
            resist_thickness=1.0,
        ),
        ImplantPhysical(
            name="PD2_implant",
            layer=LAYER.PD2,
            energy=15,
            ion="B",
            dose=1e15,
            resist_thickness=1.0,
        ),
        ImplantPhysical(
            name="ND2_implant",
            layer=LAYER.ND2,
            energy=100,
            ion="As",
            dose=1e15,
            resist_thickness=1.0,
        ),
        #欧姆接触，重掺
            ImplantPhysical(
            name="PD_Ohmic_implant",
            layer=LAYER.ND_Ohmic,
            energy=15,
            ion="B",
            dose=1e15,
            resist_thickness=1.0,
        ),
        ImplantPhysical(
            name="ND_Ohmic_implant",
            layer=LAYER.PD_Ohmic,
            energy=100,
            ion="As",
            dose=1e15,
            resist_thickness=1.0,
        ),
        # "Temperatures of ~1000C for not more than a few seconds"
        # Adjust to your process
        # https://en.wikipedia.org/wiki/Rapid_thermal_processing

        Anneal(
            name="dopant_activation",
            time=5,
            temperature=1000,
        ), 
        # Etch(
        #     name="viac_etch",
        #     layer=LAYER.VIAC,
        #     depth=LayerStackParameters.zmin_metal1
        #     - LayerStackParameters.thickness_slab_deep_etch
        #     + 0.1,
        #     material="Aluminum",
        #     type="anisotropic",
        #     resist_thickness=1.0,
        #     positive_tone=False,
        # ),
        Grow(
            name="deposit_cladding",
            layer=None,
            thickness=LayerStackParameters.thickness_top_clad
            + LayerStackParameters.thickness_slab_deep_etch,
            material="SiO2_Oxide",
            type="anisotropic",
        ),
        Grow(
            name="viac_metallization2", #金属化，Ti
            layer=None,
            thickness=LayerStackParameters.zmin_metal_Ti
            - LayerStackParameters.thickness_slab_deep_etch,
            material="Titanium",
            type="anisotropic",
        ),      
        Grow(
            name="viac_metallization1", #金属化，Al
            layer=None,
            thickness=LayerStackParameters.zmin_metal_Al
            - LayerStackParameters.thickness_slab_deep_etch,
            material="Aluminum",
            type="anisotropic",
        ),         
        Planarize(
            name="planarization",
            height=LayerStackParameters.thickness_top_clad
            - LayerStackParameters.thickness_slab_deep_etch,
        ),
    )

if __name__ == "__main__":
    # ls = get_layer_stack(substrate_thickness=50.0)
    # ls = get_layer_stack()
    # script = ls.get_klayout_3d_script()
    # print(script)
    # print(ls.get_layer_to_material())
    # print(ls.get_layer_to_thickness())

    for layername, layer in WAFER_STACK.layers.items():
        print(layername, layer.zmin, layer.thickness)
