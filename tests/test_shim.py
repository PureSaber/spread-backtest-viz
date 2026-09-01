"""Shim tests — implementation lives in quant-report-hub."""

from __future__ import annotations

import warnings

import pytest

from spread_viz import __version__
from spread_viz.cli import build_parser, main


def test_version_is_shim_release():
    assert __version__ == "0.2.0"


def test_parser_has_run_and_compare_subcommands():
    parser = build_parser()
    assert parser.prog == "spread-viz"
    with pytest.raises(SystemExit):
        parser.parse_args(["run", "--help"])


def test_main_emits_deprecation_warning():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with pytest.raises(SystemExit):
            main(["run", "--help"])
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_plot_groups_match_hub():
    from quant_report_hub.config import SPREAD_PLOT_GROUPS

    assert set(SPREAD_PLOT_GROUPS.keys()) >= {"all", "universe", "diagnostic", "common"}
    assert len(SPREAD_PLOT_GROUPS["all"]) == 15
