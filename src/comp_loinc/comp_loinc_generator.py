import shutil
import time
import typing as t
import urllib.parse
from pathlib import Path

import funowl
import linkml_runtime
from funowl import literals
from linkml_owl.dumpers import owl_dumper

import loinclib as ll
from comp_loinc import datamodel
from loinclib import LoincEdgeType as Let, LoincAttributeType as Lat


class CompLoincGenerator:
    LOINCS_LIST = 'loincs-list'
    LOINCS_PRIMARY_DEFS = 'loincs-primary-defs'
    LOINCS_SUPPLEMENTARY_DEFS = 'loincs-supplementary-defs'

    PARTS_LIST = 'parts-list'
    PARTS_TREES = 'parts-trees'
    PARTS_GROUP_CHEM_EQ = 'parts-group-chem-eq'

    GROUPS = '__groups'
    GROUP_COMP_HAS_SLASH = 'group-component-has-slash'

    def __init__(self, loinc_release: ll.LoincRelease,
                 schema_directory: Path,
                 output_directory: Path):
        self.release = loinc_release
        self.schema_dir = schema_directory
        self.output_directory = output_directory

        self._owl_dumper = owl_dumper.OWLDumper()
        self.__parts: t.Dict[str, datamodel.PartClass] = {}

        self.__datetime_string = time.strftime('%Y-%m-%d_%H-%M-%S')

        self._outputs: t.Dict[str: t.Dict[str, t.List[datamodel.Thing]]] = dict()
        self._outputs_schema: t.Dict[str, linkml_runtime.SchemaView] = dict()

    def generate_loincs_list(self):

        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        loincs_root = datamodel.LoincCodeClass(id=_loincify('__loincs'))
        loinc_code_map['__loincs'] = loincs_root

        for loinc_node_id in loinc_node_ids:
            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            properties = self.release.node_properties(loinc_node_id)

            parent = self._loinc_parent(properties, loinc_code_map)

            loinc = datamodel.LoincCodeClass(id=_loincify(code), subClassOf=[parent.id])
            loinc_code_map[code] = loinc

            # loinc.subClassOf.append(loincs_root.id)
            loinc.loinc_number = code

            long_common_name = properties.get(Lat.loinc_long_common_name, None)
            if long_common_name:
                loinc.long_common_name = long_common_name[0]
                loinc.label = f'_LC  {long_common_name[0]}'

            formal_name = f'{properties.get(Lat.loinc_component)[0]}'
            formal_name += f':{properties.get(Lat.loinc_property)[0]}'
            formal_name += f':{properties.get(Lat.loinc_time_aspect)[0]}'
            formal_name += f':{properties.get(Lat.loinc_system)[0]}'
            formal_name += f':{properties.get(Lat.loinc_scale_type)[0]}'
            if Lat.loinc_method_type in properties:
                formal_name += f':{properties.get(Lat.loinc_method_type)[0]}'

            loinc.formal_name = formal_name

            definitions = properties.get(Lat.loinc_definition, None)
            if definitions:
                # This is needed to work around some unusual string values that throw an error during dumping of:
                # ./LoincTable/Loinc.csv line: 47536:
                # "51947-0","Package label.Bottom panel",....
                definition = literals.Literal._to_n3(definitions[0])
                if definition:
                    loinc.description = definition

            short_name = properties.get(Lat.loinc_short_name, None)
            if short_name:
                loinc.short_name = short_name[0]

        self._outputs[CompLoincGenerator.LOINCS_LIST] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.LOINCS_LIST] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def generate_loincs_primary_defs(self):

        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        for loinc_node_id in loinc_node_ids:
            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc

            # component
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_COMPONENT)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple components: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component = datamodel.PartClassId(_loincify(part_code))

            # property
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_property = datamodel.PartClassId(_loincify(part_code))

            # time
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_TIME)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple times: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_time = datamodel.PartClassId(_loincify(part_code))

            # system
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_SYSTEM)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_system = datamodel.PartClassId(_loincify(part_code))

            # scale
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_scale = datamodel.PartClassId(_loincify(part_code))

            # method
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_method = datamodel.PartClassId(_loincify(part_code))

        self._outputs[CompLoincGenerator.LOINCS_PRIMARY_DEFS] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.LOINCS_PRIMARY_DEFS] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def generate_loincs_supplementary_defs(self):
        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        for loinc_node_id in loinc_node_ids:
            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc

            # 1.1 component analyte
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_COMPONENT_analyte)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component analytes: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component_analyte = datamodel.PartClassId(_loincify(part_code))

            # 1.2 component challenge
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_CHALLENGE_challenge)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component challenges: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component_challenge = datamodel.PartClassId(_loincify(part_code))

            # 1.3 component adjustment
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_ADJUSTMENT_adjustment)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component adjustments: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component_adjustment = datamodel.PartClassId(_loincify(part_code))

            # 1.4 component count
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_COUNT_count)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component counts: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component_count = datamodel.PartClassId(_loincify(part_code))

            # 2 property
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_property = datamodel.PartClassId(_loincify(part_code))

            # 3.1 time core
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_TIME_time_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple time cores: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_time_core = datamodel.PartClassId(_loincify(part_code))

            # 3.2 time modifier
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_TIME_MODIFIER_time_modifier)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple time modifiers: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_time_modifier = datamodel.PartClassId(_loincify(part_code))

            # 4.1 system core
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_SYSTEM_system_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple system cores: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_system_core = datamodel.PartClassId(_loincify(part_code))

            # 4.2 system super system
            parts = self.release.out_node_ids(loinc_node_id, Let.DetailedModel_SUPER_SYSTEM_super_system)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple system super systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_system_super_system = datamodel.PartClassId(_loincify(part_code))

            # scale
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_scale = datamodel.PartClassId(_loincify(part_code))

            # method
            parts = self.release.out_node_ids(loinc_node_id, Let.Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_method = datamodel.PartClassId(_loincify(part_code))

            # semantic analyte gene
            parts = self.release.out_node_ids(loinc_node_id, Let.SemanticEnhancement_GENE_analyte_gene)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple semantic genes: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.semantic_analyte_gene = datamodel.PartClassId(_loincify(part_code))

            # syntax analyte core
            parts = self.release.out_node_ids(loinc_node_id, Let.SyntaxEnhancement_COMPONENT_analyte_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte core: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.syntax_analyte_core = datamodel.PartClassId(_loincify(part_code))

            # syntax analyte suffix
            parts = self.release.out_node_ids(loinc_node_id, Let.SyntaxEnhancement_SUFFIX_analyte_suffix)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte core: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.syntax_analyte_suffix = datamodel.PartClassId(_loincify(part_code))

            # syntax analyte divisor
            parts = self.release.out_node_ids(loinc_node_id, Let.SyntaxEnhancement_DIVISOR_analyte_divisor)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte divisor: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.syntax_analyte_divisor = datamodel.PartClassId(_loincify(part_code))

            # syntax analyte divisor suffix
            parts = self.release.out_node_ids(loinc_node_id, Let.SyntaxEnhancement_SUFFIX_analyte_divisor_suffix)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte divisor suffixes: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.syntax_analyte_divisor_suffix = datamodel.PartClassId(_loincify(part_code))

            # syntax analyte numerator
            parts = self.release.out_node_ids(loinc_node_id, Let.SyntaxEnhancement_NUMERATOR_analyte_numerator)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte numerators: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.syntax_analyte_numerator = datamodel.PartClassId(_loincify(part_code))

        self._outputs[CompLoincGenerator.LOINCS_SUPPLEMENTARY_DEFS] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.LOINCS_SUPPLEMENTARY_DEFS] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def generate_group_component_has_slash(self):
        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        has_slash = datamodel.LoincCodeClass(id=_loincify(CompLoincGenerator.GROUP_COMP_HAS_SLASH))
        has_slash.subClassOf = datamodel.LoincCodeClassId(_loincify(CompLoincGenerator.GROUPS))
        loinc_code_map[CompLoincGenerator.GROUP_COMP_HAS_SLASH] = has_slash

        for loinc_node_id in loinc_node_ids:

            properties = self.release.node_properties(loinc_node_id)

            component_names = properties.get(Lat.loinc_component, None)
            if component_names:
                component_name = component_names[0]
                part_1 = component_name.split('^')[0]
                if '/' not in part_1:
                    continue
            else:
                continue

            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            loinc.subClassOf = has_slash.id
            loinc_code_map[code] = loinc

        self._outputs[CompLoincGenerator.GROUP_COMP_HAS_SLASH] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.GROUP_COMP_HAS_SLASH] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def generate_parts_list(self):
        part_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_part)
        code_part_map: t.Dict[str, datamodel.PartClass] = {}

        for part_node_id in part_node_ids:
            code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
            properties: dict = self.release.node_properties(part_node_id)
            part_name = properties.get(Lat.part_name, [None])[0]
            part_display_name = properties.get(Lat.part_display_name, [None])[0]
            part_type = properties.get(Lat.part_type, [None])[0]

            part = datamodel.PartClass(id=_loincify(code), part_number=code)

            if part_name:
                part.label = part_name
                part.part_name = part_name
            if part_display_name:
                part.part_display_name = part_display_name

            if part_type:
                part.part_type = part_type

            code_part_map[code] = part

        self._outputs[CompLoincGenerator.PARTS_LIST] = code_part_map
        self._outputs_schema[CompLoincGenerator.PARTS_LIST] = linkml_runtime.SchemaView(
            self.schema_dir / 'part_schema.yaml')

    def generate_parts_trees(self):

        part_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_part)
        code_part_map: t.Dict[str, datamodel.PartClass] = {}

        parts_hierarchy_root = datamodel.PartClass(id=_loincify('__parts_trees'))
        parts_no_hierarchy_root = datamodel.PartClass(id=_loincify('__parts_no_hierarchy'))

        code_part_map['__parts_trees'] = parts_hierarchy_root
        code_part_map['__parts_no_hierarchy'] = parts_no_hierarchy_root

        for part_node_id in part_node_ids:
            part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
            part = datamodel.PartClass(id=_loincify(part_code))
            code_part_map[part_code] = part

            properties = self.release.node_properties(part_node_id)

            # Do annotations.
            # Is this a new part code?
            if Lat.part_name not in properties:
                # this code is not in the parts file
                part.part_number = part_code
                code_text = properties.get(Lat.tree_code_text, None)
                if code_text:
                    part.label = f'_tree_label_ {code_text[0]}'

            # do subclass axioms
            parent_ids = self.release.out_node_ids(part_node_id, ll.EdgeType.LoincLib_HasParent)
            if parent_ids:
                part.subClassOf = [_loincify(ll.NodeType.loinc_part.identifier_of_node_id(parent_id)) for
                                   parent_id in parent_ids.values()]
            else:
                part_parent = None
                child_node_ids = self.release.in_node_ids(part_node_id, ll.EdgeType.LoincLib_HasParent)
                for _, child_of_child_node_id in child_node_ids.items():
                    child_node_type = ll.NodeType.type_for_node_id(child_of_child_node_id)
                    if child_node_type and child_node_type == ll.NodeType.loinc_part:
                        part_parent = parts_hierarchy_root
                        break

                if not part_parent:
                    part_parent = parts_no_hierarchy_root
                part.subClassOf.append(part_parent)

        self._outputs[CompLoincGenerator.PARTS_TREES] = code_part_map
        self._outputs_schema[CompLoincGenerator.PARTS_TREES] = linkml_runtime.SchemaView(
            self.schema_dir / 'part_schema.yaml')

    def generate_parts_group_chem_equivalences(self):

        code_map: dict[str, datamodel.LoincCodeClass] = {}

        group = datamodel.LoincCodeClass(id=_loincify('__parts-group-comp-eq'))
        group.subClassOf = datamodel.LoincCodeClassId(CompLoincGenerator.GROUPS)
        code_map[group.id] = group

        chem_node_id = ll.NodeType.loinc_part.node_id_of_identifier('LP7786-9')
        chem = self._parts_group_comp_equivalences_recurse(chem_node_id, code_map)
        chem.subClassOf = group.id

        self._outputs[CompLoincGenerator.PARTS_GROUP_CHEM_EQ] = code_map
        code_view = linkml_runtime.SchemaView(self.schema_dir / 'code_schema.yaml')
        part_view = linkml_runtime.SchemaView(self.schema_dir / 'part_schema.yaml')
        code_view.merge_schema(part_view.schema)
        self._outputs_schema[CompLoincGenerator.PARTS_GROUP_CHEM_EQ] = code_view

    def _parts_group_comp_equivalences_recurse(self, part_node_id, code_map):
        code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
        properties = self.release.node_properties(part_node_id)

        part_based_def = datamodel.LoincCodeClassNonIntersection(id=_loincify(f'{code}_comp_eq'))

        label = None
        part_names = properties.get(Lat.part_name, None)
        if part_names:
            label = f'{part_names[0]} (COMP EQ)'
        if not label:
            code_texts = properties.get(Lat.tree_code_text)
            if code_texts:
                label = f'{code_texts[0]} (COMP EQ)'
        if not label:
            label = f'{code} (COMP EQ)'

        part_based_def.label = label
        part_based_def.has_component = datamodel.PartClass(id=_loincify(code))
        code_map[code] = part_based_def

        children_parts = self.release.in_node_ids(part_node_id, ll.EdgeType.LoincLib_HasParent).values()
        for child_part_id in children_parts:
            if ll.NodeType.type_for_node_id(child_part_id) == ll.NodeType.loinc_part:
                child_def = self._parts_group_comp_equivalences_recurse(child_part_id, code_map)
                child_def.subClassOf.append(part_based_def.id)

        return part_based_def

    def save_outputs(self):
        for filename, output in self._outputs.items():
            self._write_outputs(output_name=filename)

    def _write_outputs(self, /, *,
                       output_name: str,
                       timestamped=True):
        output_file = self.output_directory / f'{output_name}.owl'
        output_file_datetime = self.output_directory / 'datetime' / f'{output_name}_{self.__datetime_string}.owl'

        output_file_datetime.parent.mkdir(parents=True, exist_ok=True)
        print(f'Writing: {output_file_datetime}', flush=True)
        document: funowl.ontology_document.OntologyDocument = \
            self._owl_dumper.to_ontology_document(element=list(self._outputs[output_name].values()),
                                                  schema=self._outputs_schema[output_name].schema)
        document.ontology.iri = funowl.identifiers.IRI(f'https://loinc.org/{output_name}')

        with open(output_file_datetime, 'w') as f:
            f.write(str(document))
        if timestamped:
            shutil.copyfile(output_file_datetime, output_file)
        else:
            shutil.move(output_file_datetime, output_file)

    def _loinc_parent(self, properties, code_map: dict[str, datamodel.LoincCodeClass]) -> datamodel.LoincCodeClass:

        class_types = properties.get(Lat.loinc_class_type, None)
        class_type = None
        if class_types:
            class_type_code = f'classtype_{class_types[0]}'
            class_type = code_map.setdefault(class_type_code, datamodel.LoincCodeClass(id=_loincify(class_type_code),
                                                                                       label=f'class type {class_types[0]}',
                                                                                       subClassOf=[
                                                                                           code_map['__loincs'].id
                                                                                       ]
                                                                                       ))

        classes = properties.get(Lat.loinc_class, None)
        class_part = None
        if classes:
            class_parts = classes[0].split('.')
            url_suffix = None
            for part in class_parts:
                if not class_part:
                    url_suffix = f'class_{part}'

                    class_part = code_map.setdefault(url_suffix, datamodel.LoincCodeClass(
                        id=_loincify(urllib.parse.quote(url_suffix))))
                    class_part.subClassOf = [class_type.id]
                    continue
                else:
                    url_suffix = f'{url_suffix}.{part}'
                    class_part = code_map.setdefault(url_suffix,
                                                     datamodel.LoincCodeClass(
                                                         id=_loincify(urllib.parse.quote(url_suffix)),
                                                         subClassOf=[class_part.id]))

        return class_part


def _loincify(identifier) -> str:
    """
    adds the loinc: prefix to loinc part and code numbers
    :param identifier:
    :return: string
    """
    if identifier == 'owl:Thing':
        return identifier

    return f"loinc:{identifier}"
