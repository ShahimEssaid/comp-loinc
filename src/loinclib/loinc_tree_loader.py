from enum import StrEnum

import pandas as pd
from pandas import DataFrame

from loinclib import LoinclibGraph
from loinclib.loinc_schema import LoincNodeType
from loinclib.loinc_tree_schema import LoincTreeEdges, LoincTreeProps


class LoincTreeSource(StrEnum):
  class_tree = 'class.csv'
  component_tree = 'component.csv'
  component_by_system_tree = 'component_by_system.csv'
  document_tree = 'document.csv'
  method_tree = 'method.csv'
  panel_tree = 'panel.csv'
  system_tree = 'system.csv'


class LoincTreeLoader:
  def __init__(self, config, graph: LoinclibGraph):
    self.config = config
    self.graph = graph

  def load_class_tree(self):
    self.load_tree(LoincTreeSource.class_tree)

  def load_component_tree(self):
    self.load_tree(LoincTreeSource.component_tree)

  def load_component_by_system_tree(self):
    self.load_tree(LoincTreeSource.component_by_system_tree)

  def load_document_tree(self):
    self.load_tree(LoincTreeSource.document_tree)

  def load_method_tree(self):
    self.load_tree(LoincTreeSource.method_tree)

  def load_panel_tree(self):
    self.load_tree(LoincTreeSource.panel_tree)

  def load_system_tree(self):
    self.load_tree(LoincTreeSource.system_tree)

  def load_tree(self, source: LoincTreeSource):
    if source in self.graph.loaded_sources:
      return

    dataframe = self.read_source(source)

    records_by_id = {}
    for tpl in dataframe.itertuples():
      # @formatter:off
      (
        row_num,
        id_,
        parent_id,
        level,
        code,
        sequence,
        code_text,
        component,
        property_,
        timing,
        system,
        scale,
        method
      ) = tpl
      # @formatter:on
      records_by_id[id_] = (parent_id, code, code_text)

    for parent_id, code, code_text in records_by_id.values():
      if code.startswith('LP') and parent_id:
        part_node = self.graph.getsert_node(LoincNodeType.LoincPart, code)
        part_node.set_property(type_=LoincTreeProps.code_text, value=code_text)

        parent_node = self.graph.getsert_node(LoincNodeType.LoincPart, records_by_id[parent_id][1])
        part_node.add_edge_single(type_=LoincTreeEdges.tree_parent, to_node=parent_node)

    self.graph.loaded_sources[source] = {}
    pass

  def read_source(self, source: LoincTreeSource) -> DataFrame:
    path = self.config.get_trees_path() / source.value
    return pd.read_csv(path, dtype=str, na_filter=False)
