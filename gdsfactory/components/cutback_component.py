import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler180
from gdsfactory.components.component_sequence import component_sequence
from gdsfactory.components.straight import straight
from gdsfactory.components.taper import taper
from gdsfactory.components.taper_from_csv import taper_0p5_to_3_l36
from gdsfactory.types import ComponentFactory


@gf.cell
def cutback_component(
    component: ComponentFactory = taper_0p5_to_3_l36,
    cols: int = 4,
    rows: int = 5,
    radius: float = 5.0,
    port1: str = "o1",
    port2: str = "o2",
    bend180: ComponentFactory = bend_euler180,
    straight: ComponentFactory = straight,
) -> Component:
    """Returns a daisy chain of components for measuring their loss.

    Args:
        component: for cutback
        cols
        rows
        radius: for bend
        port1: name of first optical port
        port2: name of second optical port
        bend180: ubend
        straight: waveguide function to connect both sides

    """
    component = component() if callable(component) else component
    bendu = bend180(radius=radius)
    straight_component = straight()

    # Define a map between symbols and (component, input port, output port)
    symbol_to_component = {
        "A": (component, port1, port2),
        "B": (component, port2, port1),
        "D": (bendu, "o1", "o2"),
        "C": (bendu, "o2", "o1"),
        "-": (straight_component, "o1", "o2"),
        "_": (straight_component, "o2", "o1"),
    }

    # Generate the sequence of staircases

    s = ""
    for i in range(rows):
        s += "AB" * cols
        s += "D" if i % 2 == 0 else "C"

    s = s[:-1]
    s += "-_"

    for i in range(rows):
        s += "AB" * cols
        s += "D" if (i + rows) % 2 == 0 else "C"

    s = s[:-1]

    # Create the component from the sequence
    c = component_sequence(sequence=s, symbol_to_component=symbol_to_component)
    n = len(s) - 2
    c.copy_child_info(component)
    c.info["components"] = n
    c.info["parent_name"] = f"loopback_{component.get_parent_name()}_{n}"
    return c


# straight_wide = gf.partial(straight, width=3, length=20)
# bend180_wide = gf.partial(bend_euler180, width=3)
component_flipped = gf.partial(taper, width2=0.5, width1=3)
straight_long = gf.partial(straight, length=20)


@gf.cell
def cutback_component_mirror(
    component: ComponentFactory = component_flipped,
    cols: int = 4,
    rows: int = 5,
    radius: int = 10,
    port1: str = "o2",
    port2: str = "o1",
    bend180: ComponentFactory = bend_euler180,
    straight: ComponentFactory = straight_long,
) -> Component:
    """Returns a daisy chain of components for measuring their loss.

    Flips component. Useful when 'o2' is the port that you want to route to

    Args:
        component: for cutback
        cols
        rows
        radius: for bend
        port1: name of first optical port
        port2: name of second optical port
        bend180: ubend
        straight: waveguide function to connect both sides

    """
    component = component() if callable(component) else component
    bendu = bend180(radius=radius)
    straight_component = straight()

    # Define a map between symbols and (component, input port, output port)
    symbol_to_component = {
        "A": (component, port1, port2),
        "B": (component, port2, port1),
        "D": (bendu, "o1", "o2"),
        "C": (bendu, "o2", "o1"),
        "-": (straight_component, "o1", "o2"),
        "_": (straight_component, "o2", "o1"),
    }

    s = ""
    for i in range(rows):
        s += "AB" * cols
        s += "C" if i % 2 == 0 else "D"

    s = s[:-1]
    s += "-_"

    for i in range(rows):
        s += "AB" * cols
        s += "D" if (i + rows + 1) % 2 == 0 else "C"

    s = s[:-1]

    c = component_sequence(sequence=s, symbol_to_component=symbol_to_component)
    n = len(s) - 2
    c.copy_child_info(component)
    c.info["components"] = n
    c.info["parent_name"] = f"loopback_{component.get_parent_name()}_{n}"
    return c


# cutback_component_mirror = gf.partial(
#     cutback_component, port2="o1", port1="o2", component=component_flipped, straight=straight_long
# )


if __name__ == "__main__":
    c = cutback_component()
    # c = cutback_component_mirror()
    c = gf.routing.add_fiber_single(c)
    c.show()
