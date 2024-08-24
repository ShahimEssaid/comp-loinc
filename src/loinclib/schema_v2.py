from __future__ import annotations

import re
import typing as t
from enum import Enum

import networkx as nx
from networkx import MultiDiGraph

SCHEMA_KEY = '__SCHEMA__'
TYPE_KEY = '__TYPE__'
TAGS_KEY = '__TAGS__'


class Schema:
  def __init__(self, strict: bool = False):
    self.strict = strict
    self.global_properties: t.Dict[Enum, PropertyType] = {}
    self.global_edge_types: t.Dict[Enum, EdgeType] = {}

    self.node_types: t.Dict[Enum, NodeType] = {}

    self.node_type_class_map: t.Dict[Enum, t.Type[NodeType]] = {}

    self.edge_type_class_map: t.Dict[Enum, t.Type[EdgeType]] = {}
    self.property_type_class_map: t.Dict[Enum, t.Type[PropertyType]] = {}

  def add_node_type(self, *, node_type: NodeType) -> Schema:
    if node_type.type_ in self.node_types:
      raise ValueError(f"Duplicate type: {node_type}")
    self.node_types[node_type.type_] = node_type
    return self

  def get_node_type(self, key: Enum) -> NodeType:
    return self.node_types.get(key, None)

  def getsert_node_type(self, type_: Enum) -> NodeType:
    node_type = self.get_node_type(type_)
    if node_type is None:
      node_type = self.create_node_type(type_=type_, dynamic=True)
      self.node_types[type_] = node_type
    return node_type

  def create_node_type(self, *,
      type_: Enum,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      base_url: t.Optional[str] = None,
      code_prefix: t.Optional[str] = None,
      curie_prefix: t.Optional[str] = None,
      url_regex: t.Optional[str] = None,
      url_regex_ignore_case: bool = True,
      strict: bool = False,
      dynamic: bool = False,
  ) -> NodeType:

    node_type_class = self.node_type_class_map.get(type_, NodeType)

    return node_type_class(type_=type_,
                           name=name,
                           description=description,
                           schema=self,
                           base_url=base_url,
                           code_prefix=code_prefix,
                           curie_prefix=curie_prefix,
                           url_regex=url_regex,
                           url_regex_ignore_case=url_regex_ignore_case,
                           strict=strict,
                           dynamic=dynamic)

  def create_edge_type(self, *,
      type_: Enum,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      strict: bool,
      dynamic: bool = False,
  ) -> EdgeType:

    edge_type_class = self.edge_type_class_map.get(type_, EdgeType)

    return edge_type_class(
        type_=type_,
        name=name,
        description=description,
        schema=self,
        strict=strict,
        dynamic=dynamic
    )

  def create_property_type(self, *,
      type_: Enum,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      property_owner: PropertyOwnerType,
      strict: bool,
      dynamic: bool
  ) -> PropertyType:

    property_class = self.property_type_class_map.get(type_, PropertyType)

    return property_class(
        type_=type_,
        name=name,
        description=description,
        strict=strict,
        dynamic=dynamic,
        property_owner=property_owner,
    )


class SchemaType:
  def __init__(self, *,
      type_: Enum,
      name: t.Optional[str],
      description: t.Optional[str],
      schema: Schema,
      strict: bool,
      dynamic: bool):
    self.type_ = type_
    self.name = name
    self.description = description
    self.schema = schema
    self.strict = strict
    self.dynamic = dynamic
    self.properties: t.Dict[Enum, PropertyType] = {}


class PropertyOwnerType(SchemaType):
  def __init__(self, *,
      type_: Enum,
      name: t.Optional[str],
      description: t.Optional[str],
      schema: Schema,
      strict: bool,
      dynamic: bool):
    super().__init__(type_=type_, name=name, description=description,
                     schema=schema, strict=strict, dynamic=dynamic)
    self.properties: t.Dict[Enum, PropertyType] = {}

  def add_property(self, property_: PropertyType):
    if property_.type_ in self.properties:
      raise ValueError(f"Duplicate property: {property_}")
    self.properties[property_.type_] = property_

  def get_property(self, property_key: Enum) -> t.Optional[PropertyType]:
    return self.properties.get(property_key, None)

  def getsert_property(self, *,
      type_: Enum) -> PropertyType:
    prop = self.get_property(type_)
    if prop:
      return prop
    prop = self.schema.create_property_type(type_=type_,
                                            property_owner=self,
                                            dynamic=True,
                                            strict=self.strict)
    self.properties[type_] = prop
    return prop


