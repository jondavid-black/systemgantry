from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class DataType(str, Enum):
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    TIMESTAMP = "timestamp"
    JSON = "json"
    ENUM = "enum"
    REFERENCE = "reference"


class DataCategory(str, Enum):
    CONTROLLED = "controlled"
    DYNAMIC = "dynamic"


class DataSensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    PII = "pii"
    RESTRICTED = "restricted"


class RetentionPolicy(str, Enum):
    INDEFINITE = "indefinite"
    THIRTY_DAYS = "30_days"
    FISCAL_YEAR = "fiscal_year"


class TableUIHints(BaseModel):
    display_name: Optional[str] = Field(
        default=None, description="Human-readable name for the table"
    )
    icon: Optional[str] = Field(
        default=None, description="Icon identifier (e.g. mdi-account)"
    )
    default_sort_column: Optional[str] = Field(
        default=None, description="Column to sort by default"
    )
    summary_columns: List[str] = Field(
        default_factory=list, description="Columns to show in summary views"
    )


class EnumSchema(BaseModel):
    name: str = Field(description="The name of the enum")
    values: List[str] = Field(description="The allowed values for the enum")
    description: Optional[str] = Field(
        default=None, description="Description of the enum"
    )


class ColumnSchema(BaseModel):
    name: str = Field(description="The name of the column")
    data_type: DataType = Field(description="The data type of the column")
    primary_key: bool = Field(
        default=False, description="Whether this column is a primary key"
    )
    nullable: bool = Field(default=True, description="Whether this column can be null")
    unique: bool = Field(
        default=False, description="Whether this column must be unique"
    )
    default: Optional[str] = Field(
        default=None, description="Default value for the column (as a string)"
    )
    enum_values: Optional[List[str]] = Field(
        default=None, description="List of allowed values for ENUM type"
    )
    enum_name: Optional[str] = Field(
        default=None, description="Name of the ENUM type (if applicable)"
    )
    reference_table: Optional[str] = Field(
        default=None, description="Name of the table referenced by this column"
    )
    reference_column: Optional[str] = Field(
        default="id", description="Name of the column referenced in the target table"
    )


class TableSchema(BaseModel):
    name: str = Field(description="The name of the table")
    columns: List[ColumnSchema] = Field(description="List of columns in the table")
    description: Optional[str] = Field(
        default=None, description="Description of the table"
    )
    category: DataCategory = Field(
        default=DataCategory.CONTROLLED,
        description="Category of data (controlled or dynamic)",
    )
    namespace: Optional[str] = Field(
        default=None, description="Namespace for organizing related content"
    )
    owner: Optional[str] = Field(
        default=None, description="Owner or steward team responsible for this data"
    )
    sensitivity: DataSensitivity = Field(
        default=DataSensitivity.INTERNAL,
        description="Sensitivity classification of the data",
    )
    retention: RetentionPolicy = Field(
        default=RetentionPolicy.INDEFINITE, description="Data retention policy"
    )
    ui_hints: Optional[TableUIHints] = Field(
        default=None, description="UI rendering hints for the table"
    )
    composite_unique_constraints: List[List[str]] = Field(
        default_factory=list,
        description="List of column groups that must be unique together",
    )
