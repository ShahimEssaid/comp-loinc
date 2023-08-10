from __future__ import annotations

import re
from enum import Enum


class NodeType(str, Enum):
    loinc_part = 'LPart'
    loinc_code = 'LCode'
    special = 'Special'

    def node_id_of_identifier(self, identifier: str) -> str:
        return f'{self.value}{{{identifier}}}'

    def identifier_of_node_id(self, node_id):
        match = re.match(f'{self.value}{{(.+)}}', node_id)
        if match:
            return match.group(1)
        else:
            raise ValueError(f'Failed to extract identifier from node id: {node_id}')

    def is_type(self, node_id: str) -> bool:
        if re.match(f'{self.value}{{.+}}', node_id):
            return True
        return False

    @classmethod
    def type_for_identifier(cls, identifier: str) -> NodeType:
        if re.match(r'^LP\d+-\d$', identifier):
            return NodeType.loinc_part
        elif re.search(r'^\d+-\d$', identifier):
            return NodeType.loinc_code
        else:
            raise ValueError(f'Identifier: {identifier} did not match a NodeType enum value.')

    @classmethod
    def type_for_node_id(cls, node_id: str) -> NodeType:
        if re.match(r'^LPart{LP\d+-\d}$', node_id):
            return NodeType.loinc_part
        elif re.search(r'^LCode{\d+-\d}$', node_id):
            return NodeType.loinc_code
        else:
            raise ValueError(f'Node id: {node_id} did not match a NodeType enum value.')


class AttributeType(str, Enum):
    graph_entity_type = 'graph-entity-type'


class EdgeAttributeKey(str, Enum):
    pass
    # edge_type = 'edge type'


class LoincAttributeType(str, Enum):
    """Attribute keys/names for LOINC values"""

    code = 'code'
    """The actual LOINC code (any code), or the identifier for what this node is about"""

    display = 'display'
    """
    This is the main label for a LOINC entity.

    For parts: an alternate display name for the Part, which is often used to create the LOINC Long Common Name
    """

    status = 'status'
    """The status of the entity."""

    definition = 'definition'

    # parts file based attributes
    part_name = 'part name'
    part_display_name = 'part display name'
    part_type = 'part type'

    # Tree file attributes
    tree_code_text = 'tree code text'

    # loinc attributes
    loinc_long_common_name = 'loinc long common name'
    loinc_short_name = 'loinc short name'
    loinc_definition = 'loinc definition'
    loinc_component = 'loinc component'
    loinc_property = 'loinc property'
    loinc_time_aspect = 'loinc time aspect'
    loinc_system = 'loinc system'
    loinc_scale_type = 'loinc scale type'
    loinc_method_type = 'loinc method type'
    loinc_class = 'loinc class'
    loinc_class_type = 'loinc class type'
    loinc_version_first_released = 'loinc version first released'
    loinc_version_last_changed = 'loinc version last changed'


class EdgeType(Enum):
    LoincLib_HasParent = 'loinclib', 'has_parent', 'has_parent'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, group, name, uri):
        self.rel_group = group
        self.rel_name = name
        self.rel_uri = uri

    def __repr__(self):
        return f'{self.name}{{group:{self.rel_group}, name:{self.rel_name}, uri:{self.rel_uri}}}'

    def __str__(self):
        return self.__repr__()


