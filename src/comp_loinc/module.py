import typing as t
import datamodel.comp_loinc_v2 as v2
from pathlib import Path
from loinclib.loinc_graph_schema import PropertyType as PT

import networkx as nx

import datamodel.comp_loinc_v2 as v2
from loinclib import Graph


class Modules:
    def __init__(self, *,
                 graph: nx.MultiDiGraph = nx.MultiDiGraph(),
                 release_path: Path,
                 tree_path: Path = None,
                 loinc_version: str = None,
                 ):
        self.module_map: t.Dict[str, Module] = dict()
        self.graph: Graph = Graph(graph=graph,
                                  release_path=release_path,
                                  trees_path=tree_path,
                                  loinc_version=loinc_version,
                                  )


class Module:
    def __init__(self, *,
                 name: str,
                 modules: Modules
                 ):
        self.name = name
        self.modules = modules
        self.entities: t.Dict[str, v2.Entity] = dict()

        # flags for what to include
        self._include_loinc_long_common_name = None

    def create_loinc_terms_all(self):
        pass

    def add_entity(self, entity: v2.Entity):
        self.__do_includes(entity)

    def include_loinc_term_long_common_names(self):
        if self._include_loinc_long_common_name:
            return
        self._include_loinc_long_common_name = True
        for loinc_term in self.entities.values():
            self.__do_includes(loinc_term)

    def __do_includes(self, entity: v2.Entity):
        if isinstance(entity, v2.LoincTerm):
            self.__add_loinc_term_long_common_name(entity)

    def __add_loinc_term_long_common_name(self, loinc_term: v2.LoincTerm):
        if not self._include_loinc_long_common_name:
            return
        name = self.modules.graph.get_first_node_property(property_key=PT.loinc_long_common_name)
        loinc_term.long_common_name = name
