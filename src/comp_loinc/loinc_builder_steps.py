import typing as t
from pathlib import Path

import funowl
import typer
from linkml_owl.dumpers.owl_dumper import OWLDumper
from linkml_runtime import SchemaView

from comp_loinc import Runtime
from comp_loinc.datamodel import LoincPart
from comp_loinc.datamodel.comp_loinc import LoincTerm
from loinclib import Configuration
from loinclib import LoincLoader
from loinclib import LoincNodeType, LoincTermProps
from loinclib.loinc_schema import LoincPartProps


class LoincBuilderSteps:

  def __init__(self, *,
      configuration: Configuration):
    self.configuration = configuration
    self.runtime: t.Optional[Runtime] = None

  def setup_cli_builder_steps_all(self, builder):

    builder.cli.command('lt-inst-all', help='Instantiate all LOINC terms into current module.')(
        self.term_instance_all)

    builder.cli.command('lp-inst-all', help='Instantiate all LOINC parts into current module.')(
        self.part_instance_all)

    builder.cli.command('label', help='Add rdfs:label to current entities.')(self.add_labels)
    builder.cli.command('annotate', help='Add annotations to current entities.')(self.add_annotations)

    builder.cli.command('load-schema', help='Loads a LinkML schema file and gives it a name. '
                                            'It also makes it the "current" schema to operate on with schema related builder steps.')(
        self.load_linkml_schema)
    builder.cli.command('save-owl', help='Saves the current module to an owl file.')(self.save_to_owl)

  def term_instance_all(self):
    typer.echo(f'Running lt_inst_all')
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_loinc_table__loinc_csv()
    count = 0
    for node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):
      count = count + 1
      if self.configuration.fast_run and count > 100:
        break
      loinc_number = node.get_property(LoincTermProps.loinc_number)

      # add if not already instantiated, to not override an existing one
      if self.runtime.current_module.get_entity(loinc_number, LoincTerm) is None:
        loinc_term = LoincTerm(id=loinc_number)
        self.runtime.current_module.add_entity(loinc_term)

  def part_instance_all(self):
    typer.echo(f'Running lp_inst_all')
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, configuration=self.configuration)
    loinc_loader.load_accessory_files__part_file__part_csv()
    count = 0
    for node in self.runtime.graph.get_nodes(LoincNodeType.LoincPart):
      count = count + 1
      if self.configuration.fast_run and count > 100:
        break
      number = node.get_property(LoincPartProps.part_number)

      # add if not already instantiated, to not override an existing one
      if self.runtime.current_module.get_entity(number, LoincPart) is None:
        part = LoincPart(id=number)
        self.runtime.current_module.add_entity(part)

  def add_labels(self):
    loinc_term: LoincTerm
    for loinc_term in self.runtime.current_module.get_entities_of_type(LoincTerm):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code=loinc_term.id)
      long_name = node.get_property(LoincTermProps.long_common_name)
      loinc_term.entity_label = f'LT   {long_name}'

    loinc_part: LoincPart
    for loinc_part in self.runtime.current_module.get_entities_of_type(LoincPart):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincPart, code=loinc_part.id)
      part_name = node.get_property(LoincPartProps.part_name)
      loinc_part.entity_label = f'LP   {part_name}'

  def add_annotations(self):
    loinc_term: LoincTerm
    for loinc_term in self.runtime.current_module.get_entities_of_type(LoincTerm):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincTerm, code=loinc_term.id)

      number = node.get_property(LoincTermProps.loinc_number)
      long_name = node.get_property(LoincTermProps.long_common_name)
      class_type = node.get_property(LoincTermProps.class_type)
      class_ = node.get_property(LoincTermProps.class_)

      loinc_term.long_common_name = long_name
      loinc_term.loinc_number = number
      loinc_term.loinc_class = class_
      loinc_term.loinc_class_type = class_type

    loinc_part: LoincPart
    for loinc_part in self.runtime.current_module.get_entities_of_type(LoincPart):
      node = self.runtime.graph.get_node_by_code(type_=LoincNodeType.LoincPart, code=loinc_part.id)
      part_number = node.get_property(LoincPartProps.part_number)
      part_name = node.get_property(LoincPartProps.part_name)
      part_type = node.get_property(LoincPartProps.part_type_name)
      part_display = node.get_property(LoincPartProps.part_display_name)

      loinc_part.part_number = part_number
      loinc_part.part_name = part_name
      loinc_part.part_type_name = part_type
      loinc_part.part_display_name = part_display

  def load_linkml_schema(self, filename: t.Annotated[str, typer.Option('--file-name', '-f',
                                                                       help='The LinkML schema file name in the schema directory. For example: "comp_loinc.yaml"')],
      schema_name: t.Annotated[str, typer.Option('--schema-name', '-n',
                                                 help='A name to hold the loaded schema under. Defaults to the file name without the .yaml suffix')] = None,
      reload: t.Annotated[bool, typer.Option('--reload', '-r',
                                             help='A previously loaded schema under the same name will be reloaded if true.')] = False) -> SchemaView:
    typer.echo(f'Running load_linkml_schema')
    schema_view = self.runtime.load_linkml_schema(filename, schema_name, reload)
    self.runtime.current_schema_view = schema_view
    return schema_view

  def save_to_owl(self, file_path: t.Annotated[Path, typer.Option('--file', '-f',
                                                                  help='The output file path. If relative, it will be saved under the "output" directory in the runtime directory. '
                                                                       'If not given, it will be saved after the modul\'s name in the output directory.')] = None,
      schema_name: t.Annotated[str, typer.Option('--schema-name', '-s',
                                                 help='A loaded schema name to use while saving. If not provided, the "current schema" will be used.')] = None):

    typer.echo(f'Running save_to_owl')
    owl_dumper = OWLDumper()
    document = owl_dumper.to_ontology_document(schema=self.runtime.current_schema_view.schema,
                                               element=list(self.runtime.current_module.get_all_entities()))
    document.ontology.iri = funowl.identifiers.IRI(f'https://comploinc/{self.runtime.current_module.name}')
    owl_file_path = file_path
    if owl_file_path is None:
      owl_file_path = Path(self.runtime.current_module.name + '.owl')
    if not owl_file_path.is_absolute():
      owl_file_path = self.configuration.output  / owl_file_path

    owl_file_path.parent.mkdir(parents=True, exist_ok=True)
    typer.echo(f'Writing file: {owl_file_path}')
    with open(owl_file_path, 'w') as f:
      f.write(str(document))
