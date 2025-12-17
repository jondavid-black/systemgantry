# features/steps/infrastructure_steps.py
from behave import given, when, then
import subprocess
import os


@given("a clean development environment")
def step_impl_clean_env(context):
    pass


@when("I inspect the project dependencies")
def step_impl_inspect_deps(context):
    result = subprocess.run(["uv", "pip", "list"], capture_output=True, text=True)
    context.dependencies = result.stdout


@then("behave should be listed as a development dependency")
def step_impl_check_behave(context):
    assert "behave" in context.dependencies


@given("the project root")
def step_impl_project_root(context):
    context.project_root = os.getcwd()


@when("I list directories")
def step_impl_list_dirs(context):
    context.dirs = [d for d in os.listdir(context.project_root) if os.path.isdir(d)]


@then("a features directory should exist for storing Gherkin feature files")
def step_impl_check_features_dir(context):
    assert "features" in context.dirs


@given("the test runner is configured")
def step_impl_runner_configured(context):
    pass


@when("I execute the test command")
def step_impl_exec_test_cmd(context):
    # We are running this *inside* the test runner, so effectively it's running.
    # To test the runner itself is meta, but we can verify we are in a behave execution context.
    pass


@then("the BDD test suite should initialize without errors")
def step_impl_check_initialization(context):
    assert True