class NodeType(PropertyOwnerType):

  def __init__(self, *,
      type_: Enum,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      schema: Schema,
      base_url: str = None,
      code_prefix: t.Optional[str] = None,
      curie_prefix: str = None,
      url_regex: str = None,
      url_regex_ignore_case: bool = True,
      strict: bool = False,
      dynamic: bool = False):
    super().__init__(type_=type_, name=name, description=description,
                     schema=schema, strict=strict, dynamic=dynamic)

    if base_url is None:
      base_url = f'tag:loinclib:{type_.name}.{type_.value}/'

    if url_regex is None:
      url_regex = fr'^{base_url}(P<code>.+)$'

    self.base_url = base_url
    self.code_prefix = code_prefix
    self.curie_prefix = curie_prefix
    self.property_types: t.Dict[Enum, PropertyType] = dict()
    self.edge_types: t.Dict[Enum, EdgeType] = dict()

    flags = 0
    if url_regex_ignore_case:
      flags = flags | re.IGNORECASE
    self.url_regex_pattern: re.Pattern = re.compile(url_regex, flags)

  def get_node(self, *,
      code: str,
      graph: MultiDiGraph) -> t.Optional[Node]:
    node_id = self.get_id_from_code(code)
    if node_id in graph.nodes:
      return Node(node_id=node_id, node_type=self, graph=graph)

  def getsert_node(self, *,
      code: str,
      graph: MultiDiGraph) -> Node:
    node = self.get_node(code=code, graph=graph)
    if node:
      return node
    node_id = self.get_id_from_code(code)
    graph.add_node(node_id, TYPE_KEY=self.type_)
    return Node(node_id=node_id, node_type=self, graph=graph)

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
    if edge_type.type_ in self.edge_types:
      raise ValueError(f"Duplicate edge: {edge_type}")
    self.edge_types[edge_type.type_] = edge_type

  def get_edge_type(self, edge_type_key: Enum) -> t.Optional[EdgeType]:
    edge_type = self.edge_types.get(edge_type_key, None)
    if edge_type:
      return edge_type

    edge_type = self.schema.global_edge_types.get(edge_type_key, None)
    if edge_type:
      self.edge_types[edge_type_key] = edge_type
      return edge_type

    if self.strict:
      return None

    edge_type = EdgeType(type_=edge_type_key, strict=self.schema.strict,
                         schema=self.schema)
    self.edge_types[edge_type_key] = edge_type
    return edge_type


class EdgeType(PropertyOwnerType):
  def __init__(self, *,
      type_: Enum,
      name: t.Optional[str] = None,
      description: t.Optional[str] = None,
      schema: Schema,
      strict: bool = False,
      dynamic: bool):
    super().__init__(type_=type_, name=name, description=description,
                     strict=strict, schema=schema, dynamic=dynamic)


class PropertyType(SchemaType):
  def __init__(self, *,
      type_: Enum,
      name: t.Optional[str],
      description: t.Optional[str],
      strict: bool,
      dynamic: bool,
      property_owner: PropertyOwnerType):
    super().__init__(type_=type_, name=name, description=description,
                     schema=property_owner.schema, strict=strict,
                     dynamic=dynamic)
    self.property_holder = property_owner

  def get_value(self, element: Node | Edge) -> Enum:
    if isinstance(element, Node):
      return element.graph.nodes[element.node_id][self.type_]
    else:
      return element.graph.edges[
        element.node_id, element.to_node_id, element.edge_key][
        self.type_]

  def set_value(self, element: Node | Edge, value: Enum) -> None:
    if value is None:
      del element.get_properties()[self.type_]
    else:
      element.get_properties()[self.type_] = value


