from enum import StrEnum

from loinclib.schema_v2 import Schema


class LoincNodeEnum(StrEnum):
    LoincTerm = 'loinc_term'
    LoincPart = 'loinc_part'


class LoincEdgeEnum(StrEnum):
    pass


class LoincPropertyEnum(StrEnum):
    pass


loinc_schema: Schema = Schema()

