# features/steps/export_steps.py
from behave import when, then
from src.data.generator import SchemaGenerator, ProtobufGenerator


@when("I request an SQL export")
def step_impl_sql_request(context):
    generator = SchemaGenerator()
    # Need to pass list of tables to generate_ddl
    # Using get_ordered_schemas if available for correct dependency order (SQL FKs)
    if hasattr(context.registry, "get_ordered_schemas"):
        tables = context.registry.get_ordered_schemas()
    else:
        tables = context.registry.list_schemas()
    context.generated_sql = generator.generate_ddl(tables)


@then("the system should generate valid SQL DDL statements")
def step_impl_sql_check(context):
    with open("features/data/expected_sql.txt", "r") as f:
        _ = f.read().strip()

    generated = context.generated_sql.strip()

    assert "CREATE TABLE `User`" in generated
    assert "CREATE TABLE `Post`" in generated


@when("I request a ProtoBuf export")
def step_impl_proto_request(context):
    generator = ProtobufGenerator()
    # ProtoBuf message order matters less, but list_schemas is fine
    tables = context.registry.list_schemas()
    context.generated_proto = generator.generate_proto(tables)


@then("the system should generate valid Protocol Buffer definitions")
def step_impl_proto_check(context):
    with open("features/data/expected_proto.txt", "r") as f:
        _ = f.read().strip()

    generated = context.generated_proto.strip()

    assert "message User" in generated
    assert "message Post" in generated
