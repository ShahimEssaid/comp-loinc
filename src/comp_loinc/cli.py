from __future__ import annotations

import typing as t
from pathlib import Path

import typer

from comp_loinc import Runtime
from comp_loinc.loinc_builders import LoincBuilders

LOINC_RELEASE_DIR_NAME = 'loinc_release'
LOINC_TREES_DIR_NAME = 'loinc_trees'

COMPLOINC_OUT_DIR_NAME = 'comploinc_out'


class CompLoincCli:

  def __init__(self):
    self.runtime = Runtime()
    self.cli = typer.Typer()
    self.cli.callback(invoke_without_command=True)(self.callback)
    self.work_dir = None

    self.cli.add_typer(self.runtime.builder.cli, name='builder')

    self.loinc_builders = LoincBuilders(self.runtime)
    self.loinc_builders.setup_builder_cli_all()

  def callback(self, *,
      work_dir: t.Annotated[t.Optional[Path], typer.Option(
          help='CompLOINC work directory, defaults to current work directory.'
          , default_factory=Path.cwd)],
      graph_path: t.Annotated[t.Optional[Path], typer.Option(
          help='Pickled graph path, relative to current work directory path')] = None,

      loinc_release: t.Annotated[t.Optional[Path], typer.Option(
          help=f'Path to a directory containing an unpacked LOINC release. Defaults to: ./{LOINC_RELEASE_DIR_NAME}')] = None,
      pickled_path: t.Annotated[t.Optional[Path], typer.Option(
          help='Path to an already pickled loinclib graph.')] = None,
      to_pickle_path: t.Annotated[t.Optional[Path], typer.Option(
          help='A path to which  the loinclib Graph will be saved to.')] = None,

  ):
    self.work_dir = work_dir.absolute()
    if not self.work_dir.exists():
      raise ValueError(f'Work directory: {self.work_dir} does not exist.')


cli = CompLoincCli().cli

