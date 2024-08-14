import os
import pathlib
import comp_loinc.main as main
from loinclib.enums import  NameSpace


print(main.get_latest_loinc_release())
print(main.get_latest_trees())

print(NameSpace.chebi.owl_url('chebi:123'))




