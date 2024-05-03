import csv

DIALECT_NAME = "ch_dialect"

csv.register_dialect(
    "ch_dialect",
    delimiter="ч",
    quoting=csv.QUOTE_NONE,
    escapechar="\\",
)


def get_dialect():
    return DIALECT_NAME
