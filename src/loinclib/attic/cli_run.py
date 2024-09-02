import sys

from comp_loinc import cli

sys.argv = ['cli_run',

            'builder',
            'set-module', '--name', 'test',
            'lt-inst-all',
            'load-schema',  '-f', 'comp_loinc_v2.yaml',
            'save-owl',

            # '--help'
            ]



# sys.argv = ['cli_run',
#
#             'builder',
#             'load-schema',
#             'set-module', '--name', 'test',
#             'lt-inst-all',
#             'load-schema', # '-f', 'comp_loinc_v2.yaml',
#              'save-owl',
#
#             '--help'
#             ]

cli()