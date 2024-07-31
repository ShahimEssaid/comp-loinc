# Auto generated from comp_loinc_v2.yaml by pythongen.py version: 0.9.0
# Generation date: 2024-07-30T13:31:52
# Schema: loinc-owl-core-schema
#
# id: https://loinc.org/core
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LOINC = CurieNamespace('loinc', 'https://loinc.org/')
LOINC_PROPERTY = CurieNamespace('loinc_property', 'http://loinc.org/property/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
DEFAULT_ = LOINC


# Types

# Class references



@dataclass
class Loinc(YAMLRoot):
    """
    A container of Loinc term and part instances.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Loinc"
    class_model_uri: ClassVar[URIRef] = LOINC.Loinc

    codes: Optional[Union[Union[dict, "LoincTerm"], List[Union[dict, "LoincTerm"]]]] = empty_list()
    parts: Optional[Union[Union[dict, "LoincPart"], List[Union[dict, "LoincPart"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.codes, list):
            self.codes = [self.codes] if self.codes is not None else []
        self.codes = [v if isinstance(v, LoincTerm) else LoincTerm(**as_dict(v)) for v in self.codes]

        if not isinstance(self.parts, list):
            self.parts = [self.parts] if self.parts is not None else []
        self.parts = [v if isinstance(v, LoincPart) else LoincPart(**as_dict(v)) for v in self.parts]

        super().__post_init__(**kwargs)


class Entity(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = LOINC.Entity


@dataclass
class LoincEntity(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC.LoincEntity
    class_class_curie: ClassVar[str] = "loinc:LoincEntity"
    class_name: ClassVar[str] = "LoincEntity"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincEntity

    loinc_number: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    subClassOf: Optional[Union[Union[dict, "LoincEntity"], List[Union[dict, "LoincEntity"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.loinc_number is not None and not isinstance(self.loinc_number, str):
            self.loinc_number = str(self.loinc_number)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, LoincEntity) else LoincEntity(**as_dict(v)) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class LoincTerm(LoincEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC.LoincTerm
    class_class_curie: ClassVar[str] = "loinc:LoincTerm"
    class_name: ClassVar[str] = "LoincTerm"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincTerm

    long_common_name: Optional[str] = None
    formal_name: Optional[str] = None
    short_name: Optional[str] = None
    status: Optional[str] = None
    loinc_class: Optional[str] = None
    loinc_class_type: Optional[str] = None
    primary_component: Optional[Union[dict, "LoincPart"]] = None
    primary_property: Optional[Union[dict, "LoincPart"]] = None
    primary_time_aspect: Optional[Union[dict, "LoincPart"]] = None
    primary_system: Optional[Union[dict, "LoincPart"]] = None
    primary_scale_typ: Optional[Union[dict, "LoincPart"]] = None
    primary_method_typ: Optional[Union[dict, "LoincPart"]] = None
    detailed_analyte: Optional[Union[dict, "LoincPart"]] = None
    detailed_challenge: Optional[Union[dict, "LoincPart"]] = None
    detailed_adjustment: Optional[Union[dict, "LoincPart"]] = None
    detailed_count: Optional[Union[dict, "LoincPart"]] = None
    detailed_time_core: Optional[Union[dict, "LoincPart"]] = None
    detailed_time_modifier: Optional[Union[dict, "LoincPart"]] = None
    detailed_system_core: Optional[Union[dict, "LoincPart"]] = None
    detailed_super_system: Optional[Union[dict, "LoincPart"]] = None
    syntax_analyte_core: Optional[Union[dict, "LoincPart"]] = None
    syntax_analyte_suffix: Optional[Union[dict, "LoincPart"]] = None
    syntax_analyte_numerator: Optional[Union[dict, "LoincPart"]] = None
    syntax_analyte_divisor: Optional[Union[dict, "LoincPart"]] = None
    syntax_analyte_divisor_suffix: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_gene: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_genetic_variant: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_chemical: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_divisor_chemical: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_clinical_drug: Optional[Union[dict, "LoincPart"]] = None
    semantic_system_core_anatomic_entity: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_organism: Optional[Union[dict, "LoincPart"]] = None
    semantic_challenge_route: Optional[Union[dict, "LoincPart"]] = None
    semantic_analyte_allergen: Optional[Union[dict, "LoincPart"]] = None
    metadata_class: Optional[Union[dict, "LoincPart"]] = None
    metadata_category: Optional[Union[dict, "LoincPart"]] = None
    rad_anatomic_location_imaging_focus: Optional[Union[dict, "LoincPart"]] = None
    rad_anatomic_location_laterality: Optional[Union[dict, "LoincPart"]] = None
    rad_anatomic_location_laterality_presence: Optional[Union[dict, "LoincPart"]] = None
    rad_anatomic_location_region_imaged: Optional[Union[dict, "LoincPart"]] = None
    rad_guidance_for_action: Optional[Union[dict, "LoincPart"]] = None
    rad_guidance_for_approach: Optional[Union[dict, "LoincPart"]] = None
    rad_guidance_for_object: Optional[Union[dict, "LoincPart"]] = None
    rad_guidance_for_presence: Optional[Union[dict, "LoincPart"]] = None
    rad_maneuver_maneuver_type: Optional[Union[dict, "LoincPart"]] = None
    rad_modality_subtype: Optional[Union[dict, "LoincPart"]] = None
    rad_modality_type: Optional[Union[dict, "LoincPart"]] = None
    rad_pharmaceutical_route: Optional[Union[dict, "LoincPart"]] = None
    rad_pharmaceutical_substance_given: Optional[Union[dict, "LoincPart"]] = None
    rad_reason_for_exam: Optional[Union[dict, "LoincPart"]] = None
    rad_subject: Optional[Union[dict, "LoincPart"]] = None
    rad_timing: Optional[Union[dict, "LoincPart"]] = None
    rad_view_aggregation: Optional[Union[dict, "LoincPart"]] = None
    rad_view_view_type: Optional[Union[dict, "LoincPart"]] = None
    document_kind: Optional[Union[dict, "LoincPart"]] = None
    document_role: Optional[Union[dict, "LoincPart"]] = None
    document_setting: Optional[Union[dict, "LoincPart"]] = None
    document_subject_matter_domain: Optional[Union[dict, "LoincPart"]] = None
    document_type_of_service: Optional[Union[dict, "LoincPart"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.long_common_name is not None and not isinstance(self.long_common_name, str):
            self.long_common_name = str(self.long_common_name)

        if self.formal_name is not None and not isinstance(self.formal_name, str):
            self.formal_name = str(self.formal_name)

        if self.short_name is not None and not isinstance(self.short_name, str):
            self.short_name = str(self.short_name)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.loinc_class is not None and not isinstance(self.loinc_class, str):
            self.loinc_class = str(self.loinc_class)

        if self.loinc_class_type is not None and not isinstance(self.loinc_class_type, str):
            self.loinc_class_type = str(self.loinc_class_type)

        if self.primary_component is not None and not isinstance(self.primary_component, LoincPart):
            self.primary_component = LoincPart(**as_dict(self.primary_component))

        if self.primary_property is not None and not isinstance(self.primary_property, LoincPart):
            self.primary_property = LoincPart(**as_dict(self.primary_property))

        if self.primary_time_aspect is not None and not isinstance(self.primary_time_aspect, LoincPart):
            self.primary_time_aspect = LoincPart(**as_dict(self.primary_time_aspect))

        if self.primary_system is not None and not isinstance(self.primary_system, LoincPart):
            self.primary_system = LoincPart(**as_dict(self.primary_system))

        if self.primary_scale_typ is not None and not isinstance(self.primary_scale_typ, LoincPart):
            self.primary_scale_typ = LoincPart(**as_dict(self.primary_scale_typ))

        if self.primary_method_typ is not None and not isinstance(self.primary_method_typ, LoincPart):
            self.primary_method_typ = LoincPart(**as_dict(self.primary_method_typ))

        if self.detailed_analyte is not None and not isinstance(self.detailed_analyte, LoincPart):
            self.detailed_analyte = LoincPart(**as_dict(self.detailed_analyte))

        if self.detailed_challenge is not None and not isinstance(self.detailed_challenge, LoincPart):
            self.detailed_challenge = LoincPart(**as_dict(self.detailed_challenge))

        if self.detailed_adjustment is not None and not isinstance(self.detailed_adjustment, LoincPart):
            self.detailed_adjustment = LoincPart(**as_dict(self.detailed_adjustment))

        if self.detailed_count is not None and not isinstance(self.detailed_count, LoincPart):
            self.detailed_count = LoincPart(**as_dict(self.detailed_count))

        if self.detailed_time_core is not None and not isinstance(self.detailed_time_core, LoincPart):
            self.detailed_time_core = LoincPart(**as_dict(self.detailed_time_core))

        if self.detailed_time_modifier is not None and not isinstance(self.detailed_time_modifier, LoincPart):
            self.detailed_time_modifier = LoincPart(**as_dict(self.detailed_time_modifier))

        if self.detailed_system_core is not None and not isinstance(self.detailed_system_core, LoincPart):
            self.detailed_system_core = LoincPart(**as_dict(self.detailed_system_core))

        if self.detailed_super_system is not None and not isinstance(self.detailed_super_system, LoincPart):
            self.detailed_super_system = LoincPart(**as_dict(self.detailed_super_system))

        if self.syntax_analyte_core is not None and not isinstance(self.syntax_analyte_core, LoincPart):
            self.syntax_analyte_core = LoincPart(**as_dict(self.syntax_analyte_core))

        if self.syntax_analyte_suffix is not None and not isinstance(self.syntax_analyte_suffix, LoincPart):
            self.syntax_analyte_suffix = LoincPart(**as_dict(self.syntax_analyte_suffix))

        if self.syntax_analyte_numerator is not None and not isinstance(self.syntax_analyte_numerator, LoincPart):
            self.syntax_analyte_numerator = LoincPart(**as_dict(self.syntax_analyte_numerator))

        if self.syntax_analyte_divisor is not None and not isinstance(self.syntax_analyte_divisor, LoincPart):
            self.syntax_analyte_divisor = LoincPart(**as_dict(self.syntax_analyte_divisor))

        if self.syntax_analyte_divisor_suffix is not None and not isinstance(self.syntax_analyte_divisor_suffix, LoincPart):
            self.syntax_analyte_divisor_suffix = LoincPart(**as_dict(self.syntax_analyte_divisor_suffix))

        if self.semantic_analyte_gene is not None and not isinstance(self.semantic_analyte_gene, LoincPart):
            self.semantic_analyte_gene = LoincPart(**as_dict(self.semantic_analyte_gene))

        if self.semantic_analyte_genetic_variant is not None and not isinstance(self.semantic_analyte_genetic_variant, LoincPart):
            self.semantic_analyte_genetic_variant = LoincPart(**as_dict(self.semantic_analyte_genetic_variant))

        if self.semantic_analyte_chemical is not None and not isinstance(self.semantic_analyte_chemical, LoincPart):
            self.semantic_analyte_chemical = LoincPart(**as_dict(self.semantic_analyte_chemical))

        if self.semantic_analyte_divisor_chemical is not None and not isinstance(self.semantic_analyte_divisor_chemical, LoincPart):
            self.semantic_analyte_divisor_chemical = LoincPart(**as_dict(self.semantic_analyte_divisor_chemical))

        if self.semantic_analyte_clinical_drug is not None and not isinstance(self.semantic_analyte_clinical_drug, LoincPart):
            self.semantic_analyte_clinical_drug = LoincPart(**as_dict(self.semantic_analyte_clinical_drug))

        if self.semantic_system_core_anatomic_entity is not None and not isinstance(self.semantic_system_core_anatomic_entity, LoincPart):
            self.semantic_system_core_anatomic_entity = LoincPart(**as_dict(self.semantic_system_core_anatomic_entity))

        if self.semantic_analyte_organism is not None and not isinstance(self.semantic_analyte_organism, LoincPart):
            self.semantic_analyte_organism = LoincPart(**as_dict(self.semantic_analyte_organism))

        if self.semantic_challenge_route is not None and not isinstance(self.semantic_challenge_route, LoincPart):
            self.semantic_challenge_route = LoincPart(**as_dict(self.semantic_challenge_route))

        if self.semantic_analyte_allergen is not None and not isinstance(self.semantic_analyte_allergen, LoincPart):
            self.semantic_analyte_allergen = LoincPart(**as_dict(self.semantic_analyte_allergen))

        if self.metadata_class is not None and not isinstance(self.metadata_class, LoincPart):
            self.metadata_class = LoincPart(**as_dict(self.metadata_class))

        if self.metadata_category is not None and not isinstance(self.metadata_category, LoincPart):
            self.metadata_category = LoincPart(**as_dict(self.metadata_category))

        if self.rad_anatomic_location_imaging_focus is not None and not isinstance(self.rad_anatomic_location_imaging_focus, LoincPart):
            self.rad_anatomic_location_imaging_focus = LoincPart(**as_dict(self.rad_anatomic_location_imaging_focus))

        if self.rad_anatomic_location_laterality is not None and not isinstance(self.rad_anatomic_location_laterality, LoincPart):
            self.rad_anatomic_location_laterality = LoincPart(**as_dict(self.rad_anatomic_location_laterality))

        if self.rad_anatomic_location_laterality_presence is not None and not isinstance(self.rad_anatomic_location_laterality_presence, LoincPart):
            self.rad_anatomic_location_laterality_presence = LoincPart(**as_dict(self.rad_anatomic_location_laterality_presence))

        if self.rad_anatomic_location_region_imaged is not None and not isinstance(self.rad_anatomic_location_region_imaged, LoincPart):
            self.rad_anatomic_location_region_imaged = LoincPart(**as_dict(self.rad_anatomic_location_region_imaged))

        if self.rad_guidance_for_action is not None and not isinstance(self.rad_guidance_for_action, LoincPart):
            self.rad_guidance_for_action = LoincPart(**as_dict(self.rad_guidance_for_action))

        if self.rad_guidance_for_approach is not None and not isinstance(self.rad_guidance_for_approach, LoincPart):
            self.rad_guidance_for_approach = LoincPart(**as_dict(self.rad_guidance_for_approach))

        if self.rad_guidance_for_object is not None and not isinstance(self.rad_guidance_for_object, LoincPart):
            self.rad_guidance_for_object = LoincPart(**as_dict(self.rad_guidance_for_object))

        if self.rad_guidance_for_presence is not None and not isinstance(self.rad_guidance_for_presence, LoincPart):
            self.rad_guidance_for_presence = LoincPart(**as_dict(self.rad_guidance_for_presence))

        if self.rad_maneuver_maneuver_type is not None and not isinstance(self.rad_maneuver_maneuver_type, LoincPart):
            self.rad_maneuver_maneuver_type = LoincPart(**as_dict(self.rad_maneuver_maneuver_type))

        if self.rad_modality_subtype is not None and not isinstance(self.rad_modality_subtype, LoincPart):
            self.rad_modality_subtype = LoincPart(**as_dict(self.rad_modality_subtype))

        if self.rad_modality_type is not None and not isinstance(self.rad_modality_type, LoincPart):
            self.rad_modality_type = LoincPart(**as_dict(self.rad_modality_type))

        if self.rad_pharmaceutical_route is not None and not isinstance(self.rad_pharmaceutical_route, LoincPart):
            self.rad_pharmaceutical_route = LoincPart(**as_dict(self.rad_pharmaceutical_route))

        if self.rad_pharmaceutical_substance_given is not None and not isinstance(self.rad_pharmaceutical_substance_given, LoincPart):
            self.rad_pharmaceutical_substance_given = LoincPart(**as_dict(self.rad_pharmaceutical_substance_given))

        if self.rad_reason_for_exam is not None and not isinstance(self.rad_reason_for_exam, LoincPart):
            self.rad_reason_for_exam = LoincPart(**as_dict(self.rad_reason_for_exam))

        if self.rad_subject is not None and not isinstance(self.rad_subject, LoincPart):
            self.rad_subject = LoincPart(**as_dict(self.rad_subject))

        if self.rad_timing is not None and not isinstance(self.rad_timing, LoincPart):
            self.rad_timing = LoincPart(**as_dict(self.rad_timing))

        if self.rad_view_aggregation is not None and not isinstance(self.rad_view_aggregation, LoincPart):
            self.rad_view_aggregation = LoincPart(**as_dict(self.rad_view_aggregation))

        if self.rad_view_view_type is not None and not isinstance(self.rad_view_view_type, LoincPart):
            self.rad_view_view_type = LoincPart(**as_dict(self.rad_view_view_type))

        if self.document_kind is not None and not isinstance(self.document_kind, LoincPart):
            self.document_kind = LoincPart(**as_dict(self.document_kind))

        if self.document_role is not None and not isinstance(self.document_role, LoincPart):
            self.document_role = LoincPart(**as_dict(self.document_role))

        if self.document_setting is not None and not isinstance(self.document_setting, LoincPart):
            self.document_setting = LoincPart(**as_dict(self.document_setting))

        if self.document_subject_matter_domain is not None and not isinstance(self.document_subject_matter_domain, LoincPart):
            self.document_subject_matter_domain = LoincPart(**as_dict(self.document_subject_matter_domain))

        if self.document_type_of_service is not None and not isinstance(self.document_type_of_service, LoincPart):
            self.document_type_of_service = LoincPart(**as_dict(self.document_type_of_service))

        super().__post_init__(**kwargs)


@dataclass
class LoincPart(LoincEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC.LoincPart
    class_class_curie: ClassVar[str] = "loinc:LoincPart"
    class_name: ClassVar[str] = "LoincPart"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincPart

    part_type_name: Optional[str] = None
    part_name: Optional[str] = None
    part_display_name: Optional[str] = None
    part_status: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.part_type_name is not None and not isinstance(self.part_type_name, str):
            self.part_type_name = str(self.part_type_name)

        if self.part_name is not None and not isinstance(self.part_name, str):
            self.part_name = str(self.part_name)

        if self.part_display_name is not None and not isinstance(self.part_display_name, str):
            self.part_display_name = str(self.part_display_name)

        if self.part_status is not None and not isinstance(self.part_status, str):
            self.part_status = str(self.part_status)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.codes = Slot(uri=LOINC.codes, name="codes", curie=LOINC.curie('codes'),
                   model_uri=LOINC.codes, domain=None, range=Optional[Union[Union[dict, LoincTerm], List[Union[dict, LoincTerm]]]])

slots.parts = Slot(uri=LOINC.parts, name="parts", curie=LOINC.curie('parts'),
                   model_uri=LOINC.parts, domain=None, range=Optional[Union[Union[dict, LoincPart], List[Union[dict, LoincPart]]]])

slots.id = Slot(uri=LOINC.id, name="id", curie=LOINC.curie('id'),
                   model_uri=LOINC.id, domain=None, range=URIRef)

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=LOINC.label, domain=None, range=Optional[str])

slots.description = Slot(uri=RDFS.description, name="description", curie=RDFS.curie('description'),
                   model_uri=LOINC.description, domain=None, range=Optional[str])

slots.subClassOf = Slot(uri=RDFS.subClassOf, name="subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.subClassOf, domain=None, range=Optional[Union[Union[dict, LoincEntity], List[Union[dict, LoincEntity]]]])

slots.loinc_number = Slot(uri=LOINC.loinc_number, name="loinc_number", curie=LOINC.curie('loinc_number'),
                   model_uri=LOINC.loinc_number, domain=None, range=Optional[str])

slots.long_common_name = Slot(uri=LOINC.long_common_name, name="long_common_name", curie=LOINC.curie('long_common_name'),
                   model_uri=LOINC.long_common_name, domain=None, range=Optional[str])

slots.formal_name = Slot(uri=LOINC.formal_name, name="formal_name", curie=LOINC.curie('formal_name'),
                   model_uri=LOINC.formal_name, domain=None, range=Optional[str])

slots.short_name = Slot(uri=LOINC.short_name, name="short_name", curie=LOINC.curie('short_name'),
                   model_uri=LOINC.short_name, domain=None, range=Optional[str])

slots.status = Slot(uri=LOINC.status, name="status", curie=LOINC.curie('status'),
                   model_uri=LOINC.status, domain=None, range=Optional[str])

slots.loinc_class = Slot(uri=LOINC.loinc_class, name="loinc_class", curie=LOINC.curie('loinc_class'),
                   model_uri=LOINC.loinc_class, domain=None, range=Optional[str])

slots.loinc_class_type = Slot(uri=LOINC.loinc_class_type, name="loinc_class_type", curie=LOINC.curie('loinc_class_type'),
                   model_uri=LOINC.loinc_class_type, domain=None, range=Optional[str])

slots.primary_component = Slot(uri=LOINC_PROPERTY.COMPONENT, name="primary_component", curie=LOINC_PROPERTY.curie('COMPONENT'),
                   model_uri=LOINC.primary_component, domain=None, range=Optional[Union[dict, LoincPart]])

slots.primary_property = Slot(uri=LOINC_PROPERTY.PROPERTY, name="primary_property", curie=LOINC_PROPERTY.curie('PROPERTY'),
                   model_uri=LOINC.primary_property, domain=None, range=Optional[Union[dict, LoincPart]])

slots.primary_time_aspect = Slot(uri=LOINC_PROPERTY.TIME_ASPECT, name="primary_time_aspect", curie=LOINC_PROPERTY.curie('TIME_ASPECT'),
                   model_uri=LOINC.primary_time_aspect, domain=None, range=Optional[Union[dict, LoincPart]])

slots.primary_system = Slot(uri=LOINC_PROPERTY.SYSTEM, name="primary_system", curie=LOINC_PROPERTY.curie('SYSTEM'),
                   model_uri=LOINC.primary_system, domain=None, range=Optional[Union[dict, LoincPart]])

slots.primary_scale_typ = Slot(uri=LOINC_PROPERTY.SCALE_TYP, name="primary_scale_typ", curie=LOINC_PROPERTY.curie('SCALE_TYP'),
                   model_uri=LOINC.primary_scale_typ, domain=None, range=Optional[Union[dict, LoincPart]])

slots.primary_method_typ = Slot(uri=LOINC_PROPERTY.METHOD_TYP, name="primary_method_typ", curie=LOINC_PROPERTY.curie('METHOD_TYP'),
                   model_uri=LOINC.primary_method_typ, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_analyte = Slot(uri=LOINC_PROPERTY.analyte, name="detailed_analyte", curie=LOINC_PROPERTY.curie('analyte'),
                   model_uri=LOINC.detailed_analyte, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_challenge = Slot(uri=LOINC_PROPERTY.challenge, name="detailed_challenge", curie=LOINC_PROPERTY.curie('challenge'),
                   model_uri=LOINC.detailed_challenge, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_adjustment = Slot(uri=LOINC_PROPERTY.adjustment, name="detailed_adjustment", curie=LOINC_PROPERTY.curie('adjustment'),
                   model_uri=LOINC.detailed_adjustment, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_count = Slot(uri=LOINC_PROPERTY.count, name="detailed_count", curie=LOINC_PROPERTY.curie('count'),
                   model_uri=LOINC.detailed_count, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_time_core = Slot(uri=LOINC_PROPERTY['time-core'], name="detailed_time_core", curie=LOINC_PROPERTY.curie('time-core'),
                   model_uri=LOINC.detailed_time_core, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_time_modifier = Slot(uri=LOINC_PROPERTY['time-modifier'], name="detailed_time_modifier", curie=LOINC_PROPERTY.curie('time-modifier'),
                   model_uri=LOINC.detailed_time_modifier, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_system_core = Slot(uri=LOINC_PROPERTY['system-core'], name="detailed_system_core", curie=LOINC_PROPERTY.curie('system-core'),
                   model_uri=LOINC.detailed_system_core, domain=None, range=Optional[Union[dict, LoincPart]])

slots.detailed_super_system = Slot(uri=LOINC_PROPERTY['super-system'], name="detailed_super_system", curie=LOINC_PROPERTY.curie('super-system'),
                   model_uri=LOINC.detailed_super_system, domain=None, range=Optional[Union[dict, LoincPart]])

slots.syntax_analyte_core = Slot(uri=LOINC_PROPERTY['analyte-core'], name="syntax_analyte_core", curie=LOINC_PROPERTY.curie('analyte-core'),
                   model_uri=LOINC.syntax_analyte_core, domain=None, range=Optional[Union[dict, LoincPart]])

slots.syntax_analyte_suffix = Slot(uri=LOINC_PROPERTY['analyte-suffix'], name="syntax_analyte_suffix", curie=LOINC_PROPERTY.curie('analyte-suffix'),
                   model_uri=LOINC.syntax_analyte_suffix, domain=None, range=Optional[Union[dict, LoincPart]])

slots.syntax_analyte_numerator = Slot(uri=LOINC_PROPERTY['analyte-numerator'], name="syntax_analyte_numerator", curie=LOINC_PROPERTY.curie('analyte-numerator'),
                   model_uri=LOINC.syntax_analyte_numerator, domain=None, range=Optional[Union[dict, LoincPart]])

slots.syntax_analyte_divisor = Slot(uri=LOINC_PROPERTY['analyte-divisor'], name="syntax_analyte_divisor", curie=LOINC_PROPERTY.curie('analyte-divisor'),
                   model_uri=LOINC.syntax_analyte_divisor, domain=None, range=Optional[Union[dict, LoincPart]])

slots.syntax_analyte_divisor_suffix = Slot(uri=LOINC_PROPERTY['analyte-divisor-suffix'], name="syntax_analyte_divisor_suffix", curie=LOINC_PROPERTY.curie('analyte-divisor-suffix'),
                   model_uri=LOINC.syntax_analyte_divisor_suffix, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_gene = Slot(uri=LOINC_PROPERTY.analyte_gene, name="semantic_analyte_gene", curie=LOINC_PROPERTY.curie('analyte_gene'),
                   model_uri=LOINC.semantic_analyte_gene, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_genetic_variant = Slot(uri=LOINC_PROPERTY['analyte-genetic-variant'], name="semantic_analyte_genetic_variant", curie=LOINC_PROPERTY.curie('analyte-genetic-variant'),
                   model_uri=LOINC.semantic_analyte_genetic_variant, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_chemical = Slot(uri=LOINC_PROPERTY['analyte-chemical'], name="semantic_analyte_chemical", curie=LOINC_PROPERTY.curie('analyte-chemical'),
                   model_uri=LOINC.semantic_analyte_chemical, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_divisor_chemical = Slot(uri=LOINC_PROPERTY['analyte-divisor-chemical'], name="semantic_analyte_divisor_chemical", curie=LOINC_PROPERTY.curie('analyte-divisor-chemical'),
                   model_uri=LOINC.semantic_analyte_divisor_chemical, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_clinical_drug = Slot(uri=LOINC_PROPERTY['analyte-clinical-drug'], name="semantic_analyte_clinical_drug", curie=LOINC_PROPERTY.curie('analyte-clinical-drug'),
                   model_uri=LOINC.semantic_analyte_clinical_drug, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_system_core_anatomic_entity = Slot(uri=LOINC_PROPERTY['system-core-anatomic-entity'], name="semantic_system_core_anatomic_entity", curie=LOINC_PROPERTY.curie('system-core-anatomic-entity'),
                   model_uri=LOINC.semantic_system_core_anatomic_entity, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_organism = Slot(uri=LOINC_PROPERTY['analyte-organism'], name="semantic_analyte_organism", curie=LOINC_PROPERTY.curie('analyte-organism'),
                   model_uri=LOINC.semantic_analyte_organism, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_challenge_route = Slot(uri=LOINC_PROPERTY['challenge-route'], name="semantic_challenge_route", curie=LOINC_PROPERTY.curie('challenge-route'),
                   model_uri=LOINC.semantic_challenge_route, domain=None, range=Optional[Union[dict, LoincPart]])

slots.semantic_analyte_allergen = Slot(uri=LOINC_PROPERTY['analyte-allergen'], name="semantic_analyte_allergen", curie=LOINC_PROPERTY.curie('analyte-allergen'),
                   model_uri=LOINC.semantic_analyte_allergen, domain=None, range=Optional[Union[dict, LoincPart]])

slots.metadata_class = Slot(uri=LOINC_PROPERTY.class_, name="metadata_class", curie=LOINC_PROPERTY.curie('class_'),
                   model_uri=LOINC.metadata_class, domain=None, range=Optional[Union[dict, LoincPart]])

slots.metadata_category = Slot(uri=LOINC_PROPERTY.category, name="metadata_category", curie=LOINC_PROPERTY.curie('category'),
                   model_uri=LOINC.metadata_category, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_anatomic_location_imaging_focus = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-imaging-focus'], name="rad_anatomic_location_imaging_focus", curie=LOINC_PROPERTY.curie('rad-anatomic-location-imaging-focus'),
                   model_uri=LOINC.rad_anatomic_location_imaging_focus, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_anatomic_location_laterality = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-laterality'], name="rad_anatomic_location_laterality", curie=LOINC_PROPERTY.curie('rad-anatomic-location-laterality'),
                   model_uri=LOINC.rad_anatomic_location_laterality, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_anatomic_location_laterality_presence = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-laterality-presence'], name="rad_anatomic_location_laterality_presence", curie=LOINC_PROPERTY.curie('rad-anatomic-location-laterality-presence'),
                   model_uri=LOINC.rad_anatomic_location_laterality_presence, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_anatomic_location_region_imaged = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-region-imaged'], name="rad_anatomic_location_region_imaged", curie=LOINC_PROPERTY.curie('rad-anatomic-location-region-imaged'),
                   model_uri=LOINC.rad_anatomic_location_region_imaged, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_guidance_for_action = Slot(uri=LOINC_PROPERTY['rad-guidance-for-action'], name="rad_guidance_for_action", curie=LOINC_PROPERTY.curie('rad-guidance-for-action'),
                   model_uri=LOINC.rad_guidance_for_action, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_guidance_for_approach = Slot(uri=LOINC_PROPERTY['rad-guidance-for-approach'], name="rad_guidance_for_approach", curie=LOINC_PROPERTY.curie('rad-guidance-for-approach'),
                   model_uri=LOINC.rad_guidance_for_approach, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_guidance_for_object = Slot(uri=LOINC_PROPERTY['rad-guidance-for-object'], name="rad_guidance_for_object", curie=LOINC_PROPERTY.curie('rad-guidance-for-object'),
                   model_uri=LOINC.rad_guidance_for_object, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_guidance_for_presence = Slot(uri=LOINC_PROPERTY['rad-guidance-for-presence'], name="rad_guidance_for_presence", curie=LOINC_PROPERTY.curie('rad-guidance-for-presence'),
                   model_uri=LOINC.rad_guidance_for_presence, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_maneuver_maneuver_type = Slot(uri=LOINC_PROPERTY['rad-maneuver-maneuver-type'], name="rad_maneuver_maneuver_type", curie=LOINC_PROPERTY.curie('rad-maneuver-maneuver-type'),
                   model_uri=LOINC.rad_maneuver_maneuver_type, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_modality_subtype = Slot(uri=LOINC_PROPERTY['rad-modality-subtype'], name="rad_modality_subtype", curie=LOINC_PROPERTY.curie('rad-modality-subtype'),
                   model_uri=LOINC.rad_modality_subtype, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_modality_type = Slot(uri=LOINC_PROPERTY['rad-modality-type'], name="rad_modality_type", curie=LOINC_PROPERTY.curie('rad-modality-type'),
                   model_uri=LOINC.rad_modality_type, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_pharmaceutical_route = Slot(uri=LOINC_PROPERTY['rad-pharmaceutical-route'], name="rad_pharmaceutical_route", curie=LOINC_PROPERTY.curie('rad-pharmaceutical-route'),
                   model_uri=LOINC.rad_pharmaceutical_route, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_pharmaceutical_substance_given = Slot(uri=LOINC_PROPERTY['rad-pharmaceutical-substance-given'], name="rad_pharmaceutical_substance_given", curie=LOINC_PROPERTY.curie('rad-pharmaceutical-substance-given'),
                   model_uri=LOINC.rad_pharmaceutical_substance_given, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_reason_for_exam = Slot(uri=LOINC_PROPERTY['rad-reason-for-exam'], name="rad_reason_for_exam", curie=LOINC_PROPERTY.curie('rad-reason-for-exam'),
                   model_uri=LOINC.rad_reason_for_exam, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_subject = Slot(uri=LOINC_PROPERTY['rad-subject'], name="rad_subject", curie=LOINC_PROPERTY.curie('rad-subject'),
                   model_uri=LOINC.rad_subject, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_timing = Slot(uri=LOINC_PROPERTY['rad-timing'], name="rad_timing", curie=LOINC_PROPERTY.curie('rad-timing'),
                   model_uri=LOINC.rad_timing, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_view_aggregation = Slot(uri=LOINC_PROPERTY.rad_view_aggregation, name="rad_view_aggregation", curie=LOINC_PROPERTY.curie('rad_view_aggregation'),
                   model_uri=LOINC.rad_view_aggregation, domain=None, range=Optional[Union[dict, LoincPart]])

slots.rad_view_view_type = Slot(uri=LOINC_PROPERTY.rad_view_view_type, name="rad_view_view_type", curie=LOINC_PROPERTY.curie('rad_view_view_type'),
                   model_uri=LOINC.rad_view_view_type, domain=None, range=Optional[Union[dict, LoincPart]])

slots.document_kind = Slot(uri=LOINC_PROPERTY['document-kind'], name="document_kind", curie=LOINC_PROPERTY.curie('document-kind'),
                   model_uri=LOINC.document_kind, domain=None, range=Optional[Union[dict, LoincPart]])

slots.document_role = Slot(uri=LOINC_PROPERTY['document-role'], name="document_role", curie=LOINC_PROPERTY.curie('document-role'),
                   model_uri=LOINC.document_role, domain=None, range=Optional[Union[dict, LoincPart]])

slots.document_setting = Slot(uri=LOINC_PROPERTY['document-setting'], name="document_setting", curie=LOINC_PROPERTY.curie('document-setting'),
                   model_uri=LOINC.document_setting, domain=None, range=Optional[Union[dict, LoincPart]])

slots.document_subject_matter_domain = Slot(uri=LOINC_PROPERTY['document-subject-matter-domain'], name="document_subject_matter_domain", curie=LOINC_PROPERTY.curie('document-subject-matter-domain'),
                   model_uri=LOINC.document_subject_matter_domain, domain=None, range=Optional[Union[dict, LoincPart]])

slots.document_type_of_service = Slot(uri=LOINC_PROPERTY['document-type-of-service'], name="document_type_of_service", curie=LOINC_PROPERTY.curie('document-type-of-service'),
                   model_uri=LOINC.document_type_of_service, domain=None, range=Optional[Union[dict, LoincPart]])

slots.part_type_name = Slot(uri=LOINC['part-type-name'], name="part_type_name", curie=LOINC.curie('part-type-name'),
                   model_uri=LOINC.part_type_name, domain=None, range=Optional[str])

slots.part_name = Slot(uri=LOINC.part_name, name="part_name", curie=LOINC.curie('part_name'),
                   model_uri=LOINC.part_name, domain=None, range=Optional[str])

slots.part_display_name = Slot(uri=LOINC.part_display_name, name="part_display_name", curie=LOINC.curie('part_display_name'),
                   model_uri=LOINC.part_display_name, domain=None, range=Optional[str])

slots.part_status = Slot(uri=LOINC.status, name="part_status", curie=LOINC.curie('status'),
                   model_uri=LOINC.part_status, domain=None, range=Optional[str])
