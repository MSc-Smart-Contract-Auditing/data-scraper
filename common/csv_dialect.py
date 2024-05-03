import csv

DIALECT_NAME = "db_dialect"

csv.register_dialect(
    DIALECT_NAME,
    delimiter=",",  # Use comma as the delimiter
    quoting=csv.QUOTE_MINIMAL,  # Quote fields that contain special characters
    quotechar='"',  # Use double quotes for quoting fields
    escapechar="\\",  # Use backslash to escape quote characters inside fields
)


def get_dialect():
    return DIALECT_NAME
