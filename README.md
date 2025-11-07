# Readwise MCP Server 📚

Connect your [Readwise](https://readwise.io/) account to Claude AI and access all your highlights, books, and reading list directly in conversations!

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0+-green.svg)](https://github.com/jlowin/fastmcp)

## ✨ What Can You Do?

Once set up, you can ask Claude:

- **"What's in my Readwise reading list?"** - View all saved articles
- **"Show me my daily review highlights"** - Get your spaced repetition review
- **"Search my highlights for 'productivity tips'"** - Find specific highlights
- **"Save this article: https://example.com"** - Add to your reading list
- **"List all my tags"** - See your document tags
- **"Export all my highlights"** - Backup your entire library

## 🚀 10-Minute Setup

### What You Need

- ✅ Readwise account ([Get one here](https://readwise.io/))
- ✅ Claude AI (Pro/Team/Enterprise - any plan with MCP support)
- ✅ Free [Render](https://render.com/) account for hosting

### Step 1: Get Your Readwise Token (1 min)

1. Go to https://readwise.io/access_token
2. Copy your access token
3. Keep it handy

### Step 2: Fork & Deploy Server (5 min)

#### Option A: Deploy to Render (Recommended)

1. **Fork this repository**:
   - Click "Fork" button at the top of this GitHub page
   - This creates your own copy of the code

2. **Sign up at [Render](https://render.com)** (free tier available)

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Choose "Connect a Git repository"
   - Select your forked repository from the list

4. **Configure**:
   - **Name**: `readwise-mcp` (or your choice)
   - **Runtime**: Docker (auto-detected)
   - **Plan**: Free

5. **Add Environment Variable** (in Render dashboard):
   ```bash
   READWISE_TOKEN=<paste_your_token_from_step_1>
   ```

   That's it! No API key needed.

6. Click **Create Web Service** and wait ~2 minutes

#### Option B: Other Platforms

<details>
<summary>Railway / Fly.io / Google Cloud Run</summary>

The server works on any platform that supports Docker. See `Dockerfile` for configuration.
</details>

### Step 3: Verify It's Running (1 min)

Visit: `https://YOUR-SERVICE-NAME.onrender.com/health`

You should see:
```json
{
  "status": "healthy",
  "service": "readwise-mcp-enhanced",
  "authentication": "enabled"
}
```

✅ If you see this, you're good to go!

### Step 4: Connect to Claude (3 min)

1. **Open Claude AI** at https://claude.ai

2. **Go to Settings** → **Integrations** (or similar MCP section)

3. **Add MCP Server**:
   ```
   Name: Readwise
   URL: https://YOUR-SERVICE-NAME.onrender.com
   ```

   No API key needed!

4. **Test Connection** - Should show "12 tools available"

5. **Save** and you're done! 🎉

### Step 5: Start Using!

Try asking Claude:
- "What did I save to Readwise today?"
- "Show me highlights from my AI books"
- "Get my daily review"

## 📖 All Available Features

### Reader Tools (5 tools)
- **Save documents** - Add URLs to your reading list
- **List documents** - Browse with filters (location, category, author, date)
- **Update documents** - Edit titles, tags, notes
- **Delete documents** - Remove from library
- **List tags** - View all your tags

### Highlights Tools (7 tools)
- **List highlights** - Browse with date filters
- **Daily review** - Spaced repetition system
- **Search highlights** - Find by text query using enhanced MCP endpoint with vector/semantic search
- **List books** - View books with highlight counts
- **Get book highlights** - All highlights from a specific book
- **Export highlights** - Backup everything
- **Create highlights** - Add manual highlights

### 🚀 Advanced Features
- ✅ **Enhanced MCP Search** - Uses Readwise's MCP endpoint with vector/semantic search for better results
- ✅ **Unlimited pagination** - Fetch ALL your data
- ✅ **Incremental sync** - Get only new/updated items
- ✅ **Smart filtering** - Filter by author, site, dates
- ✅ **Bulk export** - Backup your entire library

## 🆓 Cost

**100% Free for Personal Use:**
- ✅ Render: 750 hours/month (runs 24/7)
- ✅ Uses your existing Readwise subscription
- ⚠️ Server "sleeps" after 15 min (10 sec wake-up on first request)

**Optional Upgrade:**
- 💵 $7/month for Render Starter (always-on, no sleep)

## 🛠️ Troubleshooting

### "Connection Failed" in Claude

1. Visit `https://YOUR-SERVICE.onrender.com/health` - Should return healthy status
2. Verify the URL is correct in Claude settings
3. Wait 10 seconds if server was sleeping (free tier)

### Server Takes Long to Respond

- Free tier "sleeps" after 15 min inactivity
- First request after sleep takes ~10 seconds to wake up
- This is normal - subsequent requests are fast!

### "Readwise API Error"

- Check your `READWISE_TOKEN` in Render dashboard
- Verify token at https://readwise.io/access_token
- Token might have expired - get a new one

### Still Need Help?

- 📖 See [CLAUDE_AI_SETUP.md](CLAUDE_AI_SETUP.md) for detailed Claude setup
- 🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for advanced deployment options
- 🐛 [Open an issue](https://github.com/YOUR-USERNAME/readwise-mcp-server/issues)

## 🔒 Security & Privacy

- ✅ All requests encrypted via HTTPS
- ✅ Your Readwise token stays on your server (never exposed to Claude)
- ✅ Open source - inspect the code yourself!
- ⚠️ **Important**: Your server URL is public but only works with YOUR Readwise token

**Keep your secrets safe:**
- Never commit `.env` files with tokens
- Don't share your Readwise token
- Only you can access your data through your server

## 🧪 For Developers

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your tokens

# Run
python main.py

# Test
python test_all_tools.py
```

### Docker

```bash
docker build -t readwise-mcp .
docker run -p 8000:8000 \
  -e READWISE_TOKEN=your_token \
  readwise-mcp
```

### Project Structure

```
readwise-mcp-server/
├── main.py              # FastMCP server (12 tools with enhanced MCP search)
├── readwise_client.py   # Readwise API client (supports MCP endpoints)
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container config
├── render.yaml         # Render deployment
└── test_all_tools.py   # Test suite
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🙏 Credits

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - Python MCP framework
- [Readwise API](https://readwise.io/api_deets) - Readwise platform
- [MCP Protocol](https://modelcontextprotocol.io) - Anthropic's protocol

## ⭐ Support

If you find this useful, please star the repository!

---

**Made with ❤️ for the Readwise and Claude AI community**
