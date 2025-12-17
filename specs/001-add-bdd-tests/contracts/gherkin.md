# Contracts

This feature adds internal testing infrastructure and does not expose new public API endpoints (REST/GraphQL). 
The "contract" here is the Gherkin syntax used to define acceptance tests.

## Gherkin Step Definitions

### Registry Loading
- `Given a valid YAML schema definition file "{filename}"`
- `Given the schema is loaded in the registry`
- `Then the registry should contain the defined schema entities`

### SQL Export
- `When I request an SQL export`
- `Then the system should generate valid SQL DDL statements`

### ProtoBuf Export
- `When I request a ProtoBuf export`
- `Then the system should generate valid Protocol Buffer definitions`
