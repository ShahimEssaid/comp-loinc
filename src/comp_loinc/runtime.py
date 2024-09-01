import typing as t
from pathlib import Path

import linkml_runtime
import typer
import yaml
from linkml_runtime import SchemaView

from loinclib import LoinclibGraph
from loinclib.loinc_loader import LoincLoader


class Runtime:
  def __init__(self, *, home_path: Path = Path.cwd(), pickled_graph_path: Path = None, config_path: Path = None, ):
    self.home_path = home_path.absolute()
    self.pickled_graph_path = pickled_graph_path

    if config_path:
      self.config_path = config_path.absolute()
    else:
      self.config_path = self.home_path / 'comploinc_config.yaml'

    self.config = None
    if self.config_path.exists():
      with open(self.config_path, 'r') as f:
        self.config = yaml.safe_load(f)

    self.graph = LoinclibGraph(graph_path=self.pickled_graph_path)
    self.builder = Builder(self)

    from comp_loinc.module import Module
    self.modules: t.Dict[str, Module] = dict()
    self.current_module: t.Optional[Module] = None

    self.schema_views: t.Dict[str, SchemaView] = dict()
    self.current_schema_view: t.Optional[SchemaView] = None

    self.__loinc_release_loader: t.Optional[LoincLoader] = None

  def get_loinc_release_loader(self):
    if self.__loinc_release_loader is None:
      release_path = self.get_loinc_release_path()
      self.__loinc_release_loader = LoincLoader(release_path=release_path, runtime=self)
    return self.__loinc_release_loader

  def load_linkml_schema(self, file_name: str, as_name: str = None, reload: bool = False) -> SchemaView:
    from comp_loinc import schemas_path
    if as_name is None:
      as_name = file_name.removesuffix('.yaml')

    current_view = self.schema_views.get(as_name, None)
    if current_view and not reload:
      file = current_view.schema.source_file
      raise ValueError(f'Schema view for name: {as_name} already loaded from file: {file}')

    schema_path = schemas_path / file_name
    if schema_path.exists():
      schema_view = linkml_runtime.SchemaView(schema_path)
      self.schema_views[as_name] = schema_view
      return schema_view
    else:
      raise ValueError(f'Schema file {schema_path} does not exist while trying to load as name: {as_name}')


class Builder:

  def __init__(self, runtime: Runtime):
    self.runtime = runtime

    self.cli = typer.Typer(chain=True)
    self.cli.callback(invoke_without_command=True)(self.callback)

    self.cli.command('set-module')(self.set_current_module)

  def callback(self):
    pass

  def set_current_module(self, name: t.Annotated[str, typer.Option(help='Set the current module to this name.')]):
    from comp_loinc.module import Module
    if name not in self.runtime.modules:
      self.runtime.modules[name] = Module(name=name, runtime=self.runtime)
    self.runtime.current_module = self.runtime.modules[name]
