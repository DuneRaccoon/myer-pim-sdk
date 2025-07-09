# Myer PIM SDK

[![PyPI version](https://badge.fury.io/py/myer-pim-sdk.svg)](https://badge.fury.io/py/myer-pim-sdk)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python SDK for integrating with Akeneo REST API, specifically designed for Myer's Product Information Management (PIM) system.

## Features

- **Full Akeneo REST API Coverage**: Support for products, product models, families, attributes, categories, and media files
- **Rate Limiting**: Built-in throttling to respect Myer's 20 calls per minute limit
- **Synchronous & Asynchronous**: Both sync and async client implementations
- **Type Safety**: Full Pydantic model support with type hints
- **Bulk Operations**: Efficient bulk updates for multiple entities
- **Media File Handling**: Streamlined image and file upload for product enrichment
- **Error Handling**: Comprehensive error handling with specific exception types
- **Retry Logic**: Automatic retry on transient failures
- **OAuth2 Authentication**: Automatic token management and refresh

## Installation

```bash
pip install myer-pim-sdk
```

For development with Redis support:
```bash
pip install myer-pim-sdk[redis,dev]
```

## Quick Start

### Basic Setup

```python
from myer_pim_sdk import AkeneoClient

# Initialize the client
client = AkeneoClient(
    client_id="your_client_id",
    client_secret="your_client_secret", 
    base_url="https://your-pim.akeneo.com"
)

# Get a product by identifier (SKU)
product = client.products.get_by_identifier("SKU123")
print(f"Product: {product.identifier} - {product.values}")
```

### Async Usage

```python
from myer_pim_sdk import AkeneoAsyncClient
import asyncio

async def main():
    client = AkeneoAsyncClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        base_url="https://your-pim.akeneo.com"
    )
    
    try:
        # Get product asynchronously
        product = await client.products.get_by_identifier_async("SKU123")
        print(f"Product: {product.identifier}")
        
        # List products with pagination
        products = await client.products.list_by_uuid_async(limit=50, paginated=True)
        print(f"Found {len(products.items)} products")
        
    finally:
        await client.close()

asyncio.run(main())
```

## Key Concepts for Myer's System

### Product Hierarchy

In Myer's Akeneo implementation:

- **Product Models** (Level 1): Main entities where copy and image enrichment occurs
- **Products** (Level 2): SKU-level items that inherit from product models

### Enrichment Status

The SDK supports Myer's enrichment status workflow:

```python
# Update enrichment status for a product model
client.product_models.update_enrichment_status(
    code="product_model_code",
    status_type="image", 
    status_value=10  # Ready for enrichment
)

# After enrichment is complete
client.product_models.update_enrichment_status(
    code="product_model_code",
    status_type="image",
    status_value=20  # Enrichment complete
)
```

### Image Upload (Core Myer Workflow)

```python
# Upload image for a product model (recommended approach)
media_file = client.media_files.upload_for_product_model(
    product_model_code="700000540",
    attribute_code="new_image1", 
    file_path="/path/to/image.jpg"
)

# Update image status after upload
client.product_models.update_enrichment_status(
    code="700000540",
    status_type="image",
    status_value=20
)
```

## Core Resources

### Products

```python
# Get product by UUID or identifier
product = client.products.get_by_uuid("uuid-here")
product = client.products.get_by_identifier("SKU123")

# Create a new product
new_product = client.products.create_with_uuid({
    "identifier": "NEW_SKU",
    "family": "clothing",
    "values": {
        "name": [{"data": "New Product", "locale": "en_US", "scope": None}]
    }
})

# Bulk update products
results = client.products.bulk_update([
    {"identifier": "SKU1", "values": {...}},
    {"identifier": "SKU2", "values": {...}}
])

# Search products
products = client.products.search({
    "family": [{"operator": "IN", "value": ["shoes", "bags"]}]
})
```

### Product Models

```python
# Get product model by code
product_model = client.product_models.get_by_code("model_code")

# Create product model
new_model = client.product_models.create_product_model({
    "code": "new_model",
    "family_variant": "clothing_material_size",
    "values": {
        "description": [{"data": "Model description", "locale": "en_US", "scope": "ecommerce"}]
    }
})

# Update product model
updated_model = client.product_models.update_by_code("model_code", {
    "values": {
        "name": [{"data": "Updated Name", "locale": "en_US", "scope": None}]
    }
})
```

### Media Files

```python
# Upload image for product model (Myer's main use case)
media_file = client.media_files.upload_for_product_model(
    product_model_code="700000540",
    attribute_code="new_image1",
    file_path="/path/to/image.jpg"
)

# Upload image for specific product
media_file = client.media_files.upload_for_product(
    product_identifier="SKU123",
    attribute_code="image", 
    file_path="/path/to/image.jpg",
    scope="ecommerce"
)

# Download media file
binary_data = client.media_files.download("media_file_code")

# Get media file info
file_info = client.media_files.get_file_info("media_file_code")
```

### Families and Attributes

```python
# Get family details
family = client.families.get_by_code("clothing")

# List attributes
attributes = client.attributes.list(limit=100)

# Create new attribute
new_attribute = client.attributes.create_attribute({
    "code": "new_attribute",
    "type": "pim_catalog_text",
    "group": "marketing",
    "labels": {"en_US": "New Attribute"}
})

# Get family variants
variants = client.family_variants.list_for_family("clothing")
```

### Categories

```python
# Get category
category = client.categories.get_by_code("men_shoes")

# Create category
new_category = client.categories.create_category({
    "code": "new_category",
    "parent": "master",
    "labels": {"en_US": "New Category"}
})

# Upload category media
client.categories.create_media_file(
    category_code="men_shoes",
    attribute_code="category_image",
    file_path="/path/to/category_image.jpg"
)
```

## Advanced Features

### Pagination

```python
# Manual pagination
page1 = client.products.list_by_uuid(page=1, limit=100, paginated=True)
if page1.has_next:
    page2 = client.products.list_by_uuid(page=2, limit=100, paginated=True)

# Auto-pagination generator
for product in client.products.paginate(limit=100):
    print(f"Processing product: {product.identifier}")
```

### Bulk Operations

```python
# Bulk update products with status tracking
products_to_update = [
    {"identifier": "SKU1", "values": {"name": [...]}},
    {"identifier": "SKU2", "values": {"description": [...]}}
]

results = client.products.bulk_update(products_to_update)
for result in results:
    if result['status_code'] == 204:
        print(f"Successfully updated {result['identifier']}")
    else:
        print(f"Failed to update {result['identifier']}: {result['message']}")
```

### Error Handling

```python
from myer_pim_sdk import (
    AkeneoAPIError,
    AuthenticationError, 
    ValidationError,
    NotFoundError,
    RateLimitError
)

try:
    product = client.products.get_by_identifier("INVALID_SKU")
except NotFoundError:
    print("Product not found")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except AkeneoAPIError as e:
    print(f"API error: {e.message}")
```

### System Information

```python
# Check API health
is_healthy = client.system.check_health()

# Get system info
info = client.system.get_system_information()
print(f"PIM Version: {info['version']}, Edition: {info['edition']}")

# List all available endpoints
endpoints = client.system.get_endpoints()
```

## Configuration

### Rate Limiting

The SDK automatically handles Myer's rate limit of 20 calls per minute:

```python
from myer_pim_sdk import AkeneoClient

# Rate limiting is automatically configured for Myer's limits
client = AkeneoClient(
    client_id="client_id",
    client_secret="client_secret",
    base_url="https://your-pim.akeneo.com",
    # Rate limiting is handled automatically
)
```

### Custom Configuration

```python
client = AkeneoClient(
    client_id="client_id",
    client_secret="client_secret", 
    base_url="https://your-pim.akeneo.com",
    timeout=120.0,  # Request timeout in seconds
    max_retries=3,  # Number of retries on failure
    token_buffer_seconds=300  # Refresh token 5 minutes before expiry
)
```

## Myer-Specific Workflows

### Complete Product Enrichment Workflow

```python
# 1. Get products with enrichment status 10 (ready for enrichment)
products = client.product_models.list(
    search='{"enrichment_status":[{"operator":"=","value":"10"}]}'
)

for product_model in products:
    try:
        # 2. Upload product images
        for i in range(1, 6):  # Upload up to 5 images
            try:
                image_path = f"/images/{product_model.code}_image_{i}.jpg"
                client.media_files.upload_for_product_model(
                    product_model_code=product_model.code,
                    attribute_code=f"new_image{i}",
                    file_path=image_path
                )
            except FileNotFoundError:
                break  # No more images for this product
        
        # 3. Update copy/attributes
        client.product_models.update_by_code(product_model.code, {
            "values": {
                "description": [{
                    "data": "Enhanced product description",
                    "locale": "en_US", 
                    "scope": "ecommerce"
                }],
                "short_description": [{
                    "data": "Short description",
                    "locale": "en_US",
                    "scope": "ecommerce"  
                }]
            }
        })
        
        # 4. Set enrichment status to 20 (complete)
        client.product_models.update_enrichment_status(
            code=product_model.code,
            status_type="image",
            status_value=20
        )
        
        print(f"Successfully enriched {product_model.code}")
        
    except Exception as e:
        print(f"Failed to enrich {product_model.code}: {e}")
```

### Batch Image Upload

```python
import os
from pathlib import Path

def upload_images_batch(client, image_directory: str, product_codes: list):
    """Upload images for multiple product models in batch."""
    
    results = []
    
    for product_code in product_codes:
        product_results = {"code": product_code, "uploaded_images": []}
        
        # Look for images matching the product code
        image_patterns = [
            f"{product_code}_*.jpg",
            f"{product_code}_*.png", 
            f"{product_code}_*.jpeg"
        ]
        
        image_files = []
        for pattern in image_patterns:
            image_files.extend(Path(image_directory).glob(pattern))
        
        # Upload each image found
        for i, image_path in enumerate(image_files[:5], 1):  # Max 5 images
            try:
                media_file = client.media_files.upload_for_product_model(
                    product_model_code=product_code,
                    attribute_code=f"new_image{i}",
                    file_path=str(image_path)
                )
                product_results["uploaded_images"].append({
                    "attribute": f"new_image{i}",
                    "file": image_path.name,
                    "media_code": media_file.code
                })
            except Exception as e:
                print(f"Failed to upload {image_path} for {product_code}: {e}")
        
        # Update enrichment status if any images were uploaded
        if product_results["uploaded_images"]:
            try:
                client.product_models.update_enrichment_status(
                    code=product_code,
                    status_type="image", 
                    status_value=20
                )
                product_results["status"] = "completed"
            except Exception as e:
                print(f"Failed to update status for {product_code}: {e}")
                product_results["status"] = "uploaded_but_status_failed"
        else:
            product_results["status"] = "no_images_found"
        
        results.append(product_results)
    
    return results

# Usage
image_results = upload_images_batch(
    client=client,
    image_directory="/path/to/images",
    product_codes=["700000540", "700000541", "700000542"]
)
```

## Testing

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=myer_pim_sdk

# Type checking
mypy myer_pim_sdk/

# Code formatting
black myer_pim_sdk/
isort myer_pim_sdk/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

- GitHub Issues: https://github.com/DuneRaccoon/myer-pim-sdk/issues
- Documentation: https://api.akeneo.com/api-reference.html

## Changelog

### 1.0.0 (2025-07-09)

- Initial release
- Full Akeneo REST API support
- Synchronous and asynchronous clients
- Rate limiting for Myer's API constraints
- Comprehensive media file handling
- Bulk operations support
- Type-safe models with Pydantic
- Automatic OAuth2 token management
