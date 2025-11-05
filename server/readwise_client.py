"""Readwise API Client with dual API support (v2 Highlights + v3 Reader)"""

import httpx
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ReadwiseClient:
    """Client for interacting with Readwise APIs (v2 and v3)"""

    def __init__(self, token: str):
        self.token = token
        self.v2_base_url = "https://readwise.io/api/v2"
        self.v3_base_url = "https://readwise.io/api/v3"
        self.headers = {"Authorization": f"Token {token}"}

    async def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        api_version: str = "v3"
    ) -> Dict[str, Any]:
        """Make HTTP request to Readwise API"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise Exception(f"Readwise API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                logger.error(f"Request error: {str(e)}")
                raise

    # ==================== Reader API (v3) ====================

    async def save_document(self, url: str, **kwargs) -> Dict[str, Any]:
        """Save a document to Reader"""
        data = {"url": url, **kwargs}
        return await self._request("POST", f"{self.v3_base_url}/save", json=data)

    async def list_documents(
        self,
        location: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List documents from Reader"""
        params = {"pageCursor": None}
        if location:
            params["location"] = location
        if category:
            params["category"] = category

        all_results = []

        while len(all_results) < limit:
            response = await self._request("GET", f"{self.v3_base_url}/list", params=params)
            results = response.get("results", [])

            if not results:
                break

            all_results.extend(results)

            next_cursor = response.get("nextPageCursor")
            if not next_cursor:
                break

            params["pageCursor"] = next_cursor

        return all_results[:limit]

    async def update_document(self, document_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a document in Reader"""
        return await self._request("PATCH", f"{self.v3_base_url}/documents/{document_id}", json=updates)

    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document from Reader"""
        return await self._request("DELETE", f"{self.v3_base_url}/documents/{document_id}")

    async def list_tags(self) -> List[str]:
        """Get all tags from Reader"""
        response = await self._request("GET", f"{self.v3_base_url}/tags")
        return response.get("tags", [])

    async def topic_search(
        self,
        query: str,
        location: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search documents by topic"""
        params = {
            "query": query,
            "limit": limit
        }
        if location:
            params["location"] = location
        if category:
            params["category"] = category

        response = await self._request("GET", f"{self.v3_base_url}/search", params=params)
        return response.get("results", [])

    # ==================== Highlights API (v2) ====================

    async def list_highlights(
        self,
        page_size: int = 100,
        page: int = 1,
        book_id: Optional[int] = None,
        **filters
    ) -> Dict[str, Any]:
        """List highlights with filtering"""
        params = {
            "page_size": page_size,
            "page": page
        }
        if book_id:
            params["book_id"] = book_id
        params.update(filters)

        return await self._request("GET", f"{self.v2_base_url}/highlights", params=params, api_version="v2")

    async def get_daily_review(self) -> Dict[str, Any]:
        """Get daily review highlights (spaced repetition)"""
        return await self._request("GET", f"{self.v2_base_url}/review", api_version="v2")

    async def search_highlights(
        self,
        query: str,
        page_size: int = 100,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """Search highlights by text query"""
        params = {
            "q": query,
            "page_size": page_size,
            "page": page
        }
        response = await self._request("GET", f"{self.v2_base_url}/highlights", params=params, api_version="v2")
        return response.get("results", [])

    async def list_books(
        self,
        page_size: int = 100,
        page: int = 1,
        category: Optional[str] = None,
        **filters
    ) -> Dict[str, Any]:
        """List books with metadata"""
        params = {
            "page_size": page_size,
            "page": page
        }
        if category:
            params["category"] = category
        params.update(filters)

        return await self._request("GET", f"{self.v2_base_url}/books", params=params, api_version="v2")

    async def get_book_highlights(self, book_id: int) -> List[Dict[str, Any]]:
        """Get all highlights from a specific book"""
        return await self.list_highlights(book_id=book_id)

    async def export_highlights(
        self,
        updated_after: Optional[str] = None,
        include_deleted: bool = False
    ) -> List[Dict[str, Any]]:
        """Export highlights for backup/analysis"""
        params = {}
        if updated_after:
            params["updatedAfter"] = updated_after
        if include_deleted:
            params["deleted"] = "true"

        all_highlights = []
        page = 1

        while True:
            params["page"] = page
            params["page_size"] = 1000
            response = await self._request("GET", f"{self.v2_base_url}/export", params=params, api_version="v2")

            results = response.get("results", [])
            if not results:
                break

            all_highlights.extend(results)

            if not response.get("next"):
                break

            page += 1

        return all_highlights

    async def create_highlight(self, highlights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Manually create highlights"""
        return await self._request("POST", f"{self.v2_base_url}/highlights", json={"highlights": highlights}, api_version="v2")
