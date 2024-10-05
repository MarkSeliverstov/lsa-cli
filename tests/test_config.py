import json
from typing import Any
from unittest.mock import mock_open, patch

from lsa_cli_smdmrr.config import AnnotationType, Config


def create_config(config: dict[str, Any]) -> Config:
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(config)),
    ), patch("lsa_cli_smdmrr.config.os.path.exists", return_value=True):
        return Config.from_file("test")


def test_config_custom_markers() -> None:
    config: Config = create_config({"markers": {"prefix": "test"}})
    assert config.annotations_markers_map[AnnotationType.PREFIX] == "test"


def test_config_custom_output() -> None:
    config: Config = create_config(
        {"parser": {"output": {"entities": "test", "annotations": "test"}}}
    )
    assert config.output_entities_file == "test"
    assert config.output_annotations_file == "test"


def test_config_custom_exclude() -> None:
    config: Config = create_config({"parser": {"exclude": ["test"]}})
    assert "test" in config.parser_exclude


def test_config_custom_extend() -> None:
    config: Config = create_config({"parser": {"extend": {"jsx": "application/javascript"}}})
    assert config.extensions_map["jsx"] == "application/javascript"
