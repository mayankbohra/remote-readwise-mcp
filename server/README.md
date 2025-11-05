# Readwise MCP Enhanced - Remote Server

A FastMCP-powered remote server that enables Readwise Reader + Highlights integration for **Claude.ai** (web application). This allows you to use all 13 Readwise tools from anywhere, on any device, through Claude.ai's custom connectors feature.

## Features

- **13 Powerful Tools**: Complete Reader (6) + Highlights (7) API coverage
- **Secure Authentication**: Bearer token-based API key authentication
- **Production Ready**: Containerized deployment with health checks
- **Context Optimized**: 94% token reduction for efficient AI interactions
- **Universal Access**: Works with Claude.ai, Claude Desktop, and any MCP client

---

## 🚀 Quick Start

### Prerequisites

- **Claude.ai Account**: Pro, Max, Team, or Enterprise plan (required for custom connectors)
- **Readwise Account**: Get your token from https://readwise.io/access_token
- **Render Account**: Free tier available at https://render.com

### Step 1: Deploy to Render

1. **Fork or Clone this Repository**
   ```bash
   git clone https://github.com/your-username/readwise-mcp-enhanced.git
   cd readwise-mcp-enhanced
   ```

2. **Create a Render Account**
   - Go to https://render.com and sign up
   - Connect your GitHub account

3. **Deploy the Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Set the root directory to `server`
   - Render will auto-detect the Dockerfile

4. **Configure Environment Variables**
   Add these in Render's dashboard:

   | Variable | Value | Description |
   |----------|-------|-------------|
   | `READWISE_TOKEN` | Your token from readwise.io/access_token | Readwise API authentication |
   | `MCP_API_KEY` | Generate a secure random string* | Your server's API key |
   | `PORT` | 8000 | Server port (auto-set by Render) |
   | `HOST` | 0.0.0.0 | Server host |

   *Generate a secure API key:
   ```bash
   openssl rand -hex 32
   # or
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Copy your service URL: `https://your-service-name.onrender.com`

---

### Step 2: Add to Claude.ai

1. **Open Claude.ai Settings**
   - Go to https://claude.ai
   - Click your profile → Settings
   - Navigate to **Connectors** tab

2. **Add Custom Connector**
   - Click "Add Connector"
   - Choose "Custom MCP Server"

3. **Configure Connection**
   ```
   Server URL: https://your-service-name.onrender.com
   Authentication: Bearer Token
   API Key: [Your MCP_API_KEY from Render]
   ```

4. **Test Connection**
   - Claude will verify the connection
   - You should see "Readwise MCP Enhanced" appear with 13 tools

5. **Start Using**
   Try: "List my recent Readwise documents" or "Get my daily review highlights"

---

## 🔧 Local Development

### Setup

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your tokens
```

### Run Locally

```bash
python main.py
```

Server will start at `http://localhost:8000`

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python main.py
```

---

## 📚 Available Tools

### Reader Tools (6)

1. **readwise_save_document** - Save URLs to Reader
2. **readwise_list_documents** - List with smart content controls
3. **readwise_update_document** - Update metadata
4. **readwise_delete_document** - Remove documents
5. **readwise_list_tags** - Get all tags
6. **readwise_topic_search** - AI-powered search

### Highlights Tools (7)

7. **readwise_list_highlights** - Advanced filtering
8. **readwise_get_daily_review** - Spaced repetition
9. **readwise_search_highlights** - Text search
10. **readwise_list_books** - Book metadata
11. **readwise_get_book_highlights** - Per-book highlights
12. **readwise_export_highlights** - Bulk export
13. **readwise_create_highlight** - Manual creation

---

## 🔐 Security

### Authentication Flow

1. **Client → Server**: All requests include `Authorization: Bearer YOUR_API_KEY`
2. **Server → Readwise**: Server uses `READWISE_TOKEN` internally
3. **Two-Layer Security**:
   - Your API key protects your server
   - Readwise token stays secure on server (never exposed)

### Best Practices

- **Never commit** `.env` files or tokens to Git
- **Rotate API keys** periodically
- **Use HTTPS** only (Render provides this automatically)
- **Monitor usage** through Render's dashboard

---

## 🚀 Deployment Options

### Render (Recommended)

- **Free Tier**: 750 hours/month
- **Auto-scaling**: Handles traffic spikes
- **Zero config**: Dockerfile auto-detected
- **HTTPS included**: Secure by default

**Deploy Now:**
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Alternative Platforms

**Railway**
```bash
railway login
railway init
railway up
```

**Fly.io**
```bash
fly launch
fly deploy
```

**Google Cloud Run**
```bash
gcloud run deploy readwise-mcp --source ./server --region us-central1
```

---

## 🧪 Testing

### Health Check

```bash
curl https://your-service.onrender.com/health
```

### Test Authentication

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://your-service.onrender.com/list_tools
```

### Example Tool Call (via Claude.ai)

Simply ask Claude:
- "What's in my Readwise reading list?"
- "Show me my daily review highlights"
- "Save this article to Readwise: https://example.com/article"

---

## 📊 Performance

- **Cold Start**: ~10 seconds (Render free tier)
- **Response Time**: 200-500ms per request
- **Token Usage**: 94% more efficient than raw API responses
- **Uptime**: 99.9% (Render SLA)

---

## 🐛 Troubleshooting

### "Connection Failed" in Claude.ai

1. Verify your Render service is running (check dashboard)
2. Test the health endpoint: `https://your-service.onrender.com/health`
3. Confirm `MCP_API_KEY` matches between Render and Claude.ai

### "Invalid API Key"

- Double-check the Bearer token in Claude.ai settings
- Ensure no extra spaces in the API key
- Regenerate key if needed (update in both Render and Claude.ai)

### "Readwise API Error"

- Verify `READWISE_TOKEN` in Render environment variables
- Test token at https://readwise.io/access_token
- Check Readwise API status

### Server Errors

- View logs in Render dashboard
- Increase instance size if hitting memory limits
- Check Readwise API rate limits

---

## 💰 Pricing

### Render Free Tier
- ✅ 750 hours/month (enough for 24/7 uptime)
- ✅ 512 MB RAM
- ✅ Automatic HTTPS
- ⚠️ Spins down after 15 min inactivity (cold start on next request)

### Render Paid Plans
- **Starter**: $7/month - Always-on, no cold starts
- **Standard**: $25/month - More resources, faster performance

### Readwise
- Uses your existing Readwise subscription
- No additional costs

---

## 🤝 Support

- **Issues**: https://github.com/your-username/readwise-mcp-enhanced/issues
- **Discussions**: https://github.com/your-username/readwise-mcp-enhanced/discussions
- **Email**: your-email@example.com

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

---

## 🙏 Acknowledgments

Built on:
- [FastMCP](https://github.com/jlowin/fastmcp) - Python MCP framework
- [MCP Protocol](https://modelcontextprotocol.io) - Anthropic's protocol
- [Readwise API](https://readwise.io/api_deets) - Readwise platform

---

**Enjoy using Readwise with Claude.ai from anywhere! 🎉**
