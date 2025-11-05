"""FastMCP Server for Readwise Reader + Highlights Integration"""

import os
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from readwise_client import ReadwiseClient
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("Readwise MCP Enhanced")

# Get configuration from environment
READWISE_TOKEN = os.getenv("READWISE_TOKEN")
MCP_API_KEY = os.getenv("MCP_API_KEY")

if not READWISE_TOKEN:
    raise ValueError("READWISE_TOKEN environment variable is required")

if not MCP_API_KEY:
    logger.warning("MCP_API_KEY not set - server will run without authentication")

# Initialize Readwise client
client = ReadwiseClient(READWISE_TOKEN)


# ==================== Custom Authentication ====================
# Note: FastMCP 2.0+ handles auth differently
# We'll implement API key validation in the app setup below


# ==================== READER TOOLS (6) ====================

@mcp.tool()
async def readwise_save_document(
    url: str,
    tags: Optional[List[str]] = None,
    location: Optional[str] = "later",
    category: Optional[str] = "article"
) -> str:
    """
    Save a document to Readwise Reader.

    Args:
        url: The URL of the document to save
        tags: Optional list of tags to apply
        location: Where to save (new, later, archive, feed)
        category: Document category (article, email, rss, highlight, note, pdf, epub, tweet, video)

    Returns:
        JSON string with save result
    """
    try:
        kwargs = {}
        if tags:
            kwargs["tags"] = tags
        if location:
            kwargs["location"] = location
        if category:
            kwargs["category"] = category

        result = await client.save_document(url, **kwargs)
        return f"Document saved successfully: {result}"
    except Exception as e:
        logger.error(f"Error saving document: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_list_documents(
    location: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20,
    with_full_content: bool = False,
    content_max_length: Optional[int] = None
) -> str:
    """
    List documents from Readwise Reader with smart content controls.

    Args:
        location: Filter by location (new, later, archive, feed)
        category: Filter by category (article, email, rss, etc.)
        limit: Maximum number of documents to return (default: 20)
        with_full_content: Include full document content (warning: may be large)
        content_max_length: Limit content length per document

    Returns:
        JSON string with document list
    """
    try:
        documents = await client.list_documents(
            location=location,
            category=category,
            limit=limit
        )

        # Process content if requested
        if not with_full_content:
            for doc in documents:
                doc.pop("content", None)
        elif content_max_length:
            for doc in documents:
                if "content" in doc and len(doc["content"]) > content_max_length:
                    doc["content"] = doc["content"][:content_max_length] + "..."

        return f"Found {len(documents)} documents: {documents}"
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_update_document(
    document_id: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    summary: Optional[str] = None,
    location: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> str:
    """
    Update document metadata in Readwise Reader.

    Args:
        document_id: The ID of the document to update
        title: New title
        author: New author
        summary: New summary
        location: New location (new, later, archive, feed)
        tags: New tags list

    Returns:
        JSON string with update result
    """
    try:
        updates = {}
        if title:
            updates["title"] = title
        if author:
            updates["author"] = author
        if summary:
            updates["summary"] = summary
        if location:
            updates["location"] = location
        if tags:
            updates["tags"] = tags

        result = await client.update_document(document_id, updates)
        return f"Document updated successfully: {result}"
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_delete_document(document_id: str) -> str:
    """
    Delete a document from Readwise Reader.

    Args:
        document_id: The ID of the document to delete

    Returns:
        Success or error message
    """
    try:
        await client.delete_document(document_id)
        return f"Document {document_id} deleted successfully"
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_list_tags() -> str:
    """
    Get all tags from Readwise Reader.

    Returns:
        JSON string with list of tags
    """
    try:
        tags = await client.list_tags()
        return f"Found {len(tags)} tags: {tags}"
    except Exception as e:
        logger.error(f"Error listing tags: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_topic_search(
    query: str,
    location: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
) -> str:
    """
    Search documents by topic in Readwise Reader.

    Args:
        query: Search query (searches title, summary, notes, tags)
        location: Filter by location
        category: Filter by category
        limit: Maximum results to return

    Returns:
        JSON string with search results
    """
    try:
        results = await client.topic_search(
            query=query,
            location=location,
            category=category,
            limit=limit
        )
        return f"Found {len(results)} matching documents: {results}"
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return f"Error: {str(e)}"


# ==================== HIGHLIGHTS TOOLS (7) ====================

@mcp.tool()
async def readwise_list_highlights(
    book_id: Optional[int] = None,
    page_size: int = 100,
    page: int = 1,
    highlighted_at__gt: Optional[str] = None,
    highlighted_at__lt: Optional[str] = None
) -> str:
    """
    List highlights from Readwise with advanced filtering.

    Args:
        book_id: Filter by specific book ID
        page_size: Number of highlights per page (max 1000)
        page: Page number
        highlighted_at__gt: Filter highlights after this date (ISO 8601)
        highlighted_at__lt: Filter highlights before this date (ISO 8601)

    Returns:
        JSON string with highlights
    """
    try:
        filters = {}
        if highlighted_at__gt:
            filters["highlighted_at__gt"] = highlighted_at__gt
        if highlighted_at__lt:
            filters["highlighted_at__lt"] = highlighted_at__lt

        result = await client.list_highlights(
            page_size=page_size,
            page=page,
            book_id=book_id,
            **filters
        )

        # Optimize response - only return essential fields
        highlights = result.get("results", [])
        optimized = [
            {
                "id": h.get("id"),
                "text": h.get("text"),
                "note": h.get("note"),
                "book_id": h.get("book_id"),
                "highlighted_at": h.get("highlighted_at")
            }
            for h in highlights
        ]

        return f"Found {len(optimized)} highlights: {optimized}"
    except Exception as e:
        logger.error(f"Error listing highlights: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_get_daily_review() -> str:
    """
    Get daily review highlights (spaced repetition learning system).

    Returns:
        JSON string with daily review highlights
    """
    try:
        result = await client.get_daily_review()

        # Optimize response
        highlights = result.get("highlights", [])
        optimized = [
            {
                "id": h.get("id"),
                "text": h.get("text"),
                "title": h.get("title"),
                "author": h.get("author"),
                "note": h.get("note")
            }
            for h in highlights
        ]

        return f"Daily review ({len(optimized)} highlights): {optimized}"
    except Exception as e:
        logger.error(f"Error getting daily review: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_search_highlights(
    query: str,
    page_size: int = 100,
    page: int = 1
) -> str:
    """
    Search highlights by text query.

    Args:
        query: Search term (searches highlight text and notes)
        page_size: Number of results per page
        page: Page number

    Returns:
        JSON string with matching highlights
    """
    try:
        results = await client.search_highlights(
            query=query,
            page_size=page_size,
            page=page
        )

        # Optimize response
        optimized = [
            {
                "id": h.get("id"),
                "text": h.get("text"),
                "book_id": h.get("book_id"),
                "note": h.get("note")
            }
            for h in results
        ]

        return f"Found {len(optimized)} matching highlights: {optimized}"
    except Exception as e:
        logger.error(f"Error searching highlights: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_list_books(
    category: Optional[str] = None,
    page_size: int = 100,
    page: int = 1,
    last_highlight_at__gt: Optional[str] = None
) -> str:
    """
    List books with highlight metadata.

    Args:
        category: Filter by category (books, articles, tweets, podcasts)
        page_size: Number of books per page
        page: Page number
        last_highlight_at__gt: Filter books with highlights after this date

    Returns:
        JSON string with books
    """
    try:
        filters = {}
        if last_highlight_at__gt:
            filters["last_highlight_at__gt"] = last_highlight_at__gt

        result = await client.list_books(
            page_size=page_size,
            page=page,
            category=category,
            **filters
        )

        # Optimize response
        books = result.get("results", [])
        optimized = [
            {
                "id": b.get("id"),
                "title": b.get("title"),
                "author": b.get("author"),
                "category": b.get("category"),
                "num_highlights": b.get("num_highlights")
            }
            for b in books
        ]

        return f"Found {len(optimized)} books: {optimized}"
    except Exception as e:
        logger.error(f"Error listing books: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_get_book_highlights(book_id: int) -> str:
    """
    Get all highlights from a specific book.

    Args:
        book_id: The ID of the book

    Returns:
        JSON string with book highlights
    """
    try:
        result = await client.get_book_highlights(book_id)

        highlights = result.get("results", [])
        optimized = [
            {
                "id": h.get("id"),
                "text": h.get("text"),
                "note": h.get("note"),
                "location": h.get("location")
            }
            for h in highlights
        ]

        return f"Found {len(optimized)} highlights for book {book_id}: {optimized}"
    except Exception as e:
        logger.error(f"Error getting book highlights: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_export_highlights(
    updated_after: Optional[str] = None,
    include_deleted: bool = False
) -> str:
    """
    Bulk export highlights for analysis and backup.

    Args:
        updated_after: Export only highlights updated after this date (ISO 8601)
        include_deleted: Include deleted highlights

    Returns:
        JSON string with exported highlights
    """
    try:
        highlights = await client.export_highlights(
            updated_after=updated_after,
            include_deleted=include_deleted
        )

        # Optimize response
        optimized = [
            {
                "id": h.get("id"),
                "text": h.get("text"),
                "book_id": h.get("book_id"),
                "updated": h.get("updated")
            }
            for h in highlights[:1000]  # Limit to prevent huge responses
        ]

        return f"Exported {len(highlights)} highlights (showing first 1000): {optimized}"
    except Exception as e:
        logger.error(f"Error exporting highlights: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def readwise_create_highlight(
    text: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    note: Optional[str] = None,
    category: str = "books",
    highlighted_at: Optional[str] = None
) -> str:
    """
    Manually create a highlight in Readwise.

    Args:
        text: The highlight text (required)
        title: Book/article title
        author: Author name
        note: Your note on the highlight
        category: Category (books, articles, tweets, podcasts)
        highlighted_at: When it was highlighted (ISO 8601)

    Returns:
        JSON string with creation result
    """
    try:
        highlight_data = {"text": text}
        if title:
            highlight_data["title"] = title
        if author:
            highlight_data["author"] = author
        if note:
            highlight_data["note"] = note
        if category:
            highlight_data["category"] = category
        if highlighted_at:
            highlight_data["highlighted_at"] = highlighted_at

        result = await client.create_highlight([highlight_data])
        return f"Highlight created successfully: {result}"
    except Exception as e:
        logger.error(f"Error creating highlight: {e}")
        return f"Error: {str(e)}"


# ==================== Server Entry Point ====================

def create_app():
    """Create the ASGI app with authentication wrapper"""
    from starlette.applications import Starlette
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware
    from starlette.responses import JSONResponse
    from starlette.routing import Route, Mount

    async def health_check(request):
        return JSONResponse({
            "status": "healthy",
            "service": "readwise-mcp-enhanced",
            "version": "1.0.0",
            "authentication": "enabled" if MCP_API_KEY else "disabled"
        })

    async def auth_middleware(request, call_next):
        # Skip auth for health check and OAuth discovery endpoints
        if request.url.path in ["/health", "/.well-known/oauth-protected-resource",
                                "/.well-known/oauth-authorization-server", "/register"]:
            return await call_next(request)

        # Check API key if configured
        if MCP_API_KEY:
            auth_header = request.headers.get("authorization", "")
            if not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {"error": "Missing or invalid Authorization header"},
                    status_code=401
                )

            token = auth_header.replace("Bearer ", "")
            if token != MCP_API_KEY:
                return JSONResponse(
                    {"error": "Invalid API key"},
                    status_code=401
                )

        return await call_next(request)

    # Get the FastMCP ASGI app
    mcp_app = mcp.http_app()

    # Create wrapper app with auth and CORS
    # IMPORTANT: Pass the FastMCP app's lifespan to Starlette
    # FastMCP's http_app() expects to handle requests at its root
    # So we mount it at / and it will handle /mcp endpoint internally
    app = Starlette(
        routes=[
            Route("/health", health_check, methods=["GET", "HEAD"]),
            Mount("/", mcp_app)  # FastMCP handles /mcp internally
        ],
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["https://claude.ai", "https://claude.com", "https://*.anthropic.com"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
        lifespan=mcp_app.lifespan  # Fix: Pass FastMCP's lifespan manager
    )

    # Add auth middleware
    @app.middleware("http")
    async def add_auth(request, call_next):
        return await auth_middleware(request, call_next)

    return app


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting Readwise MCP Enhanced server on {host}:{port}")
    logger.info(f"Authentication: {'Enabled' if MCP_API_KEY else 'Disabled (WARNING: Not secure for production)'}")

    # Create and run the app
    app = create_app()
    uvicorn.run(app, host=host, port=port)
