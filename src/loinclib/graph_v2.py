import typing as t

import networkx as nx

from loinclib.schema_v2 import Schema, Node


class LoinclibGraph:
  def __init__(self, *,
      graph: nx.MultiDiGraph = nx.MultiDiGraph(),
      schema: Schema = Schema(),
  ):
    self.graph: nx.MultiDiGraph = graph
    self.loaded_sources = self.graph.graph.setdefault('loaded_sources', {})
    self.schema: Schema = schema

  def get_node(self, *,
      type_: t.Any,
      code: str):
    return self.schema.get_node_type(type_).get_node(code=code,
                                                     graph=self.graph)

  def getsert_node(self, *,
      type_: t.Any,
      code: str
  ) -> Node:
    return self.schema.get_node_type(type_).getsert_node(code=code,
                                                         graph=self.graph)
