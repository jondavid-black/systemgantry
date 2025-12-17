from typing import List, Dict, Any
import re
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    JSON,
    Enum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql
from .schema import TableSchema, DataType


class SchemaGenerator:
    def __init__(self):
        self.metadata = MetaData()
        self.type_mapping = {
            DataType.INTEGER: Integer,
            DataType.STRING: String(255),
            DataType.BOOLEAN: Boolean,
            DataType.FLOAT: Float,
            DataType.TIMESTAMP: DateTime,
            DataType.JSON: JSON,
            # REFERENCE type is handled specially in create_table_from_schema
        }

    def create_table_from_schema(self, schema: TableSchema) -> Table:
        if schema.name in self.metadata.tables:
            return self.metadata.tables[schema.name]

        columns = []
        for col_def in schema.columns:
            col_type: Any
            if col_def.data_type == DataType.ENUM:
                if not col_def.enum_values:
                    raise ValueError(
                        f"Column {col_def.name} is of type ENUM but has no enum_values defined"
                    )
                # For SQLAlchemy Enum, we need to pass the allowed values
                # We also set the name of the enum type to avoid conflicts
                enum_name = (
                    col_def.enum_name
                    if col_def.enum_name
                    else f"{schema.name}_{col_def.name}_enum"
                )
                col_type = Enum(*col_def.enum_values, name=enum_name)
            elif col_def.data_type == DataType.REFERENCE:
                # For foreign keys, we need to know the type of the target column.
                # However, at this stage, we might not have the target table definition available.
                # We assume standard integer keys for now, or we could look up the target table if we had a registry.
                # Ideally, this would use the type of the referenced column.
                # For now, we'll default to Integer, but this is a simplification.
                col_type = Integer
            else:
                col_type = self.type_mapping[col_def.data_type]

            # Construct column arguments
            col_args: Dict[str, Any] = {
                "primary_key": col_def.primary_key,
                "nullable": col_def.nullable,
                "unique": col_def.unique,
            }

            if col_def.default is not None:
                col_args["server_default"] = col_def.default

            # Handle Foreign Key constraint
            if col_def.data_type == DataType.REFERENCE:
                if not col_def.reference_table:
                    raise ValueError(
                        f"Column {col_def.name} is of type REFERENCE but has no reference_table defined"
                    )

                ref_column = (
                    col_def.reference_column if col_def.reference_column else "id"
                )
                fk_constraint = ForeignKey(f"{col_def.reference_table}.{ref_column}")

                # We append the ForeignKey constraint to the column definition
                # Note: This is one way to define it. Alternatively we could add it to the Table args.
                column = Column(col_def.name, col_type, fk_constraint, **col_args)
            else:
                column = Column(col_def.name, col_type, **col_args)

            columns.append(column)

        # Build composite unique constraints
        args = [*columns]
        for unique_group in schema.composite_unique_constraints:
            args.append(UniqueConstraint(*unique_group))

        # Build table comment with metadata
        comment_parts = []
        if schema.description:
            comment_parts.append(schema.description)

        metadata_parts = [f"Category: {schema.category.value}"]

        if schema.namespace:
            metadata_parts.append(f"Namespace: {schema.namespace}")

        if schema.owner:
            metadata_parts.append(f"Owner: {schema.owner}")

        metadata_parts.append(f"Sensitivity: {schema.sensitivity.value}")

        metadata_parts.append(f"Retention: {schema.retention.value}")

        comment_parts.append(f"({', '.join(metadata_parts)})")

        comment = " ".join(comment_parts)

        return Table(schema.name, self.metadata, *args, comment=comment)

    def generate_ddl(self, tables: List[TableSchema]) -> str:
        """Generates SQL DDL for a list of table schemas."""
        ddl_statements = []
        for table_schema in tables:
            sa_table = self.create_table_from_schema(table_schema)
            # Use MySQL dialect as Dolt is MySQL compatible
            create_stmt = CreateTable(sa_table).compile(dialect=mysql.dialect())
            ddl_statements.append(str(create_stmt).strip() + ";")

        return "\n\n".join(ddl_statements)


