"""Database schema extraction and introspection utilities."""
from agents.day_08_safe_sql_agent.database.connection import get_connection

def get_tables():
    query= """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    ORDER BY table_name;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return [row[0] for row in rows]


def get_columns(table_name: str = None):
    if table_name:
        query = """
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position, table_name;
        """
        params = (table_name,)
    else:
        query = """
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY ordinal_position, table_name;
        """
        params = ()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

    return [
        {
            "table": row[0],
            "column": row[1],
            "type": row[2],
            "nullable": row[3] == "YES"

        }
        for row in rows
    ]

    

def get_relationships():
    query = """
        SELECT
            tc.table_name AS source_table,
            kcu.column_name AS source_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = 'public';
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return [
        {
            "source_table": row[0],
            "source_column": row[1],
            "target_table": row[2],
            "target_column": row[3],
        }
        for row in rows
    ]

DEMO_SCHEMA = {
    "customers": {
        "columns": [
            {"name": "id", "type": "integer", "nullable": False},
            {"name": "name", "type": "varchar", "nullable": False},
            {"name": "email", "type": "varchar", "nullable": True},
        ],
        "relationships": [],
    },
    "orders": {
        "columns": [
            {"name": "id", "type": "integer", "nullable": False},
            {"name": "customer_id", "type": "integer", "nullable": False},
            {"name": "total_amount", "type": "numeric", "nullable": False},
            {"name": "created_at", "type": "timestamp", "nullable": False},
        ],
        "relationships": [
            {"column": "customer_id", "references": "customers.id"}
        ],
    },
}

def get_schema():
    try:
        tables = get_tables()
        columns = get_columns()
        relationships = get_relationships()

        schema = {}

        for table in tables:
            schema[table] = {
                "columns": [],
                "relationships": [],
            }

        for column in columns:
            if column["table"] in schema:
                schema[column["table"]]["columns"].append({
                    "name": column["column"],
                    "type": column["type"],
                    "nullable": column["nullable"],
                })

        for relationship in relationships:
            source_table = relationship["source_table"]

            if source_table in schema:
                schema[source_table]["relationships"].append({
                    "column": relationship["source_column"],
                    "references": (
                        f"{relationship['target_table']}."
                        f"{relationship['target_column']}"
                    ),
                })

        return schema
    except Exception:
        return DEMO_SCHEMA


def format_schema(schema: dict) -> str:
    lines = ["DATABASE SCHEMA", ""]

    for table_name, table_info in schema.items():
        lines.append(f"TABLE: {table_name}")
        lines.append("COLUMNS:")

        for column in table_info["columns"]:
            nullable = "" if column["nullable"] else " NOT NULL"

            lines.append(
                f"  - {column['name']}: "
                f"{column['type']}{nullable}"
            )

        lines.append("")

        for relationship in table_info["relationships"]:
            lines.append(
                "RELATIONSHIP: "
                f"{table_name}.{relationship['column']} "
                f"→ {relationship['references']}"
            )

        lines.append("")

    return "\n".join(lines)