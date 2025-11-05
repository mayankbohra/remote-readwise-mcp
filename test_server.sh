#!/bin/bash

# Test script for Readwise MCP Enhanced server
# Usage: ./test_server.sh [SERVER_URL] [API_KEY]

SERVER_URL=${1:-"http://localhost:8000"}
API_KEY=${2:-""}

echo "🧪 Testing Readwise MCP Enhanced Server"
echo "Server: $SERVER_URL"
echo "Auth: ${API_KEY:+Enabled}"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "1️⃣  Testing health endpoint..."
if curl -s "$SERVER_URL/health" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    exit 1
fi
echo ""

# Test 2: Authentication (if API key provided)
if [ -n "$API_KEY" ]; then
    echo "2️⃣  Testing authentication..."

    # Test without auth (should fail)
    if curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/list_tools" | grep -q "401"; then
        echo -e "${GREEN}✓ Unauthorized request blocked${NC}"
    else
        echo -e "${RED}✗ Should block unauthorized requests${NC}"
    fi

    # Test with auth (should succeed)
    if curl -s -H "Authorization: Bearer $API_KEY" "$SERVER_URL/list_tools" | grep -q "tools"; then
        echo -e "${GREEN}✓ Authenticated request succeeded${NC}"
    else
        echo -e "${RED}✗ Authenticated request failed${NC}"
    fi
    echo ""
fi

# Test 3: List tools
echo "3️⃣  Testing tool listing..."
AUTH_HEADER=""
if [ -n "$API_KEY" ]; then
    AUTH_HEADER="-H \"Authorization: Bearer $API_KEY\""
fi

TOOLS_RESPONSE=$(eval curl -s $AUTH_HEADER "$SERVER_URL/list_tools")
TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | grep -o "readwise_" | wc -l)

if [ "$TOOL_COUNT" -eq 13 ]; then
    echo -e "${GREEN}✓ All 13 tools available${NC}"
    echo "  Reader tools (6):"
    echo "$TOOLS_RESPONSE" | grep -o "readwise_[a-z_]*document" | head -6 | sed 's/^/    - /'
    echo "$TOOLS_RESPONSE" | grep -o "readwise_[a-z_]*tags" | sed 's/^/    - /'
    echo "$TOOLS_RESPONSE" | grep -o "readwise_[a-z_]*search" | head -1 | sed 's/^/    - /'
    echo ""
    echo "  Highlights tools (7):"
    echo "$TOOLS_RESPONSE" | grep -o "readwise_[a-z_]*highlight[s]*" | sed 's/^/    - /'
    echo "$TOOLS_RESPONSE" | grep -o "readwise_[a-z_]*book[s]*" | sed 's/^/    - /'
    echo "$TOOLS_RESPONSE" | grep -o "readwise_[a-z_]*review" | sed 's/^/    - /'
else
    echo -e "${YELLOW}⚠ Expected 13 tools, found $TOOL_COUNT${NC}"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✨ Server is ready to use!${NC}"
echo ""
echo "📝 Next steps:"
echo "   1. Copy your server URL: $SERVER_URL"
if [ -n "$API_KEY" ]; then
    echo "   2. Copy your API key: $API_KEY"
fi
echo "   3. Add to Claude.ai Settings → Connectors"
echo "   4. Start using Readwise with Claude!"
echo ""
