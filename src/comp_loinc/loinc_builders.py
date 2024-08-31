import typing as t
from pathlib import Path

import funowl
import typer
from linkml_owl.dumpers.owl_dumper import OWLDumper
from linkml_runtime import SchemaView

from comp_loinc import Runtime
from comp_loinc.datamodel.comp_loinc_v2 import LoincTerm
from loinclib.loinc_loader_v2 import LoincLoader
from loinclib.loinc_schema_v2 import LoincNodeType, LoincTermProps


class LoincBuilders:

  def __init__(self, runtime: Runtime):
    self.runtime = runtime

  def setup_builder_cli_all(self):
    self.runtime.builder.cli.command('lt-inst-all', help='Instantiate all LOINC terms into current module.')(
        self.lt_inst_all)
    self.runtime.builder.cli.command('load-schema', help='Loads a LinkML schema file and gives it a name. '
                                                         'It also makes it the "current" schema to operate on with schema related builder steps.')(
        self.load_linkml_schema)
    self.runtime.builder.cli.command('save-owl', help='Saves the current module to an owl file.')(self.save_to_owl)

  def lt_inst_all(self):
    typer.echo(f'Running lt_inst_all')
    graph = self.runtime.graph
    loinc_loader = LoincLoader(graph=graph, home_path=self.runtime.home_path,
                               config=self.runtime.config)
    loinc_loader.load_loinc_table__loinc_csv()
    for node in self.runtime.graph.get_nodes(LoincNodeType.LoincTerm):
      props = node.get_properties()
      loinc_number = props[LoincTermProps.loinc_number]
      if self.runtime.current_module.get_entity(loinc_number, LoincTerm) is None:
        loinc_term = LoincTerm(id=loinc_number)
        loinc_term.loinc_number = loinc_number
        self.runtime.current_module.add_entity(loinc_term)

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
      owl_file_path = self.runtime.home_path / 'output' / owl_file_path

    owl_file_path.parent.mkdir(parents=True, exist_ok=True)
    typer.echo(f'Writing file: {owl_file_path}')
    with open(owl_file_path, 'w') as f:
      f.write(str(document))
