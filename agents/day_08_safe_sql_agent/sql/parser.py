"""SQL statement parser and component extractor."""

import sqlglot
from sqlglot import expressions


def parse_sql(sql: str):

    statements = sqlglot.parse(
        sql,
        read="postgres",
    )

    if len(statements) != 1:
        raise ValueError(
            "Only one SQL statement is allowed."
        )

    return statements[0]

def get_statement_type(expression):

    return expression.key.upper()