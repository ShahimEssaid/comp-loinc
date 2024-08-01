from __future__ import annotations

import re
import typing as t


class Schema:
    def __init__(self):
        self.elements: t.Dict[str, SchemaElement] = {}

    def add_element(self, element: SchemaElement) -> Schema:
        if element.element_type in self.elements:
            raise ValueError(f"Duplicate element type: {element}")
        self.elements[element.element_type] = element
        return self

    def get_element(self, element_type: t.Any) -> SchemaElement:
        return self.elements[element_type]


class SchemaElement:
    def __init__(self, *,
                 element_type: t.Any(),
                 name: str,
                 description: str = None):
        self.element_type = element_type
        self.name = name
        self.description = description


class Type(SchemaElement):
    def __init__(self, *,
                 element_type: t.Any(),
                 name: str,
                 description: str = None,
                 base_url: str,
                 code_prefix: str,
                 curie_prefix: str,
                 url_regex: str,
                 url_regex_ignore_case: bool = False):
        super().__init__(element_type=element_type, name=name, description=description)
        self.base_url = base_url
        self.code_prefix = code_prefix
        self.curie_prefix = curie_prefix
        self.url_regex = url_regex

        flags = 0
        if url_regex_ignore_case:
            flags = flags | re.IGNORECASE
        self.url_regex_pattern: re.Pattern = re.compile(url_regex, flags)




class Feature(SchemaElement):
    pass


class Property(Feature):
    pass


class Edge(Feature):
    pass
