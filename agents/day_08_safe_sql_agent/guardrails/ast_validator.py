"""Abstract Syntax Tree (AST) validator for SQL queries."""

from dataclasses import dataclass, field
from sqlglot import expressions
from agents.day_08_safe_sql_agent.guardrails.policies import (
    ALLOWED_STATEMENTS,
    FORBIDDEN_SCHEMAS,
    FORBIDDEN_FUNCTIONS,
    MAX_LIMIT,
)

@dataclass
class ValidationResult:
    allowed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, message: str):
        self.allowed = False
        self.errors.append(message)


def validate_statement_type(ast, result):
    if not hasattr(ast, "key") or not ast.key:
        result.add_error("Invalid or empty SQL statement.")
        return

    statement_type = ast.key.upper()
               
    if statement_type not in ALLOWED_STATEMENTS:
        result.add_error(f"Statement type '{statement_type}' is not allowed.")


def validate_tables(ast, schema, result):

    allowed_tables = set(schema.keys())

    tables = ast.find_all(expressions.Table)

    for table in tables:
        table_name = table.name

        if table_name not in allowed_tables:
            result.add_error(
                f"Table '{table_name}' is not allowed."
            )

def validate_table_schemas(ast, result):

    tables = ast.find_all(expressions.Table)

    for table in tables:

        db = table.args.get("db")

        if db:
            schema_name = db.name.lower()

            if schema_name in FORBIDDEN_SCHEMAS:
                result.add_error(
                    f"Access to schema '{schema_name}' is forbidden."
                )


def build_column_map(schema):

    return {
        table_name: {
            column["name"]
            for column in table_info["columns"]
        }
        for table_name, table_info in schema.items()
    }



def build_select_alias_set(ast):
    aliases = set()
    for select in ast.find_all(expressions.Select):
        for expression in select.expressions:
            if isinstance(expression, expressions.Alias):
                aliases.add(expression.alias)
    return aliases


def validate_columns(ast, schema, result):

    column_map = build_column_map(schema)
    aliases = build_table_alias_map(ast)
    select_aliases = build_select_alias_set(ast)

    referenced_tables = [
        aliases.get(table.name, table.name)
        for table in ast.find_all(expressions.Table)
        if aliases.get(table.name, table.name) in column_map
    ]

    for column in ast.find_all(expressions.Column):

        column_name = column.name
        table_name = column.table

        # Skip column alias references (e.g., ORDER BY total_order_value)
        if not table_name and column_name in select_aliases:
            continue

        if table_name:

            actual_table = aliases.get(
                table_name,
                table_name
            )

            if actual_table not in column_map:
                result.add_error(
                    f"Unknown table '{actual_table}'."
                )
                continue

            if column_name not in column_map[actual_table]:
                result.add_error(
                    f"Column '{actual_table}.{column_name}' "
                    f"does not exist."
                )
        else:
            if referenced_tables:
                found = any(column_name in column_map[t] for t in referenced_tables)
                if not found:
                    result.add_error(
                        f"Column '{column_name}' does not exist."
                    )

def build_table_alias_map(ast):

    aliases = {}

    for table in ast.find_all(expressions.Table):

        table_name = table.name
        alias = table.alias

        if alias:
            aliases[alias] = table_name

    return aliases




def validate_limit(ast, result):

    limit = ast.args.get("limit")

    if limit is None:
        result.add_error(
            "LIMIT clause is required."
        )
        return

    expression = limit.expression

    if not isinstance(expression, expressions.Literal):
        result.add_error(
            "LIMIT must be a constant integer."
        )
        return

    if not expression.is_int:
        result.add_error(
            "LIMIT must be an integer."
        )
        return

    value = int(expression.this)

    if value <= 0:
        result.add_error(
            "LIMIT must be greater than zero."
        )

    if value > MAX_LIMIT:
        result.add_error(
            f"LIMIT cannot exceed {MAX_LIMIT}."
        )

def validate_functions(ast, result):

    for node in ast.find_all((expressions.Func, expressions.Anonymous)):

        func_name = getattr(node, "name", "") or node.sql_name()
        func_name = func_name.upper()

        if func_name in FORBIDDEN_FUNCTIONS:
            result.add_error(
                f"Function '{func_name}' is not allowed."
            )



def validate_sql(ast, schema):

    result = ValidationResult()

    validate_statement_type(
        ast,
        result
    )

    validate_tables(
        ast,
        schema,
        result
    )

    validate_table_schemas(
        ast,
        result
    )

    validate_columns(
        ast,
        schema,
        result
    )

    validate_limit(
        ast,
        result
    )

    validate_functions(
        ast,
        result
    )

    return result