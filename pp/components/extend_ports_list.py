from typing import Any, Dict, List, Optional

from pp.cell import cell
from pp.component import Component
from pp.port import Port, auto_rename_ports
from pp.types import ComponentOrFactory


@cell
def extend_ports_list(
    ports: List[Port],
    extension_factory: ComponentOrFactory,
    extension_settings: Optional[Dict[str, Any]] = None,
    extension_port_name: str = "W0",
) -> Component:
    """Returns a component with extension to list of ports."""
    c = Component()
    extension_settings = extension_settings or {}
    extension = (
        extension_factory(**extension_settings)
        if callable(extension_factory)
        else extension_factory
    )

    for i, port in enumerate(ports):
        extension_ref = c << extension
        extension_ref.connect(extension_port_name, port)

        for port_name, port in extension_ref.ports.items():
            c.add_port(f"{i}_{port_name}", port=port)

    auto_rename_ports(c)
    return c


if __name__ == "__main__":
    import pp

    c = pp.c.mmi1x2()
    from pp.components.straight_heater import straight_with_heater

    cr = extend_ports_list(
        ports=c.get_ports_list(), extension_factory=straight_with_heater
    )
    c.add_ref(cr)
    c.show()
