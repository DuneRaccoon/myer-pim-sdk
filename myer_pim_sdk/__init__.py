# Myer PIM SDK - Akeneo REST API Integration

from .client import AkeneoClient, AkeneoAsyncClient
from .exceptions import (
    AkeneoAPIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError
)
from .search import (
    SearchBuilder,
    FilterBuilder,
    ProductPropertyFilter,
    ProductModelPropertyFilter,
    AttributeFilter
)
from .search.operators import (
    ComparisonOperator,
    ListOperator,
    DateOperator,
    TextOperator,
    CategoryOperator,
    CompletenessOperator,
    BooleanOperator,
    ParentOperator,
    QualityScoreOperator,
    EmptyOperator
)

__version__ = "1.0.0"
__all__ = [
    "AkeneoClient",
    "AkeneoAsyncClient",
    "AkeneoAPIError",
    "AuthenticationError", 
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "SearchBuilder",
    "FilterBuilder",
    "ComparisonOperator",
    "ListOperator",
    "DateOperator",
    "TextOperator",
    "CategoryOperator",
    "CompletenessOperator",
    "BooleanOperator",
    "ParentOperator",
    "QualityScoreOperator",
    "EmptyOperator",
    "ProductPropertyFilter",
    "ProductModelPropertyFilter",
    "AttributeFilter"
]
