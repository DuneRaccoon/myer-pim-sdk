# resources/category.py

from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING
import json

from .base import AkeneoResource
from ..models.category import CategoryRead, CategoryWrite, CategoryCreateWrite
from ..utils import validate_identifier

if TYPE_CHECKING:
    from ..client import AkeneoClient, AkeneoAsyncClient


class Category(AkeneoResource):
    """Category resource for Akeneo API."""
    
    endpoint = "categories"
    model_class = CategoryRead
    
    def get_by_code(self, code: str) -> "Category":
        """Get a category by its code."""
        code = validate_identifier(code, "code")
        return self.get(code)
    
    def create_category(self, data: Union[Dict[str, Any], CategoryCreateWrite]) -> "Category":
        """Create a new category."""
        return self.create(data)
    
    def update_by_code(self, code: str, data: Union[Dict[str, Any], CategoryWrite]) -> "Category":
        """Update a category by code."""
        code = validate_identifier(code, "code")
        return self.update(code, data)
    
    def delete_by_code(self, code: str) -> None:
        """Delete a category by code."""
        code = validate_identifier(code, "code")
        self.delete(code)
    
    def bulk_update(self, categories: List[Union[Dict[str, Any], CategoryWrite]]) -> List[Dict[str, Any]]:
        """Update multiple categories at once."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        # Prepare the NDJSON payload
        lines = []
        for category_data in categories:
            if hasattr(category_data, 'model_dump'):
                prepared_data = category_data.model_dump(by_alias=True, exclude_none=True)
            else:
                prepared_data = category_data
            lines.append(json.dumps(prepared_data))
        
        ndjson_payload = '\n'.join(lines)
        url = "/api/rest/v1/categories"
        
        response = self._client._make_request_sync("PATCH", url, form_data=ndjson_payload)
        
        # Parse NDJSON response
        if isinstance(response, str):
            results = []
            for line in response.strip().split('\n'):
                if line.strip():
                    results.append(json.loads(line))
            return results
        
        return response if isinstance(response, list) else [response]
    
    def create_media_file(self, category_code: str, attribute_code: str, file_path: str, 
                         scope: Optional[str] = None, locale: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a media file for a category attribute.
        
        Args:
            category_code: Code of the category
            attribute_code: Code of the attribute
            file_path: Path to the file to upload
            scope: Channel scope (optional)
            locale: Locale (optional)
        """
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        category_code = validate_identifier(category_code, "category_code")
        
        url = "/api/rest/v1/category-media-files"
        
        # Prepare the category JSON
        category_json = {
            "code": category_code,
            "attribute_code": attribute_code,
            "channel": scope,
            "locale": locale
        }
        
        # Prepare the multipart form data
        with open(file_path, 'rb') as f:
            files = {
                'file': f,
            }
            form_data = {
                'category': json.dumps(category_json)
            }
            
            response = self._client._make_request_sync("POST", url, form_data=form_data, files=files)
        
        return response
    
    def download_media_file(self, file_path: str) -> bytes:
        """Download a category media file."""
        if not hasattr(self._client, '_make_request_sync'):
            raise TypeError("This method requires a synchronous client")
        
        url = f"/api/rest/v1/category-media-files/{file_path}/download"
        response = self._client._make_request_sync("GET", url)
        
        # For binary content, we need to access the raw response
        # This might need to be adjusted based on how the client handles binary responses
        return response
    
    # Asynchronous versions
    async def get_by_code_async(self, code: str) -> "Category":
        """Get a category by its code asynchronously."""
        code = validate_identifier(code, "code")
        return await self.get_async(code)
    
    async def create_category_async(self, data: Union[Dict[str, Any], CategoryCreateWrite]) -> "Category":
        """Create a new category asynchronously."""
        return await self.create_async(data)
    
    async def update_by_code_async(self, code: str, data: Union[Dict[str, Any], CategoryWrite]) -> "Category":
        """Update a category by code asynchronously."""
        code = validate_identifier(code, "code")
        return await self.update_async(code, data)
    
    async def delete_by_code_async(self, code: str) -> None:
        """Delete a category by code asynchronously."""
        code = validate_identifier(code, "code")
        await self.delete_async(code)
    
    async def bulk_update_async(self, categories: List[Union[Dict[str, Any], CategoryWrite]]) -> List[Dict[str, Any]]:
        """Update multiple categories at once asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        # Prepare the NDJSON payload
        lines = []
        for category_data in categories:
            if hasattr(category_data, 'model_dump'):
                prepared_data = category_data.model_dump(by_alias=True, exclude_none=True)
            else:
                prepared_data = category_data
            lines.append(json.dumps(prepared_data))
        
        ndjson_payload = '\n'.join(lines)
        url = "/api/rest/v1/categories"
        
        response = await self._client._make_request_async("PATCH", url, form_data=ndjson_payload)
        
        # Parse NDJSON response
        if isinstance(response, str):
            results = []
            for line in response.strip().split('\n'):
                if line.strip():
                    results.append(json.loads(line))
            return results
        
        return response if isinstance(response, list) else [response]
    
    async def create_media_file_async(self, category_code: str, attribute_code: str, file_path: str, 
                                    scope: Optional[str] = None, locale: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a media file for a category attribute asynchronously.
        
        Args:
            category_code: Code of the category
            attribute_code: Code of the attribute
            file_path: Path to the file to upload
            scope: Channel scope (optional)
            locale: Locale (optional)
        """
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        category_code = validate_identifier(category_code, "category_code")
        
        url = "/api/rest/v1/category-media-files"
        
        # Prepare the category JSON
        category_json = {
            "code": category_code,
            "attribute_code": attribute_code,
            "channel": scope,
            "locale": locale
        }
        
        # Prepare the multipart form data
        with open(file_path, 'rb') as f:
            files = {
                'file': f,
            }
            form_data = {
                'category': json.dumps(category_json)
            }
            
            response = await self._client._make_request_async("POST", url, form_data=form_data, files=files)
        
        return response
    
    async def download_media_file_async(self, file_path: str) -> bytes:
        """Download a category media file asynchronously."""
        if not hasattr(self._client, '_make_request_async'):
            raise TypeError("This method requires an asynchronous client")
        
        url = f"/api/rest/v1/category-media-files/{file_path}/download"
        response = await self._client._make_request_async("GET", url)
        
        # For binary content, we need to access the raw response
        return response