class LoincEdgeType(Enum):
    # First part: Component/Analyte
    # ==========

    #  https://loinc.org/kb/enriched-linkages-between-loinc-terms-and-loinc-parts/#primary
    Primary_COMPONENT = 'Primary', 'COMPONENT', 'http://loinc.org/property/COMPONENT'

    # Sub parts:
    # https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#componentanalyte-1st-part
    # https://loinc.org/kb/users-guide/major-parts-of-a-loinc-term/#distinguishing-multiple-values-for-any-test-via-the-test-name-4th-subpart
    # https://loinc.org/kb/enriched-linkages-between-loinc-terms-and-loinc-parts/#detailedmodel
    DetailedModel_COMPONENT_analyte = 'DetailedModel', 'COMPONENT', 'http://loinc.org/property/analyte'
    DetailedModel_CHALLENGE_challenge = 'DetailedModel', 'CHALLENGE', 'http://loinc.org/property/challenge'
    DetailedModel_ADJUSTMENT_adjustment = 'DetailedModel', 'ADJUSTMENT', 'http://loinc.org/property/adjustment'
    DetailedModel_COUNT_count = 'DetailedModel', 'COUNT', 'http://loinc.org/property/count'

    # Second part: Property
    # ==========

    Primary_PROPERTY = 'Primary', 'PROPERTY', 'http://loinc.org/property/PROPERTY'

    DetailedModel_PROPERTY_PROPERTY = 'DetailedModel', 'PROPERTY', 'http://loinc.org/property/PROPERTY'

    # Time part:
    # ==========

    Primary_TIME = 'Primary', 'TIME', 'http://loinc.org/property/TIME_ASPCT'

    DetailedModel_TIME_time_core = 'DetailedModel', 'TIME', 'http://loinc.org/property/time-core'
    DetailedModel_TIME_MODIFIER_time_modifier = 'DetailedModel', 'TIME MODIFIER', 'http://loinc.org/property/time-modifier'

    # System part:
    # ==========

    Primary_SYSTEM = 'Primary', 'SYSTEM', 'http://loinc.org/property/SYSTEM'

    DetailedModel_SYSTEM_system_core = 'DetailedModel', 'SYSTEM', 'http://loinc.org/property/system-core'
    DetailedModel_SUPER_SYSTEM_super_system = 'DetailedModel', 'SUPER SYSTEM', 'http://loinc.org/property/super-system'

    # Scale part:
    # ==========

    Primary_SCALE = 'Primary', 'SCALE', 'http://loinc.org/property/SCALE_TYP'
    DetailedModel_SCALE_SCALE_TYP = 'DetailedModel', 'SCALE', 'http://loinc.org/property/SCALE_TYP'

    # Method part:
    # ==========

    Primary_METHOD = 'Primary', 'METHOD', 'http://loinc.org/property/METHOD_TYP'

    DetailedModel_METHOD_METHOD_TYP = 'DetailedModel', 'METHOD', 'http://loinc.org/property/METHOD_TYP'

    # Document

    DocumentOntology_Document_Kind = 'DocumentOntology', 'Document.Kind', 'http://loinc.org/property/document-kind'
    DocumentOntology_Document_Role = 'DocumentOntology', 'Document.Role', 'http://loinc.org/property/document-role'
    DocumentOntology_Document_Setting = 'DocumentOntology', 'Document.Setting', 'http://loinc.org/property/document-setting'
    DocumentOntology_Document_SubjectMatterDomain = 'DocumentOntology', 'Document.SubjectMatterDomain', 'http://loinc.org/property/document-subject-matter-domain'
    DocumentOntology_Document_TypeOfService = 'DocumentOntology', 'Document.TypeOfService', 'http://loinc.org/property/document-type-of-service'

    # Radiology

    Radiology_Rad_Anatomic_Location_Imaging_Focus = 'Radiology', 'Rad.Anatomic Location.Imaging Focus', 'http://loinc.org/property/rad-anatomic-location-imaging-focus'
    Radiology_Rad_Anatomic_Location_Laterality = 'Radiology', 'Rad.Anatomic Location.Laterality', 'http://loinc.org/property/rad-anatomic-location-laterality'
    Radiology_Rad_Anatomic_Location_Laterality_Presence = 'Radiology', 'Rad.Anatomic Location.Laterality.Presence', 'http://loinc.org/property/rad-anatomic-location-laterality-presence'
    Radiology_Rad_Anatomic_Location_Region_Imaged = 'Radiology', 'Rad.Anatomic Location.Region Imaged', 'http://loinc.org/property/rad-anatomic-location-region-imaged'
    Radiology_Rad_Guidance_for_Action = 'Radiology', 'Rad.Guidance for.Action', 'http://loinc.org/property/rad-guidance-for-action'
    Radiology_Rad_Guidance_for_Approach = 'Radiology', 'Rad.Guidance for.Approach', 'http://loinc.org/property/rad-guidance-for-approach'
    Radiology_Rad_Guidance_for_Object = 'Radiology', 'Rad.Guidance for.Object', 'http://loinc.org/property/rad-guidance-for-object'
    Radiology_Rad_Guidance_for_Presence = 'Radiology', 'Rad.Guidance for.Presence', 'http://loinc.org/property/rad-guidance-for-presence'
    Radiology_Rad_Maneuver_Maneuver_Type = 'Radiology', 'Rad.Maneuver.Maneuver Type', 'http://loinc.org/property/rad-maneuver-maneuver-type'
    Radiology_Rad_Modality_Modality_Subtype = 'Radiology', 'Rad.Modality.Modality Subtype', 'http://loinc.org/property/rad-modality-subtype'
    Radiology_Rad_Modality_Modality_Type = 'Radiology', 'Rad.Modality.Modality Type', 'http://loinc.org/property/rad-modality-type'
    Radiology_Rad_Pharmaceutical_Route = 'Radiology', 'Rad.Pharmaceutical.Route', 'http://loinc.org/property/rad-pharmaceutical-route'
    Radiology_Rad_Pharmaceutical_Substance_Given = 'Radiology', 'Rad.Pharmaceutical.Substance Given', 'http://loinc.org/property/rad-pharmaceutical-substance-given'
    Radiology_Rad_Reason_for_Exam = 'Radiology', 'Rad.Reason for Exam', 'http://loinc.org/property/rad-reason-for-exam'
    Radiology_Rad_Subject = 'Radiology', 'Rad.Subject', 'http://loinc.org/property/rad-subject'
    Radiology_Rad_Timing = 'Radiology', 'Rad.Timing', 'http://loinc.org/property/rad-timing'
    Radiology_Rad_View_Aggregation = 'Radiology', 'Rad.View.Aggregation', 'http://loinc.org/property/rad-view-aggregation'
    Radiology_Rad_View_View_Type = 'Radiology', 'Rad.View.View Type', 'http://loinc.org/property/rad-view-view-type'

    # Other
    Metadata_CLASS_CLASS = 'Metadata', 'CLASS', 'http://loinc.org/property/CLASS'
    Metadata_CLASS_category = 'Metadata', 'CLASS', 'http://loinc.org/property/category'
    Search_CHALLENGE_search = 'Search', 'CHALLENGE', 'http://loinc.org/property/search'
    Search_COMPONENT_search = 'Search', 'COMPONENT', 'http://loinc.org/property/search'
    Search_METHOD_search = 'Search', 'METHOD', 'http://loinc.org/property/search'
    Search_SUPER_SYSTEM_search = 'Search', 'SUPER SYSTEM', 'http://loinc.org/property/search'
    Search_SYSTEM_search = 'Search', 'SYSTEM', 'http://loinc.org/property/search'
    SemanticEnhancement_GENE_analyte_gene = 'SemanticEnhancement', 'GENE', 'http://loinc.org/property/analyte-gene'
    SyntaxEnhancement_COMPONENT_analyte_core = 'SyntaxEnhancement', 'COMPONENT', 'http://loinc.org/property/analyte-core'
    SyntaxEnhancement_DIVISOR_analyte_divisor = 'SyntaxEnhancement', 'DIVISOR', 'http://loinc.org/property/analyte-divisor'
    SyntaxEnhancement_NUMERATOR_analyte_numerator = 'SyntaxEnhancement', 'NUMERATOR', 'http://loinc.org/property/analyte-numerator'
    SyntaxEnhancement_SUFFIX_analyte_divisor_suffix = 'SyntaxEnhancement', 'SUFFIX', 'http://loinc.org/property/analyte-divisor-suffix'
    SyntaxEnhancement_SUFFIX_analyte_suffix = 'SyntaxEnhancement', 'SUFFIX', 'http://loinc.org/property/analyte-suffix'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, group, name, uri):
        self.edge_group = group
        self.edge_name = name
        self.edge_uri = uri

    def __repr__(self):
        return f'LoincEdge:{{group:{self.edge_group}, name:{self.edge_name}, uri:{self.edge_uri}}}'

    def __str__(self):
        return self.__repr__()

    @classmethod
    def type_of(cls, /, *, group, name, uri):
        for edgeType in LoincEdgeType:
            if edgeType.edge_group == group and edgeType.edge_name == name and edgeType.edge_uri == uri:
                return edgeType
        raise ValueError(f'Unable to find LoincEdgeType for group: {{{group}}}, name: {{{name}}}, uri: {{{uri}}}')


