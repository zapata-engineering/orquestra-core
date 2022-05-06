################################################################################
# © Copyright 2020-2022 Zapata Computing Inc.
################################################################################
from orquestra.pythontemplate.foo import bar


def test_bar_returns_42():
    assert bar() == 42