class ProtobufGenerator:
    def __init__(self, package_name: str = "systemcatalyst"):
        self.package_name = package_name
        self.type_mapping = {
            DataType.INTEGER: "int32",
            DataType.STRING: "string",
            DataType.BOOLEAN: "bool",
            DataType.FLOAT: "float",
            DataType.TIMESTAMP: "google.protobuf.Timestamp",
            DataType.JSON: "string",  # Protobuf doesn't have native JSON, typically mapped to string
            # ENUM and REFERENCE handled dynamically
        }

    def generate_proto(self, tables: List[TableSchema]) -> str:
        """Generates Protobuf definitions for a list of table schemas."""
        lines = ['syntax = "proto3";', f"package {self.package_name};", ""]

        # Check if we need to import Timestamp
        has_timestamp = any(
            col.data_type == DataType.TIMESTAMP
            for table in tables
            for col in table.columns
        )
        if has_timestamp:
            lines.append('import "google/protobuf/timestamp.proto";')
            lines.append("")

        for table in tables:
            # Handle Enums first
            for col in table.columns:
                if col.data_type == DataType.ENUM:
                    if not col.enum_values:
                        raise ValueError(
                            f"Column {col.name} is of type ENUM but has no enum_values defined"
                        )

                    enum_name = col.enum_name or f"{table.name}_{col.name}_enum"
                    # Protobuf enum conventions typically UpperCamelCase
                    # Handle snake_case to CamelCase conversion safely
                    if "_" in enum_name:
                        enum_name = "".join(
                            part[:1].upper() + part[1:]
                            for part in enum_name.split("_")
                            if part
                        )
                    else:
                        # Ensure first letter is uppercase, preserve rest
                        enum_name = enum_name[:1].upper() + enum_name[1:]

                    lines.append(f"enum {enum_name} {{")
                    # Protobuf enums must start with 0.
                    # Convention: ENUM_NAME_VALUE_NAME
                    # We need to transform the enum name from CamelCase to UPPER_SNAKE_CASE for the prefix
                    # This regex finds the boundary where a lower case letter is followed by an upper case letter
                    # or numbers and inserts an underscore.
                    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", enum_name)
                    prefix = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).upper()

                    # Convert values to upper snake case for the keys
                    # e.g. "in_progress" -> "IN_PROGRESS"
                    for idx, val in enumerate(col.enum_values):
                        # Ensure safe identifier
                        safe_val = val.upper().replace(" ", "_").replace("-", "_")
                        lines.append(f"  {prefix}_{safe_val} = {idx};")

                    lines.append("}")
                    lines.append("")

            # Generate Message
            # Use UpperCamelCase for message name
            msg_name = "".join(x.capitalize() for x in table.name.split("_"))
            lines.append(f"message {msg_name} {{")

            for idx, col in enumerate(table.columns, 1):
                field_type = "string"  # Default fallback

                if col.data_type == DataType.ENUM:
                    enum_name = col.enum_name or f"{table.name}_{col.name}_enum"
                    if "_" in enum_name:
                        enum_name = "".join(
                            part[:1].upper() + part[1:]
                            for part in enum_name.split("_")
                            if part
                        )
                    else:
                        enum_name = enum_name[:1].upper() + enum_name[1:]
                    field_type = enum_name

                elif col.data_type == DataType.REFERENCE:
                    # For references, we typically use the ID type of the referenced table
                    # Defaulting to int32 as a safe bet for now, similar to SchemaGenerator
                    field_type = "int32"
                else:
                    field_type = self.type_mapping.get(col.data_type, "string")

                lines.append(f"  {field_type} {col.name} = {idx};")

            lines.append("}")
            lines.append("")

        return "\n".join(lines)
