import unittest
from enum import StrEnum

from loinclib.graph_v2 import LoinclibGraph
from loinclib.loinc_schema_v2 import LoincNodeType, LoincTermProps


class GraphTests(unittest.TestCase):

  def test_graph_1(self):
    graph = LoinclibGraph()
    self.assertIsNotNone(graph)

    node_type = graph.schema.getsert_node_type(LoincNodeType.LoincTerm)
    self.assertIsNotNone(node_type)

    node = graph.getsert_node(type_=LoincNodeType.LoincTerm, code='123')
    node.set_property(type_=LoincTermProps.loinc_number, value='123')
    loinc_number = node.get_property(type_=LoincTermProps.loinc_number)
    self.assertEqual(loinc_number, '123')

    node.set_property(type_=LoincTermProps.loinc_number, value=None)
    self.assertNotIn(member=LoincTermProps.loinc_number, container=node.get_properties())




    print(node)


