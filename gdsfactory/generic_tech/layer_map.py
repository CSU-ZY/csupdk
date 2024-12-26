import gdsfactory as gf

Layer = tuple[int, int]


#这部分是给Layer起个名字，让layer可以被调用，用于组件的描述
class LAYER(gf.LayerEnum):
    """Generic layermap based on book.

    Lukas Chrostowski, Michael Hochberg, "Silicon Photonics Design",
    Cambridge University Press 2015, page 353
    You will need to create a new LayerMap with your specific foundry layers.
    """

    layout = gf.constant(gf.kcl.layout)

    WAFER: Layer = (999, 0)

    WG: Layer = (1, 0)
    WGCLAD: Layer = (111, 0)
    SLAB150: Layer = (2, 0)
    SHALLOW_ETCH: Layer = (2, 6)
    SLAB90: Layer = (3, 0)
    DEEP_ETCH: Layer = (3, 6)
    DEEPTRENCH: Layer = (4, 0)
    GE: Layer = (5, 0)
    UNDERCUT: Layer = (6, 0)
    WGN: Layer = (34, 0)
    WGN_CLAD: Layer = (36, 0)

    N: Layer = (20, 0)
    NP: Layer = (22, 0)
    NPP: Layer = (24, 0)
    P: Layer = (21, 0)
    PP: Layer = (23, 0)
    PPP: Layer = (25, 0)
    GEN: Layer = (26, 0)
    GEP: Layer = (27, 0)

    HEATER: Layer = (47, 0)
    M1: Layer = (41, 0)
    M2: Layer = (45, 0)
    M3: Layer = (49, 0)
    MTOP: Layer = (49, 0)
    VIAC: Layer = (40, 0)
    VIA1: Layer = (44, 0)
    VIA2: Layer = (43, 0)
    PADOPEN: Layer = (46, 0)

    DICING: Layer = (100, 0)
    NO_TILE_SI: Layer = (71, 0)
    PADDING: Layer = (67, 0)
    DEVREC: Layer = (68, 0)
    FLOORPLAN: Layer = (64, 0)
    TEXT: Layer = (66, 0)
    PORT: Layer = (1, 10)
    WG_PIN: Layer = (1, 10)
    PORTE: Layer = (1, 11)
    PORTH: Layer = (70, 0)
    SHOW_PORTS: Layer = (1, 12)
    LABEL_INSTANCE: Layer = (206, 0)
    LABEL_SETTINGS: Layer = (202, 0)
    TE: Layer = (203, 0)
    TM: Layer = (204, 0)
    DRC_MARKER: Layer = (205, 0)
    
    SOURCE: Layer = (110, 0)
    MONITOR: Layer = (101, 0)



#新添加的层--用于测试
    csulayer1:Layer = (400,0)
    csulayer2:Layer = (401,0)
    csulayer3:Layer = (402,0)

#新建关于工艺流程的层，如下：
    Si_Sub: Layer = (88, 0)
    SiO_Bottom_Clad: Layer = (87,0)

    SiO_WG_1_Core: Layer = (1,1)
    SiO_WG_1_Clad: Layer = (1,2)
    SiO_WG_2_Core: Layer = (2,1)
    SiO_WG_2_Clad: Layer = (2,2)
    SiO_WG_3_Core: Layer = (3,1)
    SiO_WG_3_Clad: Layer = (3,2)

    SiO_ToP_Clad: Layer = (4,0)
    Metal_TiN: Layer = (10,0)
    SiO_Oxide_1: Layer = (11,0)
    Metal_Al: Layer = (12,0)
    Metal_Ti: Layer = (13,0)
    SiN: Layer = (14,0)

    #Dopping：
    NWD: Layer = (30,0)
    PWD: Layer = (31,0)
    ND1: Layer = (32,0)
    PD1: Layer = (33,0)
    ND2: Layer = (34,0)
    PD2: Layer = (35,0)
    ND_Ohmic: Layer = (36,0)
    PD_Ohmic: Layer = (37,0)


    #中间还可以任意添加层数


    #注释部分：
    Label_Optical_IO: Layer = (95,0)
    Label_Settings: Layer = (96,0)
    TXT: Layer = (97,0)
    DA: Layer = (98,0)
    DecRec: Layer = (99,0)



gf.kcl.layers = LAYER


if __name__ == "__main__":
    LAYER.my_layer = (1, 2)
