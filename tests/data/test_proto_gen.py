from src.data.schema import TableSchema, ColumnSchema, DataType
from src.data.generator import ProtobufGenerator


def test_generate_simple_proto():
    table = TableSchema(
        name="User",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(name="username", data_type=DataType.STRING),
            ColumnSchema(name="email", data_type=DataType.STRING),
            ColumnSchema(name="is_active", data_type=DataType.BOOLEAN),
            ColumnSchema(name="score", data_type=DataType.FLOAT),
        ],
    )

    generator = ProtobufGenerator()
    proto_output = generator.generate_proto([table])

    expected_lines = [
        'syntax = "proto3";',
        "package systemcatalyst;",
        "",
        "message User {",
        "  int32 id = 1;",
        "  string username = 2;",
        "  string email = 3;",
        "  bool is_active = 4;",
        "  float score = 5;",
        "}",
    ]

    for line in expected_lines:
        assert line in proto_output


def test_generate_proto_with_timestamp():
    table = TableSchema(
        name="Event",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(name="created_at", data_type=DataType.TIMESTAMP),
        ],
    )

    generator = ProtobufGenerator()
    proto_output = generator.generate_proto([table])

    assert 'import "google/protobuf/timestamp.proto";' in proto_output
    assert "google.protobuf.Timestamp created_at = 2;" in proto_output


def test_generate_proto_with_enum():
    table = TableSchema(
        name="Task",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="status",
                data_type=DataType.ENUM,
                enum_values=["TODO", "IN_PROGRESS", "DONE"],
                enum_name="TaskStatus",
            ),
        ],
    )

    generator = ProtobufGenerator()
    proto_output = generator.generate_proto([table])

    assert "enum TaskStatus {" in proto_output
    assert "TASK_STATUS_TODO = 0;" in proto_output
    assert "TASK_STATUS_IN_PROGRESS = 1;" in proto_output
    assert "TaskStatus status = 2;" in proto_output


def test_generate_proto_multiple_tables():
    user = TableSchema(
        name="User", columns=[ColumnSchema(name="id", data_type=DataType.INTEGER)]
    )
    post = TableSchema(
        name="Post", columns=[ColumnSchema(name="id", data_type=DataType.INTEGER)]
    )

    generator = ProtobufGenerator()
    proto_output = generator.generate_proto([user, post])

    assert "message User {" in proto_output
    assert "message Post {" in proto_output


def test_generate_proto_complex_types():
    table = TableSchema(
        name="ComplexData",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(name="metadata", data_type=DataType.JSON),
            ColumnSchema(
                name="parent_id",
                data_type=DataType.REFERENCE,
                reference_table="ParentTable",
                reference_column="id",
            ),
        ],
    )

    generator = ProtobufGenerator()
    proto_output = generator.generate_proto([table])

    # JSON should be mapped to string
    assert "string metadata = 2;" in proto_output
    # REFERENCE should be mapped to int32 (default assumption)
    assert "int32 parent_id = 3;" in proto_output
