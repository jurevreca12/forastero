import sys
import os
from typing import Callable, Any
from pathlib import Path
import pytest
from pytest import FixtureRequest
from cocotb.handle import SimHandleBase
from cocotb_tools.runner import get_runner

SIM = os.getenv("SIM", default="verilator")

@pytest.fixture(scope="session")
def arbiter_fixture(request: FixtureRequest) -> Callable[[], Any] | SimHandleBase:
    prj_dir = Path(__file__).resolve().parent
    root_dir = prj_dir.parent
    sys.path.append(str(prj_dir))
    sys.path.append(str(root_dir))
    runner = get_runner(SIM)
    runner.build(
        sources=[root_dir / "common" / "rtl" / "arbiter.sv"],
        hdl_toplevel="arbiter"
    )
    return lambda: runner.test(
        hdl_toplevel="arbiter", 
        test_module=["test_random_iterable", "test_random", "test_sequences", "test_smoke"],
        test_dir=prj_dir,
    )
