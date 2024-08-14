from enum import StrEnum

from loinclib.schema_v2 import Schema, NodeType, Property, EdgeType


class LoincNodes(StrEnum):
    LoincTerm = 'LoincTerm'
    LoincPart = 'LoincPart'


class LoincTermEdges(StrEnum):
    primary_component = 'primary_component'
    primary_property = 'primary_property'
    primary_time_aspect = 'primary_time_aspect'
    primary_system = 'primary_system'
    primary_scale_type = 'primary_scale_type'
    primary_method_type = 'primary_method_type'


class LoincTermProps(StrEnum):
    loinc_number = 'loinc_number'
    long_common_name = 'long_common_name'
    formal_name = 'formal_name'
    short_name = 'short_name'
    class_ = 'class'
    class_type = 'class_type'


class LoincPartEdges(StrEnum):
    sub_class_of = 'sub_class_of'


class LoincPartProps(StrEnum):
    part_number = 'part_number'
    part_type_name = 'part_type_name'
    part_name = 'part_name'
    part_display_name = 'part_display_name'


loinc_schema: Schema = Schema()

loinc_term = NodeType(type_key=LoincNodes.LoincTerm,
                      schema=loinc_schema,
                      base_url='https://loinc.org/',
                      url_regex=r'^https?://loinc.org/(P<code>\d+-\d)$',
                      curie_prefix='loinc')

loinc_schema.add_node_type(node_type=loinc_term)

# properties
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincTermProps.loinc_number))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincTermProps.long_common_name))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincTermProps.formal_name))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincTermProps.short_name))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincTermProps.class_))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincTermProps.class_type))

# edges
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincTermEdges.primary_component))
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincTermEdges.primary_property))
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincTermEdges.primary_time_aspect))
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincTermEdges.primary_system))
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincTermEdges.primary_scale_type))
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincTermEdges.primary_method_type))


loinc_part = NodeType(type_key=LoincNodes.LoincPart,
                      schema=loinc_schema,
                      base_url='https://loinc.org/',
                      url_regex=r'^https?://loinc.org/(P<code>LP\d+-\d)$',
                      curie_prefix='loinc')
loinc_schema.add_node_type(node_type=loinc_part)

# properties
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincPartProps.part_number))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincPartProps.part_type_name))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincPartProps.part_name))
loinc_term.add_property(Property(node_type=loinc_term, type_key=LoincPartProps.part_display_name))

# edge
loinc_term.add_edge_type(EdgeType(node_type=loinc_term, edge_type_key=LoincPartEdges.sub_class_of))



