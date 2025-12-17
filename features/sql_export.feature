Feature: SQL Export Transformation
  As a system user
  I want to verify that valid YAML schema definitions are correctly loaded into the registry and exported as SQL
  So that I can ensure data integrity during transformation

  Scenario: Load valid YAML and export SQL
    Given a valid YAML schema definition file "features/data/valid_schema.yaml"
    Then the registry should contain the defined schema entities
    When I request an SQL export
    Then the system should generate valid SQL DDL statements
