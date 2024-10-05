import json
import os
from typing import Any

from lsa_cli_smdmrr.annotation_parser import AnnotationParser
from lsa_cli_smdmrr.annotations_to_entities_converter import AnnotationsToEntitiesConverter
from lsa_cli_smdmrr.config import Config
from lsa_cli_smdmrr.models import SourceFileAnnotations

TEST_DATA_PATH: str = os.path.join("./tests/test_data")


def load_json(file_path: str) -> Any:
    with open(os.path.join(TEST_DATA_PATH, file_path), "r") as file:
        return json.load(file)


def test_annotation_parser() -> None:
    annotations: list[SourceFileAnnotations] = AnnotationParser(
        Config.parser_exclude, "@lc-", Config.extensions_map
    ).parse(TEST_DATA_PATH)
    entities_json: list[dict[str, Any]] = [
        entity.to_json()
        for entity in AnnotationsToEntitiesConverter(Config.annotations_markers_map).convert(
            annotations
        )
    ]
    annotations_json: list[dict[str, Any]] = [annotation.to_json() for annotation in annotations]

    expected_annotations: dict[str, Any] = load_json("lsa_annotations_expected.json")
    assert annotations_json == expected_annotations["filesAnnotations"]
    expected_entities: dict[str, Any] = load_json("lsa_entities_expected.json")
    assert entities_json == expected_entities["entities"]