# class SpecialNodeNames(str, Enum):
#     ratio_or_fraction = '_ratio_or_fraction'
#
#     @classmethod
#     def has_value(cls, value):
#         return value in cls._value2member_map_

# class LoincPrimaryEdgeType(Enum):
#     # Generate from rel-primary.py script
#     DocumentOntology_Document_Kind = 'DocumentOntology', 'Document.Kind', 'http://loinc.org/property/document-kind'
#     DocumentOntology_Document_Role = 'DocumentOntology', 'Document.Role', 'http://loinc.org/property/document-role'
#     DocumentOntology_Document_Setting = 'DocumentOntology', 'Document.Setting', 'http://loinc.org/property/document-setting'
#     DocumentOntology_Document_SubjectMatterDomain = 'DocumentOntology', 'Document.SubjectMatterDomain', 'http://loinc.org/property/document-subject-matter-domain'
#     DocumentOntology_Document_TypeOfService = 'DocumentOntology', 'Document.TypeOfService', 'http://loinc.org/property/document-type-of-service'
#     Primary_COMPONENT = 'Primary', 'COMPONENT', 'http://loinc.org/property/COMPONENT'
#     Primary_METHOD = 'Primary', 'METHOD', 'http://loinc.org/property/METHOD_TYP'
#     Primary_PROPERTY = 'Primary', 'PROPERTY', 'http://loinc.org/property/PROPERTY'
#     Primary_SCALE = 'Primary', 'SCALE', 'http://loinc.org/property/SCALE_TYP'
#     Primary_SYSTEM = 'Primary', 'SYSTEM', 'http://loinc.org/property/SYSTEM'
#     Primary_TIME = 'Primary', 'TIME', 'http://loinc.org/property/TIME_ASPCT'
#     Radiology_Rad_Anatomic_Location_Imaging_Focus = 'Radiology', 'Rad.Anatomic Location.Imaging Focus', 'http://loinc.org/property/rad-anatomic-location-imaging-focus'
#     Radiology_Rad_Anatomic_Location_Laterality = 'Radiology', 'Rad.Anatomic Location.Laterality', 'http://loinc.org/property/rad-anatomic-location-laterality'
#     Radiology_Rad_Anatomic_Location_Laterality_Presence = 'Radiology', 'Rad.Anatomic Location.Laterality.Presence', 'http://loinc.org/property/rad-anatomic-location-laterality-presence'
#     Radiology_Rad_Anatomic_Location_Region_Imaged = 'Radiology', 'Rad.Anatomic Location.Region Imaged', 'http://loinc.org/property/rad-anatomic-location-region-imaged'
#     Radiology_Rad_Guidance_for_Action = 'Radiology', 'Rad.Guidance for.Action', 'http://loinc.org/property/rad-guidance-for-action'
#     Radiology_Rad_Guidance_for_Approach = 'Radiology', 'Rad.Guidance for.Approach', 'http://loinc.org/property/rad-guidance-for-approach'
#     Radiology_Rad_Guidance_for_Object = 'Radiology', 'Rad.Guidance for.Object', 'http://loinc.org/property/rad-guidance-for-object'
#     Radiology_Rad_Guidance_for_Presence = 'Radiology', 'Rad.Guidance for.Presence', 'http://loinc.org/property/rad-guidance-for-presence'
#     Radiology_Rad_Maneuver_Maneuver_Type = 'Radiology', 'Rad.Maneuver.Maneuver Type', 'http://loinc.org/property/rad-maneuver-maneuver-type'
#     Radiology_Rad_Modality_Modality_Subtype = 'Radiology', 'Rad.Modality.Modality Subtype', 'http://loinc.org/property/rad-modality-subtype'
#     Radiology_Rad_Modality_Modality_Type = 'Radiology', 'Rad.Modality.Modality Type', 'http://loinc.org/property/rad-modality-type'
#     Radiology_Rad_Pharmaceutical_Route = 'Radiology', 'Rad.Pharmaceutical.Route', 'http://loinc.org/property/rad-pharmaceutical-route'
#     Radiology_Rad_Pharmaceutical_Substance_Given = 'Radiology', 'Rad.Pharmaceutical.Substance Given', 'http://loinc.org/property/rad-pharmaceutical-substance-given'
#     Radiology_Rad_Reason_for_Exam = 'Radiology', 'Rad.Reason for Exam', 'http://loinc.org/property/rad-reason-for-exam'
#     Radiology_Rad_Subject = 'Radiology', 'Rad.Subject', 'http://loinc.org/property/rad-subject'
#     Radiology_Rad_Timing = 'Radiology', 'Rad.Timing', 'http://loinc.org/property/rad-timing'
#     Radiology_Rad_View_Aggregation = 'Radiology', 'Rad.View.Aggregation', 'http://loinc.org/property/rad-view-aggregation'
#     Radiology_Rad_View_View_Type = 'Radiology', 'Rad.View.View Type', 'http://loinc.org/property/rad-view-view-type'
#
#
#
#     def __new__(cls, *args, **kwds):
#         value = len(cls.__members__) + 1
#         obj = object.__new__(cls)
#         obj._value_ = value
#         return obj
#
#     def __init__(self, group, name, uri):
#         self.rel_group = group
#         self.rel_name = name
#         self.rel_uri = uri
#
#     def __repr__(self):
#         return f'{self.name}{{group:{self.rel_group}, name:{self.rel_name}, uri:{self.rel_uri}}}'
#
#     def __str__(self):
#         return self.__repr__()
#
#     @classmethod
#     def type_of(cls, property_uri: str):
#         for t in LoincPrimaryEdgeType:
#             if t.rel_uri == property_uri:
#                 return t
#         raise ValueError(f'Unable to find LoincPrimaryEdgeType for url: {property_uri}')


