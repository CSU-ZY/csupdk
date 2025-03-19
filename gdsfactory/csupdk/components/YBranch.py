import gdsfactory as gf
from gdsfactory.components import straight, bend_euler
from gdsfactory import Component

# @gf.cell(check_instances=False)
def y_branch(
    length1: float = 15.0,
    length2: float = 10.0,
    bend_radius: float = 10,             
    width: float = 0.5,
    angle1: float = 45,
    angle2: float = 45,
    cross_section: str = "strip",  # 这里是直接使用字符串来表示交叉截面
) -> Component:
    r"""Y-branch waveguide.

    Args:
        length1: Length of the input waveguide.
        length2: Length of the output waveguide.
        bend_radius: Radius of the first bend.
        width: Width of the waveguide.
        angle1: Angle for the first branch.
        angle2: Angle for the second output direction.
        cross_section: Cross-section type for the waveguide.
    """
    c = gf.Component()

    # 创建输入波导
    wg_input = c << gf.components.straight(length=length1, width=width)

    # 创建第一对弯曲波导（用于分支）
    bend_left1 = c << gf.components.bend_euler(angle=angle1, radius=bend_radius, width=width)
    bend_right1 = c << gf.components.bend_euler(angle=-angle1, radius=bend_radius, width=width)

    # 创建两个直波导（连接段）
    wg_left = c << gf.components.straight(length=length2, width=width)
    wg_right = c << gf.components.straight(length=length2, width=width)

    # 创建第二对弯曲波导（用于调整输出方向）
    bend_left2 = c << gf.components.bend_euler(angle=-angle2, radius=bend_radius, width=width)
    bend_right2 = c << gf.components.bend_euler(angle=angle2, radius=bend_radius, width=width)

    # 连接输入波导到第一对弯曲波导
    bend_left1.connect("o1", wg_input.ports["o2"])
    bend_right1.connect("o1", wg_input.ports["o2"])

    # 连接第一对弯曲波导到直波导
    wg_left.connect("o1", bend_left1.ports["o2"])
    wg_right.connect("o1", bend_right1.ports["o2"])

    # 连接直波导到第二对弯曲波导
    bend_left2.connect("o1", wg_left.ports["o2"])
    bend_right2.connect("o1", wg_right.ports["o2"])

    c.flatten()  # Flatten the component to resolve any issues with nested components

    return c


c = y_branch()
c.show() 
# c_unlocked = c.copy()
# c_unlocked.flatten()  # 展开所有子组件
# c_unlocked.show()  # 显示组件

