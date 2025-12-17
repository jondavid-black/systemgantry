# features/steps/registry_steps.py
from behave import given, then
from src.data.registry import SchemaRegistry
import os
from pathlib import Path


@given('a valid YAML schema definition file "{filename}"')
def step_impl_load_schema(context, filename):
    context.registry = SchemaRegistry()
    # Ensure absolute path and use Path object
    abs_path = os.path.abspath(filename)
    schema_dir = Path(os.path.dirname(abs_path))
    context.registry.load_from_directory(schema_dir)


@then("the registry should contain the defined schema entities")
def step_impl_verify_registry(context):
    # Verify User and Post entities are present
    assert context.registry.get_schema("User") is not None
    assert context.registry.get_schema("Post") is not None
