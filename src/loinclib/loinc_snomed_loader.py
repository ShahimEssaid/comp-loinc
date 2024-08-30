from enum import StrEnum
from pathlib import Path

import pandas as pd

from loinclib import LoinclibGraph, SnomedNodeType, SnomedEdges
from loinclib.loinc_schema_v2 import LoincNodeType
from loinclib.snomed_schema_v2 import SnomedProperteis


class LoincSnomedSources(StrEnum):
  description = 'description'
  identifier = 'identifier'
  relation = 'relation'


class LoincSnomedLoader:
  def __init__(self, config, home_path: Path, graph: LoinclibGraph):
    self.home_path = home_path
    self.config = config
    self.graph = graph

  def get_description_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['description']
    return self.home_path / path

  def get_identifier_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['identifier']
    return self.home_path / path

  def get_relationship_path(self) -> Path:
    default = self.config['loinc_snomed']['release']['default']
    path = self.config['loinc_snomed']['release'][default]['files']['relationship']
    return self.home_path / path

  def read_description(self):
    return pd.read_csv(self.get_description_path(), dtype=str, na_filter=False, sep='\t')

  def read_identifiers(self):
    return pd.read_csv(self.get_identifier_path(), dtype=str, na_filter=False, sep='\t')

  def read_relationship(self):
    return pd.read_csv(self.get_relationship_path(), dtype=str, na_filter=False, sep='\t')

  def load_description(self):
    if LoincSnomedSources.description in self.graph.loaded_sources:
      return

    for tpl in self.read_description().itertuples():
      # @formatter:off
      (
      index,
      id_,
      effective_time,
      active,
      module_id,
      concept_id,
      language_code,
      type_id,
      term,
      case_significance_id
      ) = tpl
      # @formatter:on

      snomed_node = self.graph.getsert_node(SnomedNodeType.Concept, concept_id)
      snomed_node.set_property(type_=SnomedProperteis.fully_specified_name, value=term)


    self.graph.loaded_sources[LoincSnomedSources.description] = {}

  def load_identifier(self):
    if LoincSnomedSources.identifier in self.graph.loaded_sources:
      return

    for tpl in self.read_identifiers().itertuples():
      # @formatter:off
      (
        index,
        alternate_identifier, # loinc term code
        effective_time,
        active,
        module_id,
        identifier_schema_id,  # loinc
        referenced_component_id
      ) = tpl
      # @formatter:on

      loinc_node = self.graph.getsert_node(type_=LoincNodeType.LoincTerm, code=alternate_identifier)
      snomed_node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=referenced_component_id)
      loinc_node.add_edge_single(type_=SnomedEdges.maps_to, to_node=snomed_node)

    self.graph.loaded_sources[LoincSnomedSources.identifier] = {}

  def load_relationship(self):
    if LoincSnomedSources.relation in self.graph.loaded_sources:
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
        relationship_group,
        type_id,
        characteristic_type_id,
        modifier_id
      ) = tpl
      # @formatter:on


      from_node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=source_id)
      to_node = self.graph.getsert_node(type_=SnomedNodeType.Concept, code=destination_id)
      type_ = SnomedEdges(type_id)
      from_node.add_edge_single(type_=type_, to_node=to_node)


    self.graph.loaded_sources[LoincSnomedSources.relation] = {}
