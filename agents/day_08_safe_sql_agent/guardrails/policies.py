"""Security policies and query restrictions."""

ALLOWED_STATEMENTS = {
    "SELECT",
}

MAX_LIMIT = 1000

FORBIDDEN_FUNCTIONS = {
    "PG_READ_FILE",
    "PG_WRITE_FILE",
    "PG_LS_DIR",
    "DBLINK",
}

FORBIDDEN_SCHEMAS = {
    "pg_catalog",
    "information_schema",
    "pg_toast",
}