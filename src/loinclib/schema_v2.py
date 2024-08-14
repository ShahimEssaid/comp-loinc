from __future__ import annotations

import re
import typing as t

from loinclib.view_v2 import Node, Edge

SCHEMA_KEY = '__SCHEMA__'
TYPE_KEY = '__TYPE__'
TAGS_KEY = '__TAGS__'


class Schema:
    def __init__(self, strict: bool = False):
        self.types: t.Dict[t.Any, NodeType] = {}
        self.strict = strict
        self.global_properties: t.Dict[t.Any, Property] = {}
        self.global_edge_types: t.Dict[t.Any, EdgeType] = {}

    def add_node_type(self, *, node_type: NodeType) -> Schema:
        if node_type.edge_type_key in self.types:
            raise ValueError(f"Duplicate type: {node_type}")
        self.types[node_type.edge_type_key] = node_type
        return self

    def get_node_type(self, key: t.Any) -> NodeType:
        return self.types.get(key, None)


class SchemaType:
    def __init__(self, *,
                 type_key: t.Any,
                 name: t.Optional[str] = None,
                 description: t.Optional[str] = None,
                 schema: Schema,
                 strict: bool):
        self.edge_type_key = type_key
        self.name = name
        self.description = description
        self.schema = schema
        self.strict = strict
        self.properties: t.Dict[t.Any, Property] = {}

    def add_property(self, property_: Property):
        if property_.property_key in self.properties:
            raise ValueError(f"Duplicate property: {property_}")
        self.properties[property_.property_key] = property_

    def get_property(self, property_key: t.Any) -> t.Optional[Property]:
        property_ = self.properties.get(property_key, None)
        if property_:
            return property_

        property_ = self.schema.global_properties.get(property_key, None)
        if property_:
            self.properties[property_.property_key] = property_
            return property_

        if self.strict:
            return None

        property_ = Property(property_key=property_key, strict=self.schema.strict)
        self.properties[property_.property_key] = property_
        return property_


class NodeType(SchemaType):
    def __init__(self, *,
                 type_key: t.Any,
                 name: t.Optional[str] = None,
                 description: t.Optional[str] = None,
                 schema: Schema,
                 base_url: str,
                 code_prefix: t.Optional[str] = None,
                 curie_prefix: str,
                 url_regex: str,
                 url_regex_ignore_case: bool = False,
                 strict: bool = False):
        super().__init__(type_key=type_key, name=name, description=description, schema=schema, strict=strict)
        self.base_url = base_url
        self.code_prefix = code_prefix
        self.curie_prefix = curie_prefix
        self.url_regex = url_regex

        self.property_types: t.Dict[t.Any, Property] = dict()
        self.edge_types: t.Dict[t.Any, EdgeType] = dict()

        flags = 0
        if url_regex_ignore_case:
            flags = flags | re.IGNORECASE
        self.url_regex_pattern: re.Pattern = re.compile(url_regex, flags)

    def get_id_from_code(self, code: str) -> str:
        return self.get_url_from_code(code)

    def get_url_from_code(self, code: str) -> str:
        return self.base_url + code

    # def get_node_by_code(self, code: str, graph: nx.Graph, create: bool = False) -> t.Optional[t.Dict]:
    #     node_id = self.get_id_from_code(code)
    #     node = graph.nodes.get(node_id)
    #     if node is None and create:
    #         graph.add_node(node_id)
    #         node = graph.nodes.get(node_id)
    #     return node
    #
    # def get_node_view_by_code(self, code: str, graph: nx.Graph, create: bool = False) -> t.Optional[Node]:
    #     node_id = self.get_id_from_code(code)
    #     if node_id in graph.nodes:
    #         return Node(self, node_id, graph)
    #     if create:
    #         graph.add_node(node_id)
    #         return Node(self, node_id=node_id, graph=graph)

    def add_edge_type(self, edge_type: EdgeType):
        if edge_type.edge_type_key in self.edge_types:
            raise ValueError(f"Duplicate edge: {edge_type}")
        self.edge_types[edge_type.edge_type_key] = edge_type

    def get_edge_type(self, edge_type_key: t.Any) -> t.Optional[EdgeType]:
        edge_type = self.edge_types.get(edge_type_key, None)
        if edge_type:
            return edge_type

        edge_type = self.schema.global_edge_types.get(edge_type_key, None)
        if edge_type:
            self.edge_types[edge_type_key] = edge_type
            return edge_type

        if self.strict:
            return None

        edge_type = EdgeType(edge_type_key=edge_type_key, strict=self.schema.strict, schema=self.schema)
        self.edge_types[edge_type_key] = edge_type
        return edge_type


class EdgeType(SchemaType):
    def __init__(self, *,
                 edge_type_key: t.Any(),
                 name: t.Optional[str] = None,
                 description: t.Optional[str] = None,
                 schema: Schema,
                 strict: bool):
        super().__init__(type_key=edge_type_key, name=name, description=description, strict=strict, schema=schema)


class Property:
    def __init__(self, *,
                 property_key: t.Any(),
                 name: t.Optional[str] = None,
                 description: t.Optional[str] = None,
                 strict: bool):
        self.property_key = property_key
        self.name = name
        self.description = description
        self.strict = strict

    def get_value(self, element: Node | Edge) -> t.Any:
        if isinstance(element, Node):
            return element.graph.nodes[element.node_id][self.property_key]
        else:
            return element.graph.edges[element.node_id, element.to_node_id, element.edge_key][self.property_key]

    def set_value(self, element: Node | Edge, value: t.Any) -> t.Any:
        if isinstance(element, Node):
            element.graph.nodes[element.node_id][self.property_key] = value
        else:
            element.graph.edges[element.node_id, element.to_node_id, element.edge_key][self.property_key] = value
