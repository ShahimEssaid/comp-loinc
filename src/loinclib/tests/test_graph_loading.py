from pathlib import Path
from unittest import TestCase

from comp_loinc import Runtime
from loinclib.loinc_release_loader_v2 import LoincReleaseLoader
from loinclib.loinc_schema_v2 import LoincNodeType
from loinclib import SnomedReleaseLoader, SnomedNodeType

LOINC_PATH = Path('loinc_release/2.67')
TREE_PATH = Path('loinc_trees/2023-09-26')


class TestLoading(TestCase):

  def test_load_loinc_table(self):
    pass

  def test_load_primary(self):
    runtime = Runtime()
    loinc_loader = LoincReleaseLoader(config=runtime.config, graph=runtime.graph, home_path=runtime.home_path)
    loinc_loader.load_accessory_files__part_file__loinc_part_link_primary_csv()
    loinc_loader.load_accessory_files__part_file__loinc_part_link_supplementary_csv()

    node = runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code='100021-5')

    for edge in node.get_all_out_edges():
      print(edge)

    print(runtime)

  def test_load_snomed(self):
    runtime = Runtime()
    snomed_loader = SnomedReleaseLoader(config=runtime.config, home_path=runtime.home_path, graph=runtime.graph)
    # snomed_loader.read_relations_tsv()
    snomed_loader.load_relations_tsv()

    node = runtime.graph.get_node_by_code(type_=SnomedNodeType.Concept, code='237334005')
    for edge in node.get_all_out_edges():
      print(edge)

    print('done')
