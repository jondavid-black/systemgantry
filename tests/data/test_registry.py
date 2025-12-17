import pytest
from src.data.schema import TableSchema, ColumnSchema, DataType
from src.data.registry import SchemaRegistry
from src.data.storage import YAMLStorage


@pytest.fixture
def registry():
    return SchemaRegistry()


@pytest.fixture
def user_schema():
    return TableSchema(
        name="users",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(name="name", data_type=DataType.STRING),
        ],
    )


@pytest.fixture
def post_schema():
    return TableSchema(
        name="posts",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="user_id",
                data_type=DataType.REFERENCE,
                reference_table="users",
                reference_column="id",
            ),
            ColumnSchema(name="content", data_type=DataType.STRING),
        ],
    )


def test_register_and_get(registry, user_schema):
    registry.register(user_schema)
    assert registry.get_schema("users") == user_schema
    assert len(registry.list_schemas()) == 1


def test_duplicate_registration_error(registry, user_schema):
    registry.register(user_schema)
    with pytest.raises(ValueError):
        registry.register(user_schema)


def test_validation_success(registry, user_schema, post_schema):
    registry.register(user_schema)
    registry.register(post_schema)
    assert registry.validate() == []


def test_validation_missing_table(registry, post_schema):
    registry.register(post_schema)
    errors = registry.validate()
    assert len(errors) == 1
    assert "References unknown table 'users'" in errors[0]


def test_validation_missing_column(registry, user_schema):
    bad_schema = TableSchema(
        name="bad",
        columns=[
            ColumnSchema(
                name="ref",
                data_type=DataType.REFERENCE,
                reference_table="users",
                reference_column="missing_col",
            )
        ],
    )
    registry.register(user_schema)
    registry.register(bad_schema)
    errors = registry.validate()
    assert len(errors) == 1
    assert "References unknown column 'missing_col'" in errors[0]


def test_resolve_datatype(registry, user_schema, post_schema):
    registry.register(user_schema)
    registry.register(post_schema)

    # Direct resolution
    assert registry.resolve_target_datatype("users", "id") == DataType.INTEGER

    # Reference resolution
    assert registry.resolve_target_datatype("posts", "user_id") == DataType.INTEGER


def test_load_from_directory(registry, tmp_path, user_schema):
    # Create a temporary YAML file
    storage = YAMLStorage()
    schema_file = tmp_path / "test_schema.yaml"

    # Convert Pydantic model to dict for storage
    # We use model_dump if using Pydantic V2, or dict() for V1.
    # Assuming V2 based on context, but let's check basic dict dump.
    # Note: .dict() is deprecated in V2 but usually still present, .model_dump() is preferred.
    # Let's try to serialize properly using pydantic's helpers if needed,
    # but for now passing the dict representation to the storage is enough.
    # To be safe with potential Enum serialization issues in simple dict(), we'll trust the storage or pydantic.
    # Simple dict dump often leaves Enums as objects.

    # For robust test serialization let's construct the dict manually or trust storage handles objects.
    # Our YAMLStorage uses ruamel.yaml which might need help with Enums if not careful.
    # However, let's just write the raw dict structure that matches our schema.

    schema_data = {
        "name": "users",
        "columns": [
            {"name": "id", "data_type": "integer", "primary_key": True},
            {"name": "name", "data_type": "string"},
        ],
    }

    storage.save(schema_data, schema_file)

    registry.load_from_directory(tmp_path)
    loaded = registry.get_schema("users")
    assert loaded is not None
    assert loaded.name == "users"
    assert len(loaded.columns) == 2
