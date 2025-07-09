# resources/product.py

from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING
import json

from .base import AkeneoResource
from ..models.product import ProductRead, ProductWrite, ProductCreateWrite
from ..utils import validate_identifier

if TYPE_CHECKING:
    from ..client import AkeneoClient, AkeneoAsyncClient


class Product(AkeneoResource):
    """
    Product resource for Akeneo API.
    
    Handles both UUID-based and identifier-based product operations.
    For Myer's system, products are SKU-level items (Level 2).
    """
    
    endpoint = "products"
    model_class = ProductRead
    
    # Synchronous methods
    
    def get_by_uuid(self, uuid: str) -> "Product":
        """Get a product by its UUID."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        uuid = validate_identifier(uuid, "UUID")
        url = f"/api/rest/v1/products-uuid/{uuid}"
        response = self._client._make_request_sync("GET", url)
        
        return self._create_instance(response)
    
    def get_by_identifier(self, identifier: str) -> "Product":
        """Get a product by its identifier (SKU).""" 
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        identifier = validate_identifier(identifier, "identifier")
        url = f"/api/rest/v1/products/{identifier}"
        response = self._client._make_request_sync("GET", url)
        
        return self._create_instance(response)
    
    def list_by_uuid(self, paginated: bool = False, **params) -> Union[List["Product"], "PaginatedResponse[Product]"]:
        """List products using the UUID endpoint."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        url = "/api/rest/v1/products-uuid"
        prepared_params = self._prepare_request_params(params)
        response = self._client._make_request_sync("GET", url, params=prepared_params)
        
        items = self._extract_items(response)
        instances = [self._create_instance(item) for item in items]
        
        if paginated:
            pagination_data = self._extract_pagination_data(response)
            links = response.get('_links', {}) if isinstance(response, dict) else {}
            from .base import PaginatedResponse
            return PaginatedResponse(
                items=instances,
                current_page=pagination_data.get('current_page', 1),
                has_next=pagination_data.get('has_next', False),
                has_previous=pagination_data.get('has_previous', False),
                has_first=pagination_data.get('has_first', False),
                has_last=pagination_data.get('has_last', False),
                links=links
            )
        
        return instances
    
    def create_with_uuid(self, data: Union[Dict[str, Any], ProductCreateWrite]) -> "Product":
        """Create a new product using the UUID endpoint."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        url = "/api/rest/v1/products-uuid"
        prepared_data = self._prepare_request_data(data)
        response = self._client._make_request_sync("POST", url, json_data=prepared_data)
        
        return self._create_instance(response)
    
    def update_by_uuid(self, uuid: str, data: Union[Dict[str, Any], ProductWrite]) -> "Product":
        """Update a product by UUID."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        uuid = validate_identifier(uuid, "UUID")
        url = f"/api/rest/v1/products-uuid/{uuid}"
        prepared_data = self._prepare_request_data(data)
        response = self._client._make_request_sync("PATCH", url, json_data=prepared_data)
        
        # Akeneo PATCH often returns empty response, so fetch the updated product
        if response:
            return self._create_instance(response)
        else:
            return self.get_by_uuid(uuid)
    
    def update_by_identifier(self, identifier: str, data: Union[Dict[str, Any], ProductWrite]) -> "Product":
        """Update a product by identifier."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        identifier = validate_identifier(identifier, "identifier")
        url = f"/api/rest/v1/products/{identifier}"
        prepared_data = self._prepare_request_data(data)
        response = self._client._make_request_sync("PATCH", url, json_data=prepared_data)
        
        # Akeneo PATCH often returns empty response, so fetch the updated product
        if response:
            return self._create_instance(response)
        else:
            return self.get_by_identifier(identifier)
    
    def delete_by_uuid(self, uuid: str) -> None:
        """Delete a product by UUID."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        uuid = validate_identifier(uuid, "UUID")
        url = f"/api/rest/v1/products-uuid/{uuid}"
        self._client._make_request_sync("DELETE", url)
    
    def delete_by_identifier(self, identifier: str) -> None:
        """Delete a product by identifier."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        identifier = validate_identifier(identifier, "identifier")
        url = f"/api/rest/v1/products/{identifier}"
        self._client._make_request_sync("DELETE", url)
    
    def bulk_update(self, products: List[Union[Dict[str, Any], ProductWrite]], use_uuid: bool = False) -> List[Dict[str, Any]]:
        """
        Update multiple products at once.
        
        Args:
            products: List of product data to update
            use_uuid: Whether to use the UUID endpoint (default: identifier endpoint)
            
        Returns:
            List of status responses for each product update
        """
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        # Prepare the NDJSON payload
        lines = []
        for product_data in products:
            if hasattr(product_data, 'model_dump'):
                prepared_data = product_data.model_dump(by_alias=True, exclude_none=True)
            else:
                prepared_data = product_data
            lines.append(json.dumps(prepared_data))
        
        ndjson_payload = '\n'.join(lines)
        
        # Choose endpoint based on use_uuid flag
        url = "/api/rest/v1/products-uuid" if use_uuid else "/api/rest/v1/products"
        
        headers = {
            "Content-Type": "application/vnd.akeneo.collection+json"
        }
        
        response = self._client._make_request_sync("PATCH", url, form_data=ndjson_payload)
        
        # Parse NDJSON response
        if isinstance(response, str):
            results = []
            for line in response.strip().split('\n'):
                if line.strip():
                    results.append(json.loads(line))
            return results
        
        return response if isinstance(response, list) else [response]
    
    def search(self, search_criteria: Dict[str, Any], **params) -> List["Product"]:
        """
        Search for products using the search endpoint.
        
        Args:
            search_criteria: Search criteria in Akeneo format
            **params: Additional query parameters
            
        Returns:
            List of matching products
        """
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        url = "/api/rest/v1/products-uuid/search"
        
        # Prepare request body
        request_body = {
            "search": json.dumps(search_criteria) if search_criteria else None,
            **params
        }
        
        # Clean None values
        request_body = {k: v for k, v in request_body.items() if v is not None}
        
        response = self._client._make_request_sync("POST", url, json_data=request_body)
        
        items = self._extract_items(response)
        return [self._create_instance(item) for item in items]
    
    # Asynchronous methods
    
    async def get_by_uuid_async(self, uuid: str) -> "Product":
        """Get a product by its UUID asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        uuid = validate_identifier(uuid, "UUID")
        url = f"/api/rest/v1/products-uuid/{uuid}"
        response = await self._client._make_request_async("GET", url)
        
        return self._create_instance(response)
    
    async def get_by_identifier_async(self, identifier: str) -> "Product":
        """Get a product by its identifier (SKU) asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        identifier = validate_identifier(identifier, "identifier")
        url = f"/api/rest/v1/products/{identifier}"
        response = await self._client._make_request_async("GET", url)
        
        return self._create_instance(response)
    
    async def list_by_uuid_async(self, paginated: bool = False, **params) -> Union[List["Product"], "PaginatedResponse[Product]"]:
        """List products using the UUID endpoint asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        url = "/api/rest/v1/products-uuid"
        prepared_params = self._prepare_request_params(params)
        response = await self._client._make_request_async("GET", url, params=prepared_params)
        
        items = self._extract_items(response)
        instances = [self._create_instance(item) for item in items]
        
        if paginated:
            pagination_data = self._extract_pagination_data(response)
            links = response.get('_links', {}) if isinstance(response, dict) else {}
            from .base import PaginatedResponse
            return PaginatedResponse(
                items=instances,
                current_page=pagination_data.get('current_page', 1),
                has_next=pagination_data.get('has_next', False),
                has_previous=pagination_data.get('has_previous', False),
                has_first=pagination_data.get('has_first', False),
                has_last=pagination_data.get('has_last', False),
                links=links
            )
        
        return instances
    
    async def create_with_uuid_async(self, data: Union[Dict[str, Any], ProductCreateWrite]) -> "Product":
        """Create a new product using the UUID endpoint asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        url = "/api/rest/v1/products-uuid"
        prepared_data = self._prepare_request_data(data)
        response = await self._client._make_request_async("POST", url, json_data=prepared_data)
        
        return self._create_instance(response)
    
    async def update_by_uuid_async(self, uuid: str, data: Union[Dict[str, Any], ProductWrite]) -> "Product":
        """Update a product by UUID asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        uuid = validate_identifier(uuid, "UUID")
        url = f"/api/rest/v1/products-uuid/{uuid}"
        prepared_data = self._prepare_request_data(data)
        response = await self._client._make_request_async("PATCH", url, json_data=prepared_data)
        
        # Akeneo PATCH often returns empty response, so fetch the updated product
        if response:
            return self._create_instance(response)
        else:
            return await self.get_by_uuid_async(uuid)
    
    async def update_by_identifier_async(self, identifier: str, data: Union[Dict[str, Any], ProductWrite]) -> "Product":
        """Update a product by identifier asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        identifier = validate_identifier(identifier, "identifier")
        url = f"/api/rest/v1/products/{identifier}"
        prepared_data = self._prepare_request_data(data)
        response = await self._client._make_request_async("PATCH", url, json_data=prepared_data)
        
        # Akeneo PATCH often returns empty response, so fetch the updated product
        if response:
            return self._create_instance(response)
        else:
            return await self.get_by_identifier_async(identifier)
    
    async def delete_by_uuid_async(self, uuid: str) -> None:
        """Delete a product by UUID asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        uuid = validate_identifier(uuid, "UUID")
        url = f"/api/rest/v1/products-uuid/{uuid}"
        await self._client._make_request_async("DELETE", url)
    
    async def delete_by_identifier_async(self, identifier: str) -> None:
        """Delete a product by identifier asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        identifier = validate_identifier(identifier, "identifier")
        url = f"/api/rest/v1/products/{identifier}"
        await self._client._make_request_async("DELETE", url)
    
    async def bulk_update_async(self, products: List[Union[Dict[str, Any], ProductWrite]], use_uuid: bool = False) -> List[Dict[str, Any]]:
        """
        Update multiple products at once asynchronously.
        
        Args:
            products: List of product data to update
            use_uuid: Whether to use the UUID endpoint (default: identifier endpoint)
            
        Returns:
            List of status responses for each product update
        """
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        # Prepare the NDJSON payload
        lines = []
        for product_data in products:
            if hasattr(product_data, 'model_dump'):
                prepared_data = product_data.model_dump(by_alias=True, exclude_none=True)
            else:
                prepared_data = product_data
            lines.append(json.dumps(prepared_data))
        
        ndjson_payload = '\n'.join(lines)
        
        # Choose endpoint based on use_uuid flag
        url = "/api/rest/v1/products-uuid" if use_uuid else "/api/rest/v1/products"
        
        response = await self._client._make_request_async("PATCH", url, form_data=ndjson_payload)
        
        # Parse NDJSON response
        if isinstance(response, str):
            results = []
            for line in response.strip().split('\n'):
                if line.strip():
                    results.append(json.loads(line))
            return results
        
        return response if isinstance(response, list) else [response]
    
    async def search_async(self, search_criteria: Dict[str, Any], **params) -> List["Product"]:
        """
        Search for products using the search endpoint asynchronously.
        
        Args:
            search_criteria: Search criteria in Akeneo format
            **params: Additional query parameters
            
        Returns:
            List of matching products
        """
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        url = "/api/rest/v1/products-uuid/search"
        
        # Prepare request body
        request_body = {
            "search": json.dumps(search_criteria) if search_criteria else None,
            **params
        }
        
        # Clean None values
        request_body = {k: v for k, v in request_body.items() if v is not None}
        
        response = await self._client._make_request_async("POST", url, json_data=request_body)
        
        items = self._extract_items(response)
        return [self._create_instance(item) for item in items]