class Element:
  def __init__(self, *,
      node_id: str,
      graph: nx.MultiDiGraph):
    self.node_id: str = node_id
    self.graph: nx.MultiDiGraph = graph

  def get_properties(self) -> t.Dict[Enum, t.Any]:
    pass


class Node(Element):
  def __init__(self, *,
      node_id: str,
      node_type: NodeType,
      graph: nx.MultiDiGraph):
    super().__init__(node_id=node_id, graph=graph)
    self.node_type: NodeType = node_type

  def get_property(self, type_: Enum) -> t.Any:
    property_type = self.node_type.get_property(type_)
    if property_type is None:
      return None
    return property_type.get_value(self)

  def set_property(self, *,
      type_: Enum,
      value: t.Any) -> Node:
    property_type = self.node_type.getsert_property(type_=type_)
    property_type.set_value(self, value)
    return self

  def get_properties(self) -> t.Dict[Enum, t.Any]:
    return self.graph.nodes[self.node_id]



  # def get_out_edges(self, type_keys: t.Optional[Enum | t.Set[Enum]] = None) -> \
  #     t.Iterator[Edge]:
  #   type_keys = type_keys if isinstance(type_keys, set) else set(
  #       type_keys) if type_keys else None  # todo: fix?
  #   for from_node, to_node, edge_key, data in self.graph.edges(
  #       nbunch=self.node_id, data=True, keys=True):
  #     type_key = data.get(TYPE_KEY, None)
  #     self.node_type.get_edge()
  #     if type_keys is None or type_key in type_keys:
  #       edge_view = Edge(edge_type_key=type_key, from_node_id=from_node,
  #                        to_node_id=to_node,
  #                        edge_key=edge_key, graph=self.graph)
  #   # todo: fix
  #   return None

  # def get_out_edges_by_type(self, type_key: Enum) -> t.Iterator[Edge]:
  #
  #   for from_node, to_node, edge_key, data in self.graph.edges(
  #       nbunch=self.node_id, data=True, keys=True):
  #     if TYPE_KEY in data and data[TYPE_KEY] == type_key:
  #       edge_view = Edge(edge_type_key=type_key, from_node_id=from_node,
  #                        to_node_id=to_node,
  #                        edge_key=edge_key, graph=self.graph)
  #       yield edge_view

  # def get_or_create_out_edge_type(self, *,
  #     edge_type_key: Enum, target_type_key: Enum,
  #     target_code_code: str) -> Edge:
  #
  #   target_type = self.node_type_key.schema.get_node_type()
  #   target_id = target_type.get_id_from_code(target_code_code)
  #
  #   target = self.graph.succ[self.node_id].get(target_id, None)
  #   if target is None:
  #     self.graph.add_edge(self.node_id, target_id,
  #                         TYPE_KEY=target_node_type.type_)
  #   else:
  #     pass

  # @staticmethod
  # def get_node_by_code(code: str, type_key: Enum, graph: nx.Graph, schema: Schema, create: bool = False) -> \
  #         t.Optional[Node]:
  #     node_type = schema.get_node_type(type_key)
  #     node_id = node_type.get_id_from_code(code)
  #     node = graph.nodes.get(node_id)
  #     if node is None and create:
  #         graph.add_node(node_id)
  #         node = graph.nodes.get(node_id)
  #
  #     return Node(node_type, node_id, graph)


class Edge(Element):
  def __init__(self, *,
      from_node_id: str,
      to_node_id: str,
      edge_key: int,
      edge_type: EdgeType,
      graph: nx.MultiDiGraph):
    super().__init__(node_id=from_node_id, graph=graph)
    self.to_node_id = to_node_id
    self.edge_key = edge_key
    self.edge_type = edge_type

  def get_property(self, type_: Enum) -> t.Any:
    property_type = self.edge_type.get_property(type_)
    if property_type is None:
      return None
    return property_type.get_value(self)

  def set_property(self, *, type_: Enum, value: t.Any) -> Edge:
    property_type = self.edge_type.getsert_property(type_=type_)
    property_type.set_value(self, value)
    return self

  def get_properties(self) -> t.Dict[Enum, t.Any]:
    return self.graph.edges[
      self.node_id, self.to_node_id, self.edge_key]
