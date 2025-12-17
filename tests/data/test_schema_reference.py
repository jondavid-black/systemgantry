import pytest
from sqlalchemy.dialects import mysql

from src.data.schema import TableSchema, ColumnSchema, DataType
from src.data.generator import SchemaGenerator


def dump(sql, *multiparams, **params):
    print(sql.compile(dialect=mysql.dialect()))


def test_reference_column_generation():
    # Define a simple user table schema (the referenced table)
    user_schema = TableSchema(
        name="users",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(name="name", data_type=DataType.STRING),
        ],
    )

    # Define an order table schema with a reference to users
    order_schema = TableSchema(
        name="orders",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="user_id",
                data_type=DataType.REFERENCE,
                reference_table="users",
                reference_column="id",
            ),
            ColumnSchema(name="amount", data_type=DataType.FLOAT),
        ],
    )

    generator = SchemaGenerator()

    # Generate the table object
    order_table = generator.create_table_from_schema(order_schema)

    # Verify the table structure
    assert order_table.name == "orders"
    assert len(order_table.columns) == 3

    # Check the foreign key column
    fk_column = order_table.columns["user_id"]
    assert len(fk_column.foreign_keys) == 1
    fk = list(fk_column.foreign_keys)[0]
    assert fk.target_fullname == "users.id"

    # Verify DDL generation
    ddl = generator.generate_ddl([user_schema, order_schema])
    assert "FOREIGN KEY(user_id) REFERENCES users (id)" in ddl


def test_missing_reference_table_error():
    # Schema with missing reference_table
    bad_schema = TableSchema(
        name="bad_table",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="ref_col",
                data_type=DataType.REFERENCE,
                # reference_table is missing
            ),
        ],
    )

    generator = SchemaGenerator()

    with pytest.raises(ValueError) as excinfo:
        generator.create_table_from_schema(bad_schema)

    assert (
        "Column ref_col is of type REFERENCE but has no reference_table defined"
        in str(excinfo.value)
    )
