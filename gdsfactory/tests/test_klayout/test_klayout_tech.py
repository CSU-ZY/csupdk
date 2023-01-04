from __future__ import annotations

from pytest_regressions.data_regression import DataRegressionFixture

from gdsfactory.config import PATH

try:
    from gdsfactory.technology.klayout_tech import LayerViews
except Exception:
    print("klayout not installed")


def test_klayout_tech_create(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:

    lyp = LayerViews.from_lyp(str(PATH.klayout_lyp))

    if check:
        data_regression.check(lyp.dict())


if __name__ == "__main__":
    test_klayout_tech_create(None, check=False)
