from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


class EDMParserError(Exception):
    pass


class EDMParser:
    def __init__(self):
        self.yaml = YAML(typ="safe")
        self.yaml.allow_duplicate_keys = False

    def parse_file(self, file_path: str) -> dict:
        path = Path(file_path)

        if not path.exists():
            raise EDMParserError(f"File not found: {path}")

        if not path.is_file():
            raise EDMParserError(f"Not a file: {path}")

        if path.stat().st_size > 1024 * 1024:
            raise EDMParserError("File exceeds maximum size (1 MB)")

        try:
            with path.open("r", encoding="utf-8") as file:
                ast = self.yaml.load(file)

        except UnicodeDecodeError as exc:
            raise EDMParserError("Invalid UTF-8 encoding") from exc

        except YAMLError as exc:
            raise EDMParserError(
                f"YAML parsing failed: {exc}"
            ) from exc

        if ast is None:
            raise EDMParserError("Empty EDM file")

        if not isinstance(ast, dict):
            raise EDMParserError("EDM root must be a mapping")

        return ast
