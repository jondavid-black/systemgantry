# Data Model - Add BDD Testing

**Feature**: Add BDD Testing
**Status**: Draft

## Overview

Since this feature is about adding a testing layer, it does not introduce new persistent data models for the application itself. However, it relies on the *existing* data models defined in the `src/data` module.

## Referenced Entities (Existing)

### 1. Schema Definition
The core entity being tested.
- **Source**: YAML files in `features/data/` (test inputs)
- **Internal Representation**: `SchemaDefinition` (Pydantic model in `src/data/schema.py` presumably, or raw dicts processed by Registry)

### 2. Registry
The system under test component.
- **Class**: `src.data.registry.SchemaRegistry`
- **Role**: State container for loaded schemas.

### 3. Generator
The transformation engine.
- **Class**: `src.data.generator.SchemaGenerator` (SQL)
- **Class**: `src.data.generator.ProtobufGenerator` (ProtoBuf)
- **Role**: Converts Registry contents to output formats.

## Test Data Model

The BDD tests will introduce *test data* structures, specifically Gherkin feature files and their backing step implementations.

### Feature File Structure
```gherkin
Feature: [Name]
  Scenario: [Name]
    Given [Context]
    When [Action]
    Then [Outcome]
```
