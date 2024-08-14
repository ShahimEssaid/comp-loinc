from __future__ import annotations

import typing as t

import networkx as nx

from loinclib.schema_v2 import TYPE_KEY, Schema, NodeType


class Element:
    def __init__(self, node_id: str, graph: nx.MultiDiGraph):
        self.node_id: str = node_id
        self.graph: nx.MultiDiGraph = graph


class Node(Element):
    def __init__(self, node_type: t.Any, node_id: str, graph: nx.MultiDiGraph):
        super().__init__(node_id, graph)
        self.node_type: NodeType = node_type

    def set_property(self, *, property_: t.Any, value: t.Any) -> Node:
        self.graph.nodes[self.node_id][property_] = value
        return self

    def get_property(self, property_: t.Any) -> t.Any:
        return self.graph.nodes[self.node_id][property_]

    def get_out_edges(self, type_keys: t.Optional[t.Any | t.Set[t.Any]] = None) -> t.Iterator[Edge]:
        type_keys = type_keys if isinstance(type_keys, set) else set(type_keys) if type_keys
        for from_node, to_node, edge_key, data in self.graph.edges(nbunch=self.node_id, data=True, keys=True):
            type_key =  data.get(TYPE_KEY, None)
            self.node_type.get_edge()
            if type_keys is None or type_key in type_keys:
                edge_view = Edge(edge_type_key=type_key, from_node_id=from_node, to_node_id=to_node,
                                 edge_key=edge_key, graph=self.graph)





    def get_out_edges_by_type(self, type_key: t.Any) -> t.Iterator[Edge]:

        for from_node, to_node, edge_key, data in self.graph.edges(nbunch=self.node_id, data=True, keys=True):
            if TYPE_KEY in data and data[TYPE_KEY] == type_key:
                edge_view = Edge(edge_type_key=type_key, from_node_id=from_node, to_node_id=to_node,
                                 edge_key=edge_key, graph=self.graph)
                yield edge_view

    def get_or_create_out_edge_type(self, *,
                                    edge_type_key: t.Any, target_type_key: t.Any, target_code_code: str) -> Edge:

        target_type = self.node_type_key.schema.get_node_type()
        target_id = target_type.get_id_from_code(target_code_code)

        target = self.graph.succ[self.node_id].get(target_id, None)
        if target is None:
            self.graph.add_edge(self.node_id, target_id, TYPE_KEY=target_node_type.edge_type_key)
        else:
            pass

    @staticmethod
    def get_node_by_code(code: str, type_key: t.Any, graph: nx.Graph, schema: Schema, create: bool = False) -> \
            t.Optional[Node]:
        node_type = schema.get_node_type(type_key)
        node_id = node_type.get_id_from_code(code)
        node = graph.nodes.get(node_id)
        if node is None and create:
            graph.add_node(node_id)
            node = graph.nodes.get(node_id)

        return Node(node_type, node_id, graph)


class Edge(Element):
    def __init__(self, edge_type_key: t.Any, from_node_id: str, to_node_id: str, edge_key: int, graph: nx.MultiDiGraph):
        super().__init__(node_id=from_node_id, graph=graph)
        self.to_node_id = to_node_id
        self.edge_type_key = edge_type_key
        self.edge_key = edge_key


    def set_property(self, *, property_key: t.Any, value: t.Any) -> Edge:
        self.graph.edges[self.from_node_id, self.to_node_id, self.edge_key][property_key] = value
        return self

    def get_property(self, property_: t.Any) -> t.Any:
        return self.graph.edges[self.from_node_id, self.to_node_id, self.edge_key]
