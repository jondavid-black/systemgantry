Feature: ProtoBuf Export Transformation
  As a system user
  I want to verify that valid YAML schema definitions are correctly loaded into the registry and exported as Protocol Buffers
  So that I can ensure compatibility with gRPC services

  Scenario: Load valid YAML and export ProtoBuf
    Given a valid YAML schema definition file "features/data/valid_schema.yaml"
    Then the registry should contain the defined schema entities
    When I request a ProtoBuf export
    Then the system should generate valid Protocol Buffer definitions
