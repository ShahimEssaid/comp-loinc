from sys import argv, orig_argv

from comp_loinc.cli import comploinc_file_cli

argv.append('comploinc_files/term-annotations.txt')

comploinc_file_cli()
