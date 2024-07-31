from pathlib import Path

import typer
import pickle
import typing as t

LOINC_RELEASE_DIR_NAME = 'loinc_release'
LOINC_TREES_DIR_NAME = 'loinc_trees'

COMPLOINC_OUT_DIR_NAME = 'comploinc_out'

class CompLoincCli2:

    def __init__(self):
        self.cli = typer.Typer()
        self.cli.callback(invoke_without_command=True)(self.callback)

    def callback(self, *,
                 work_dir: t.Annotated[t.Optional[Path], typer.Option(help='CompLOINC work directory.')] = Path.cwd(),
                 loinc_release: t.Annotated[t.Optional[Path], typer.Option(
                     help=f'Path to a directory containing an unpacked LOINC release. Defaults to: ./{LOINC_RELEASE_DIR_NAME}')] = None,
                 pickled_path: t.Annotated[t.Optional[Path], typer.Option(help='Path to an already pickled loinclib graph.')] = None,
                 to_pickle_path: t.Annotated[t.Optional[Path], typer.Option(help='A path to which  the loinclib Graph will be saved to.')] = None,
                 ):


        typer.echo("Callback 2 called.")

        if not work_dir.exists():
            raise ValueError(f'Work directory: {work_dir} does not exist.')
        self.work_dir = work_dir.absolute()




cli = CompLoincCli2().cli
