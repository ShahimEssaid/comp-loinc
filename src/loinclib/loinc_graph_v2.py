from pathlib import Path

import networkx as nx
import pandas as pd




class LoincGraph:
    def __init__(self, *,
                 release_path: Path,
                 loinc_version: str,
                 trees_path: Path,
                 graph: nx.MultiDiGraph = nx.MultiDiGraph(),
                 ):
        self.release_path: Path = release_path
        self.trees_path: Path = trees_path
        self.loinc_version: str = loinc_version
        self.graph: nx.MultiDiGraph = graph
        self.loaded_sources = self.graph.graph.setdefault('loaded_sources', {})


    def load_LoincTable_Loinc_csv(self) -> None:
        if 'LoincTable/Loinc.csv' in self.loaded_sources:
            return
        for tpl in self.read_LoincTable_Loinc_csv().itertuples():
            (row_number,
             loinc_number,  # done
             component,  # done
             _property,  # done
             time_aspect,
             system,
             scale_type,
             method_type,
             _class,  # done
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

        pass


    def read_LoincTable_Loinc_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.release_path / 'LoincTable' / 'Loinc.csv', dtype=str, na_filter=False)