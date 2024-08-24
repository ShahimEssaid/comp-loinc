from enum import StrEnum
from pathlib import Path

import pandas as pd
import loinc_schema_v2 as LS

from loinclib.graph_v2 import LoinclibGraph
from loinclib.schema_v2 import Node


class LoincSources(StrEnum):
  LoincTable_LoincCsv = 'LoincTable/Loinc.csv'


class LoincLoader:

  def __init__(self, *,
      release_path: Path):
    self.release_path = release_path

  def load_loinc_table__loinc_csv(self, graph: LoinclibGraph) -> None:

    if LoincSources.LoincTable_LoincCsv in graph.loaded_sources:
      return

    for tpl in self.read_loinc_table__loinc_csv().itertuples():
      (row_number,
       loinc_number,  # done
       component,  # done
       property_,  # done
       time_aspect,
       system,
       scale_type,
       method_type,
       class_,  # done
       version_last_changed,  # Done
       change_type,
       definition_description,  # done
       status,  # done
       consumer_name,
       class_type,  # done
       formula,
       example_answers,
       survey_question_text,
       survey_question_source,
       units_required,
       related_names_2,
       short_name,  # done
       order_obs,
       hl7_field_subfield_id,
       external_copyright_notice,
       example_units,
       long_common_name,  # done
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
       version_first_released,  # done
       valid_hl7_attachement_request,
       display_name
       ) = tpl

      node: Node = graph.getsert_node(type_=LS.LoincNodeType.LoincTerm,
                                      code=loinc_number)

      # properties
      node.set_property(type_=LS.LoincTermProps.loinc_number,
                        value=loinc_number)
      node.set_property(type_=LS.LoincTermProps.long_common_name,
                        value=long_common_name)
      node.set_property(type_=LS.LoincTermProps.class_, value=class_)
      node.set_property(type_=LS.LoincTermProps.class_type, value=class_type)

      # edges

      graph.loaded_sources[LoincSources.LoincTable_LoincCsv] = {}

  def read_loinc_table__loinc_csv(self) -> pd.DataFrame:
    return pd.read_csv(self.release_path / 'LoincTable' / 'Loinc.csv',
                       dtype=str, na_filter=False)
