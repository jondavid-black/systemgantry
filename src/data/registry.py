from typing import Dict, Optional, List
from pathlib import Path
from .schema import TableSchema, DataType
from .storage import YAMLStorage


class SchemaRegistry:
    """
    Central registry for all table schemas.
    Handles registration, retrieval, and dependency resolution for schema definitions.
    """

    def __init__(self):
        self._schemas: Dict[str, TableSchema] = {}
        self._storage = YAMLStorage()

    def register(self, schema: TableSchema) -> None:
        """Register a new table schema."""
        if schema.name in self._schemas:
            raise ValueError(f"Schema for table '{schema.name}' already exists")
        self._schemas[schema.name] = schema

    def clear(self) -> None:
        """Clear all registered schemas."""
        self._schemas.clear()

    def get_schema(self, name: str) -> Optional[TableSchema]:
        """Retrieve a schema by table name."""
        return self._schemas.get(name)

    def list_schemas(self) -> List[TableSchema]:
        """List all registered schemas."""
        return list(self._schemas.values())

    def load_from_directory(self, directory: Path | str) -> None:
        """
        Load all YAML schema definitions from a directory.
        Expects files to be valid YAML matching the TableSchema structure.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Support both .yaml and .yml extensions
        files = list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))

        for file_path in files:
            try:
                data = self._storage.load(file_path)
                # Ensure we handle both single schema dicts and lists of schemas
                if isinstance(data, list):
                    for item in data:
                        self.register(TableSchema(**item))
                elif isinstance(data, dict):
                    self.register(TableSchema(**data))
            except Exception as e:
                # We log/print here but might want to aggregate errors in the future
                print(f"Failed to load schema from {file_path}: {e}")
                raise e

    def resolve_target_datatype(self, table_name: str, column_name: str) -> DataType:
        """
        Resolves the actual physical DataType of a column.
        If the column is a REFERENCE, it recursively looks up the target.
        """
        schema = self.get_schema(table_name)
        if not schema:
            raise ValueError(f"Table '{table_name}' not found in registry")

        # Find the column
        target_col = next((c for c in schema.columns if c.name == column_name), None)
        if not target_col:
            raise ValueError(
                f"Column '{column_name}' not found in table '{table_name}'"
            )

        # If it's a primitive, return it
        if target_col.data_type != DataType.REFERENCE:
            return target_col.data_type

        # If it's a reference, recurse
        if not target_col.reference_table:
            raise ValueError(
                f"Column '{table_name}.{column_name}' is a REFERENCE but lacks reference_table"
            )

        ref_col_name = target_col.reference_column or "id"

        # Prevent infinite recursion (basic check)
        if target_col.reference_table == table_name:
            raise ValueError(
                f"Circular reference detected on '{table_name}.{column_name}'"
            )

        return self.resolve_target_datatype(target_col.reference_table, ref_col_name)

    def validate(self) -> List[str]:
        """
        Validates the integrity of the registry.
        Returns a list of error messages (empty if valid).
        """
        errors = []
        for table_name, schema in self._schemas.items():
            for col in schema.columns:
                if col.data_type == DataType.REFERENCE:
                    if not col.reference_table:
                        errors.append(
                            f"{table_name}.{col.name}: Missing reference_table"
                        )
                        continue

                    target_schema = self.get_schema(col.reference_table)
                    if not target_schema:
                        errors.append(
                            f"{table_name}.{col.name}: References unknown table '{col.reference_table}'"
                        )
                        continue

                    target_col_name = col.reference_column or "id"
                    target_col = next(
                        (c for c in target_schema.columns if c.name == target_col_name),
                        None,
                    )

                    if not target_col:
                        errors.append(
                            f"{table_name}.{col.name}: References unknown column '{target_col_name}' in '{col.reference_table}'"
                        )
        return errors

    def get_ordered_schemas(self) -> List[TableSchema]:
        """
        Returns schemas topologically sorted based on foreign key dependencies.
        Raises ValueError if a cycle is detected.
        """
        visited = set()
        temp_marked = set()
        order = []

        def visit(name: str):
            if name in temp_marked:
                raise ValueError(
                    f"Circular dependency detected involving table '{name}'"
                )
            if name in visited:
                return

            temp_marked.add(name)
            schema = self._schemas[name]

            # Find dependencies (tables referenced by this table)
            dependencies = set()
            for col in schema.columns:
                if col.data_type == DataType.REFERENCE and col.reference_table:
                    # Self-references don't constrain creation order (usually handled by alter,
                    # but here we just ignore for topological sort as we can create the table then add constraint.
                    # However, strictly speaking, for CREATE TABLE, we need the parent first.)
                    # If it's a self-reference, we don't treat it as a topological dependency
                    # that must precede this table, because that's impossible.
                    if col.reference_table != name:
                        dependencies.add(col.reference_table)

            for dep in dependencies:
                if dep in self._schemas:  # Only care about dependencies we know about
                    visit(dep)

            temp_marked.remove(name)
            visited.add(name)
            order.append(schema)

        # Sort keys to ensure deterministic order for independent nodes
        for name in sorted(self._schemas.keys()):
            if name not in visited:
                visit(name)

        return order
