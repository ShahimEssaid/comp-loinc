from enum import StrEnum

import pandas as pd

from loinclib import LoinclibGraph, Node, Configuration
from loinclib.snomed_schema_v2 import SnomedNodeType, SnomedEdges


class SnomedSources(StrEnum):
  relations = 'relations'


class SnomedReleaseLoader:

  def __init__(self, *, graph: LoinclibGraph, config: Configuration):
    self.config = config
    self.graph = graph

  def read_relationship(self) -> pd.DataFrame:
    return pd.read_csv(self.config.get_snomed_relations_path(), dtype=str, na_filter=False, sep='\t')

  def load_selected_relations(self, *types_: StrEnum) -> None:

    loaded_relationships = self.graph.loaded_sources.get(SnomedSources.relations, {})
    new_relationships = False
    for type_ in types_:
      if type_ not in loaded_relationships:
        new_relationships = True

    if not new_relationships:
      return

    for tpl in self.read_relationship().itertuples():
      # @formatter:off
      (
       index,
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

      if type_ in loaded_relationships:
        continue

      if type_ in types_:
        from_node: Node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=source_id)
        to_node: Node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=destination_id)
        from_node.add_edge_single(type_, to_node=to_node, error_if_duplicate=False)

    for type_ in types_:
      loaded_relationships[type_] = True
