from enum import StrEnum
from pathlib import Path

import pandas as pd

from loinclib import LoinclibGraph, Node
from loinclib.snomed_schema_v2 import SnomedNodeType, SnomedEdges


class SnomedSources(StrEnum):
  relations = 'relations'


class SnomedReleaseLoader:
  # def __init__(self, config, home_path: Path):
  def __init__(self, *, graph: LoinclibGraph, config, home_path: Path):
    self.config = config
    self.home_path = home_path
    self.graph = graph

  def get_relations_path(self) -> Path:
    release_version = self.config['snomed']['release']['default']
    relationship_path = self.config['snomed']['release'][release_version]['files']['relationship']
    return (self.home_path / relationship_path).absolute()

  def read_relations_tsv(self) -> pd.DataFrame:
    # with open(self.get_relations_path(), 'r') as f:
    #   return pd.read_csv(f, dtype=str, na_filter=False, sep='\t')
    return pd.read_csv(self.get_relations_path(), dtype=str, na_filter=False, sep='\t')

  def load_relations_tsv(self) -> None:
    if SnomedSources.relations in self.graph.loaded_sources:
      return

    for tpl in self.read_relations_tsv().itertuples():
      # @formatter:off
      (
        row_number,
       id_,
       effective_time,
       active,
       module_id,
       source_id,
       destination_id,
       # relationship_id,
       relationship_group,
       type_id,
       characteristic_type_id,
       modifier_id,
       ) = tpl
      # @formatter:on


      type_ = None
      try:
        type_ = SnomedEdges(type_id)
      except ValueError:
        pass
      if type_:
        from_node: Node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=source_id)
        to_node: Node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=destination_id)
        from_node.add_edge_single(SnomedEdges(type_id), to_node=to_node, error_if_duplicate=False)


    self.graph.loaded_sources[SnomedSources.relations] = {}
