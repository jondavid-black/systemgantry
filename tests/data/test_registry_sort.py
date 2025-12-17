import pytest
from src.data.schema import TableSchema, ColumnSchema, DataType
from src.data.registry import SchemaRegistry


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


def test_topological_sort(registry, user_schema, post_schema):
    # Posts depend on Users
    registry.register(post_schema)
    registry.register(user_schema)

    ordered = registry.get_ordered_schemas()
    names = [s.name for s in ordered]

    # Users must come before Posts
    assert names.index("users") < names.index("posts")


def test_circular_dependency_error(registry):
    t1 = TableSchema(
        name="t1",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="ref", data_type=DataType.REFERENCE, reference_table="t2"
            ),
        ],
    )
    t2 = TableSchema(
        name="t2",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="ref", data_type=DataType.REFERENCE, reference_table="t1"
            ),
        ],
    )
    registry.register(t1)
    registry.register(t2)

    with pytest.raises(ValueError) as exc:
        registry.get_ordered_schemas()
    assert "Circular dependency" in str(exc.value)


def test_self_reference_ignored(registry):
    # A category table that has a parent_id referencing itself
    cat_schema = TableSchema(
        name="categories",
        columns=[
            ColumnSchema(name="id", data_type=DataType.INTEGER, primary_key=True),
            ColumnSchema(
                name="parent_id",
                data_type=DataType.REFERENCE,
                reference_table="categories",
            ),
        ],
    )
    registry.register(cat_schema)
    ordered = registry.get_ordered_schemas()
    assert len(ordered) == 1
    assert ordered[0].name == "categories"
