from enum import StrEnum
from pathlib import Path

import pandas as pd

import loinclib.loinc_schema_v2 as LS
from loinclib import LoinclibGraph
from loinclib.schema_v2 import Node


class LoincSources(StrEnum):
  LoincTable__LoincCsv = 'LoincTable/Loinc.csv'
  AccessoryFiles__PartFile__PartCsv = 'AccessoryFiles/PartFile/Part.csv'
  AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv = 'AccessoryFiles/PartFile/LoincPartLink_Primary.csv'
  AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv = 'AccessoryFiles/PartFile/LoincPartLink_Supplementary.csv'
  AccessoryFiles__PartFile__PartRelatedCodeMappingCsv = 'AccessoryFiles/PartFile/PartRelatedCodeMapping.csv'


class LoincReleaseLoader:

  def __init__(self, *, graph: LoinclibGraph, config, home_path: Path):
    self.graph = graph
    # self.runtime = runtime
    self.config = config
    self.home_path = home_path
    self.release_path = self.get_loinc_release_path()

  def load_loinc_table__loinc_csv(self) -> None:

    if LoincSources.LoincTable__LoincCsv in self.graph.loaded_sources:
      return

    for tpl in self.read_loinc_table__loinc_csv().itertuples():
      # @formatter:off
      (row_number,
       loinc_number,
       component,
       property_,
       time_aspect,
       system,
       scale_type,
       method_type,
       class_,
       version_last_changed,
       change_type, definition_description,
       status,
       consumer_name,
       class_type,
       formula,
       example_answers,
       survey_question_text,
       urvey_question_source,
       units_required,
       related_names_2,
       short_name,
       order_obs,
       hl7_field_subfield_id,
       external_copyright_notice,
       example_units,
       long_common_name,
       example_ucum_units,
       status_reason,
       status_text,
       change_reason_public,
       common_test_rank,
       common_order_rank,
       common_si_test_rank,
       hl7_attachement_structure,
       external_copyright_link,
       panel_type,
       ask_at_order_entry,
       associated_observations,
       version_first_released,
       valid_hl7_attachment_request,
       display_name) = tpl
      # @formatter:on

      node: Node = self.graph.getsert_node(type_=LS.LoincNodeType.LoincTerm, code=loinc_number)

      # properties
      node.set_property(type_=LS.LoincTermProps.loinc_number, value=loinc_number)
      node.set_property(type_=LS.LoincTermProps.long_common_name, value=long_common_name)
      node.set_property(type_=LS.LoincTermProps.class_, value=class_)
      node.set_property(type_=LS.LoincTermProps.definition_description, value=definition_description)
      node.set_property(type_=LS.LoincTermProps.class_type, value=class_type)

      # edges

    self.graph.loaded_sources[LoincSources.LoincTable__LoincCsv] = {}

  def load_accessory_files__part_file__part_csv(self) -> None:
    if LoincSources.AccessoryFiles__PartFile__PartCsv in self.graph.loaded_sources:
      return

    for tpl in self.read_accessory_files__part_file__part_csv().itertuples():
      # @formatter:off
      (row_number,
       part_number,
       part_type_name,
       part_name,
       part_display_name,
       status) = tpl
      # @formatter:on

      node: Node = self.graph.getsert_node(type_=LS.LoincNodeType.LoincPart, code=part_number)
      node.set_property(type_=LS.LoincPartProps.part_number, value=part_number)
      node.set_property(type_=LS.LoincPartProps.part_type_name, value=part_type_name)
      node.set_property(type_=LS.LoincPartProps.part_name, value=part_name)
      node.set_property(type_=LS.LoincPartProps.part_display_name, value=part_display_name)
      node.set_property(type_=LS.LoincPartProps.status, value=status)

    self.graph.loaded_sources[LoincSources.AccessoryFiles__PartFile__PartCsv] = {}

  def load_accessory_files__part_file__loinc_part_link_primary_csv(self) -> None:
    if LoincSources.AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv in self.graph.loaded_sources:
      return

    for tpl in self.read_accessory_files__part_file__loinc_part_link_primary_csv().itertuples():
      # @formatter:off
      (row_number,
       loinc_number,
       long_common_name,
       part_number,
       part_name,
       part_code_system,
       part_type_name,
       link_type_name,
       property_) = tpl
      # @formatter:off

      loinc_node: Node = self.graph.getsert_node(LS.LoincNodeType.LoincTerm, loinc_number)
      part_node: Node = self.graph.getsert_node(LS.LoincNodeType.LoincPart, part_number)
      loinc_node.add_edge_single(LS.LoincTermPrimaryEdges(property_),part_node,False)

    self.graph.loaded_sources[LoincSources.AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv] = {}


  def load_accessory_files__part_file__loinc_part_link_supplementary_csv(self) -> None:
    if LoincSources.AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv in self.graph.loaded_sources:
      return

    for tpl in self.read_accessory_files__part_file__loinc_part_link_supplementary_csv().itertuples():
      # @formatter:off
      (row_number,
       loinc_number,
       long_common_name,
       part_number,
       part_name,
       part_code_system,
       part_type_name,
       link_type_name,
       property_) = tpl
      # @formatter:off

      loinc_node: Node = self.graph.getsert_node(LS.LoincNodeType.LoincTerm, loinc_number)
      part_node: Node = self.graph.getsert_node(LS.LoincNodeType.LoincPart, part_number)
      loinc_node.add_edge_single(LS.LoincTermSupplementaryEdges(property_),part_node,False)

    self.graph.loaded_sources[LoincSources.AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv] = {}

  def read_loinc_table__loinc_csv(self) -> pd.DataFrame:
    return pd.read_csv(self.release_path / LoincSources.LoincTable__LoincCsv, dtype=str, na_filter=False)

  def read_accessory_files__part_file__part_csv(self) -> pd.DataFrame:
    return pd.read_csv(self.release_path / LoincSources.AccessoryFiles__PartFile__PartCsv, dtype=str, na_filter=False)

  def read_accessory_files__part_file__loinc_part_link_primary_csv(self) -> pd.DataFrame:
    return pd.read_csv(self.release_path / LoincSources.AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv, dtype=str,
                       na_filter=False)

  def read_accessory_files__part_file__loinc_part_link_supplementary_csv(self) -> pd.DataFrame:
    return pd.read_csv(self.release_path / LoincSources.AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv,
                       dtype=str, na_filter=False)

  def read_accessory_files__part_file__part_related_code_mapping_csv(self) -> pd.DataFrame:
    return pd.read_csv(self.release_path / LoincSources.AccessoryFiles__PartFile__PartRelatedCodeMappingCsv,
                       dtype=str, na_filter=False)

  def get_loinc_release_path(self):
    release_path = None
    if self.config:
      loinc = self.config.get('loinc', None)
      if loinc:
        release = loinc.get('release', None)
        if release:
          default_ver = release.get('default', None)
          if default_ver:
            loinc_ver = release.get(default_ver, None)
            if loinc_ver:
              loinc_ver_path = loinc_ver.get('path', None)
              if loinc_ver_path:
                release_path = self.home_path / loinc_ver_path

    if release_path is None:
      release_path = self.home_path / 'loinc_release'

    return release_path.absolute()