#!/usr/bin/env python

from pprint import pprint

from edm_parser.parser import EDMParser, EDMParserError


def main():
    parser = EDMParser()

    try:
        ast = parser.parse_file("examples/motor.edm")

        print("YAML parsing successful!")
        pprint(ast)

    except EDMParserError as exc:
        print(f"Parser error: {exc}")


if __name__ == "__main__":
    main()