# class LoincSupplementaryEdgeType(Enum):
#     DetailedModel_ADJUSTMENT_adjustment = 'DetailedModel', 'ADJUSTMENT', 'http://loinc.org/property/adjustment'
#     DetailedModel_CHALLENGE_challenge = 'DetailedModel', 'CHALLENGE', 'http://loinc.org/property/challenge'
#     DetailedModel_COMPONENT_analyte = 'DetailedModel', 'COMPONENT', 'http://loinc.org/property/analyte'
#     DetailedModel_COUNT_count = 'DetailedModel', 'COUNT', 'http://loinc.org/property/count'
#     DetailedModel_METHOD_METHOD_TYP = 'DetailedModel', 'METHOD', 'http://loinc.org/property/METHOD_TYP'
#     DetailedModel_PROPERTY_PROPERTY = 'DetailedModel', 'PROPERTY', 'http://loinc.org/property/PROPERTY'
#     DetailedModel_SCALE_SCALE_TYP = 'DetailedModel', 'SCALE', 'http://loinc.org/property/SCALE_TYP'
#     DetailedModel_SUPER_SYSTEM_super_system = 'DetailedModel', 'SUPER SYSTEM', 'http://loinc.org/property/super-system'
#     DetailedModel_SYSTEM_system_core = 'DetailedModel', 'SYSTEM', 'http://loinc.org/property/system-core'
#     DetailedModel_TIME_MODIFIER_time_modifier = 'DetailedModel', 'TIME MODIFIER', 'http://loinc.org/property/time-modifier'
#     DetailedModel_TIME_time_core = 'DetailedModel', 'TIME', 'http://loinc.org/property/time-core'
#     Metadata_CLASS_CLASS = 'Metadata', 'CLASS', 'http://loinc.org/property/CLASS'
#     Metadata_CLASS_category = 'Metadata', 'CLASS', 'http://loinc.org/property/category'
#     Search_CHALLENGE_search = 'Search', 'CHALLENGE', 'http://loinc.org/property/search'
#     Search_COMPONENT_search = 'Search', 'COMPONENT', 'http://loinc.org/property/search'
#     Search_METHOD_search = 'Search', 'METHOD', 'http://loinc.org/property/search'
#     Search_SUPER_SYSTEM_search = 'Search', 'SUPER SYSTEM', 'http://loinc.org/property/search'
#     Search_SYSTEM_search = 'Search', 'SYSTEM', 'http://loinc.org/property/search'
#     SemanticEnhancement_GENE_analyte_gene = 'SemanticEnhancement', 'GENE', 'http://loinc.org/property/analyte-gene'
#     SyntaxEnhancement_COMPONENT_analyte_core = 'SyntaxEnhancement', 'COMPONENT', 'http://loinc.org/property/analyte-core'
#     SyntaxEnhancement_DIVISOR_analyte_divisor = 'SyntaxEnhancement', 'DIVISOR', 'http://loinc.org/property/analyte-divisor'
#     SyntaxEnhancement_NUMERATOR_analyte_numerator = 'SyntaxEnhancement', 'NUMERATOR', 'http://loinc.org/property/analyte-numerator'
#     SyntaxEnhancement_SUFFIX_analyte_divisor_suffix = 'SyntaxEnhancement', 'SUFFIX', 'http://loinc.org/property/analyte-divisor-suffix'
#     SyntaxEnhancement_SUFFIX_analyte_suffix = 'SyntaxEnhancement', 'SUFFIX', 'http://loinc.org/property/analyte-suffix'
#
#     def __new__(cls, *args, **kwds):
#         value = len(cls.__members__) + 1
#         obj = object.__new__(cls)
#         obj._value_ = value
#         return obj
#
#     def __init__(self, group, name, uri):
#         self.rel_group = group
#         self.rel_name = name
#         self.rel_uri = uri
#
#     def __repr__(self):
#         return f'{self.name}{{group:{self.rel_group}, name:{self.rel_name}, uri:{self.rel_uri}}}'
#
#     def __str__(self):
#         return self.__repr__()


# class NodePrefix(str, Enum):
#     loinc_code = 'LC:'
#     loinc_part = 'LP:'


if __name__ == '__main__':
    print(NodeType.loinc_part.name)
    print(NodeType.loinc_part.value)
