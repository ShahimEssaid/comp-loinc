import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from sssom.io import convert_file
from comp_loinc.ingest.source_data_utils import loincify
from .mapping_utils import build_context
from pathlib import Path
import os
import sys

path_root = Path(__file__).parents[3]
sys.path.append(str(path_root))

class Mappings(object):
    def __init__(self, user, pwd, output):
        self.fhir_endpoint = 'https://fhir.loinc.org'
        self.user = user
        self.pwd = pwd
        self.output = output

class ChebiFhirIngest(Mappings):
    def __init__(self, user, pwd, output):
        super().__init__(user, pwd, output)
        self.chebi_loinc_sssom = self.create_chebi_loinc_sssom()
        self.sssom_chebi_to_owl()
    def get_fhir_chebi_mappings(self):
        r = requests.get(f"{self.fhir_endpoint}/ConceptMap/?url=http://loinc.org/cm/loinc-parts-to-chebi",
                         auth=HTTPBasicAuth(self.user, self.pwd))
        return r.json()

    def create_chebi_loinc_sssom(self):
        chebi_context_map = build_context({"loinc": "https://loinc.org/"})
        chebi_loinc_fhir = self.get_fhir_chebi_mappings()
        part_mappings = chebi_loinc_fhir['entry'][0]['resource']['group'][0]['element']
        sssom_mappings = []
        for part_map in part_mappings:
            predicate_map = {
                "equivalent": 'skos:exactMatch',
                "relatedto": 'skos:relatedMatch'
            }
            sssom_obj = dict()

            sssom_obj['subject_id'] = loincify(part_map['code'])
            sssom_obj['predicate_id'] = predicate_map[part_map['target'][0]['equivalence']]
            sssom_obj['object_id'] = part_map['target'][0]['code']
            sssom_obj['object_label'] = part_map['target'][0]['display']
            sssom_obj['mapping_justification'] = "sempav:HumanCuration"
            sssom_mappings.append(sssom_obj)
        l2c_df = pd.DataFrame(sssom_mappings)

        with open(f"{path_root}/data/output/sssom_mapping_files/loinc2chebi.tsv", 'w') as lc:
            lc.write(chebi_context_map)
            l2c_df.to_csv(lc, sep="\t", index=False)

    def sssom_chebi_to_owl(self):
        with open(f"{path_root}/data/output/owl_component_files/{self.output}", 'w') as l2co:
            convert_file(f"{path_root}/data/output/sssom_mapping_files/loinc2chebi.tsv", output=l2co, output_format='owl')
