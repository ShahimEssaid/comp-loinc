import typing as t
from pathlib import Path

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
        self.graph = Graph(graph=graph,
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
