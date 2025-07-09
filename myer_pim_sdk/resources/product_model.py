# resources/product_model.py

from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING
import json

from .base import AkeneoResource
from ..models.product_model import ProductModelRead, ProductModelWrite, ProductModelCreateWrite
from ..utils import validate_identifier

if TYPE_CHECKING:
    from ..client import AkeneoClient, AkeneoAsyncClient


class ProductModel(AkeneoResource):
    """
    Product Model resource for Akeneo API.
    
    For Myer's system, product models are the main entities (Level 1) 
    where copy and image enrichment is performed.
    """
    
    endpoint = "product-models"
    model_class = ProductModelRead
    
    # Synchronous methods
    
    def get_by_code(self, code: str) -> "ProductModel":
        """Get a product model by its code."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        code = validate_identifier(code, "code")
        url = f"/api/rest/v1/product-models/{code}"
        response = self._client._make_request_sync("GET", url)
        
        return self._create_instance(response)
    
    def create_product_model(self, data: Union[Dict[str, Any], ProductModelCreateWrite]) -> "ProductModel":
        """Create a new product model."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        url = "/api/rest/v1/product-models"
        prepared_data = self._prepare_request_data(data)
        response = self._client._make_request_sync("POST", url, json_data=prepared_data)
        
        return self._create_instance(response)
    
    def update_by_code(self, code: str, data: Union[Dict[str, Any], ProductModelWrite]) -> "ProductModel":
        """Update a product model by code."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        code = validate_identifier(code, "code")
        url = f"/api/rest/v1/product-models/{code}"
        prepared_data = self._prepare_request_data(data)
        response = self._client._make_request_sync("PATCH", url, json_data=prepared_data)
        
        # Akeneo PATCH often returns empty response, so fetch the updated product model
        if response:
            return self._create_instance(response)
        else:
            return self.get_by_code(code)
    
    def delete_by_code(self, code: str) -> None:
        """Delete a product model by code."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
            
        code = validate_identifier(code, "code")
        url = f"/api/rest/v1/product-models/{code}"
        self._client._make_request_sync("DELETE", url)
    
    def bulk_update(self, product_models: List[Union[Dict[str, Any], ProductModelWrite]]) -> List[Dict[str, Any]]:
        """
        Update multiple product models at once.
        
        Args:
            product_models: List of product model data to update
            
        Returns:
            List of status responses for each product model update
        """
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        # Prepare the NDJSON payload
        lines = []
        for product_model_data in product_models:
            if hasattr(product_model_data, 'model_dump'):
                prepared_data = product_model_data.model_dump(by_alias=True, exclude_none=True)
            else:
                prepared_data = product_model_data
            lines.append(json.dumps(prepared_data))
        
        ndjson_payload = '\n'.join(lines)
        
        url = "/api/rest/v1/product-models"
        
        response = self._client._make_request_sync("PATCH", url, form_data=ndjson_payload)
        
        # Parse NDJSON response
        if isinstance(response, str):
            results = []
            for line in response.strip().split('\n'):
                if line.strip():
                    results.append(json.loads(line))
            return results
        
        return response if isinstance(response, list) else [response]
    
    def update_enrichment_status(self, code: str, status_type: str, status_value: int) -> None:
        """
        Update the enrichment status for a product model.
        
        This is specific to Myer's implementation where enrichment status
        is tracked (e.g., image status 10, copy status 10, etc.)
        
        Args:
            code: Product model code
            status_type: Type of status (e.g., 'image', 'copy')
            status_value: Status value (e.g., 10, 20, 30)
        """
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        code = validate_identifier(code, "code")
        
        # This would typically update a specific attribute value
        # The exact implementation depends on how Myer structures their enrichment status
        status_data = {
            "values": {
                f"{status_type}_status": [
                    {
                        "data": status_value,
                        "locale": None,
                        "scope": None
                    }
                ]
            }
        }
        
        self.update_by_code(code, status_data)
    
    # Asynchronous methods
    
    async def get_by_code_async(self, code: str) -> "ProductModel":
        """Get a product model by its code asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        code = validate_identifier(code, "code")
        url = f"/api/rest/v1/product-models/{code}"
        response = await self._client._make_request_async("GET", url)
        
        return self._create_instance(response)
    
    async def create_product_model_async(self, data: Union[Dict[str, Any], ProductModelCreateWrite]) -> "ProductModel":
        """Create a new product model asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        url = "/api/rest/v1/product-models"
        prepared_data = self._prepare_request_data(data)
        response = await self._client._make_request_async("POST", url, json_data=prepared_data)
        
        return self._create_instance(response)
    
    async def update_by_code_async(self, code: str, data: Union[Dict[str, Any], ProductModelWrite]) -> "ProductModel":
        """Update a product model by code asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        code = validate_identifier(code, "code")
        url = f"/api/rest/v1/product-models/{code}"
        prepared_data = self._prepare_request_data(data)
        response = await self._client._make_request_async("PATCH", url, json_data=prepared_data)
        
        # Akeneo PATCH often returns empty response, so fetch the updated product model
        if response:
            return self._create_instance(response)
        else:
            return await self.get_by_code_async(code)
    
    async def delete_by_code_async(self, code: str) -> None:
        """Delete a product model by code asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
            
        code = validate_identifier(code, "code")
        url = f"/api/rest/v1/product-models/{code}"
        await self._client._make_request_async("DELETE", url)
    
    async def bulk_update_async(self, product_models: List[Union[Dict[str, Any], ProductModelWrite]]) -> List[Dict[str, Any]]:
        """
        Update multiple product models at once asynchronously.
        
        Args:
            product_models: List of product model data to update
            
        Returns:
            List of status responses for each product model update
        """
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        # Prepare the NDJSON payload
        lines = []
        for product_model_data in product_models:
            if hasattr(product_model_data, 'model_dump'):
                prepared_data = product_model_data.model_dump(by_alias=True, exclude_none=True)
            else:
                prepared_data = product_model_data
            lines.append(json.dumps(prepared_data))
        
        ndjson_payload = '\n'.join(lines)
        
        url = "/api/rest/v1/product-models"
        
        response = await self._client._make_request_async("PATCH", url, form_data=ndjson_payload)
        
        # Parse NDJSON response
        if isinstance(response, str):
            results = []
            for line in response.strip().split('\n'):
                if line.strip():
                    results.append(json.loads(line))
            return results
        
        return response if isinstance(response, list) else [response]
    
    async def update_enrichment_status_async(self, code: str, status_type: str, status_value: int) -> None:
        """
        Update the enrichment status for a product model asynchronously.
        
        This is specific to Myer's implementation where enrichment status
        is tracked (e.g., image status 10, copy status 10, etc.)
        
        Args:
            code: Product model code
            status_type: Type of status (e.g., 'image', 'copy')
            status_value: Status value (e.g., 10, 20, 30)
        """
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        code = validate_identifier(code, "code")
        
        # This would typically update a specific attribute value
        # The exact implementation depends on how Myer structures their enrichment status
        status_data = {
            "values": {
                f"{status_type}_status": [
                    {
                        "data": status_value,
                        "locale": None,
                        "scope": None
                    }
                ]
            }
        }
        
        await self.update_by_code_async(code, status_data)
