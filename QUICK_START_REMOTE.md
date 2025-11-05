# 🚀 Quick Start: Deploy Readwise MCP for Claude.ai

**Goal**: Get your Readwise data accessible in Claude.ai within 10 minutes!

## Prerequisites

- ✅ Claude.ai account (Pro, Max, Team, or Enterprise plan)
- ✅ Readwise account
- ✅ GitHub account (for deployment)

---

## Step 1: Get Your Readwise Token (1 min)

1. Go to https://readwise.io/access_token
2. Copy your access token
3. Keep it handy (you'll need it in Step 3)

---

## Step 2: Deploy to Render (3 min)

### Option A: One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Sign up for Render (free tier available)
3. Connect your GitHub account
4. Skip to Step 3 for environment variables

### Option B: Manual Deploy

1. **Sign up** at https://render.com
2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Choose "Deploy from Git"
   - Connect this repository
3. **Configure**:
   - **Name**: `readwise-mcp` (or your choice)
   - **Root Directory**: `server`
   - **Runtime**: Docker
   - **Plan**: Free

---

## Step 3: Configure Environment Variables (2 min)

In Render's dashboard, go to **Environment** tab and add:

### Required Variables

```bash
READWISE_TOKEN=<paste_your_token_from_step_1>
MCP_API_KEY=<generate_secure_random_string>
```

### Generate MCP_API_KEY

**Option 1 - Terminal**:
```bash
openssl rand -hex 32
```

**Option 2 - Python**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Option 3 - Online**:
Visit https://www.random.org/strings/ and generate a 64-character hex string

⚠️ **Save this API key** - you'll need it in Step 5!

### Optional Variables (already set by default)

```bash
PORT=8000
HOST=0.0.0.0
```

Click **Save Changes** and wait for deployment (~2 minutes).

---

## Step 4: Verify Deployment (1 min)

1. Copy your Render service URL: `https://YOUR-SERVICE-NAME.onrender.com`
2. Open in browser: `https://YOUR-SERVICE-NAME.onrender.com/health`
3. You should see:
   ```json
   {
     "status": "healthy",
     "service": "readwise-mcp-enhanced",
     "version": "1.0.0",
     "authentication": "enabled"
   }
   ```

✅ If you see this, your server is running!

---

## Step 5: Connect to Claude.ai (3 min)

1. **Open Claude.ai**
   - Go to https://claude.ai
   - Sign in with your Pro/Max/Team/Enterprise account

2. **Navigate to Connectors**
   - Click your profile icon (bottom left)
   - Select "Settings"
   - Click "Connectors" tab

3. **Add Custom Connector**
   - Click "+ Add Connector"
   - Select "Custom MCP Server"

4. **Enter Configuration**
   ```
   Name: Readwise
   Server URL: https://YOUR-SERVICE-NAME.onrender.com
   Authentication: Bearer Token
   Token: <your_MCP_API_KEY_from_step_3>
   ```

5. **Test Connection**
   - Click "Test Connection"
   - Should show: ✅ "Connected successfully"
   - You'll see "13 tools available"

6. **Save**
   - Click "Save Connector"
   - Done!

---

## 🎉 You're Ready!

Try these in Claude.ai:

### Example Queries

1. **"What's in my Readwise reading list?"**
   - Lists your saved documents

2. **"Show me my daily review highlights"**
   - Gets your spaced repetition highlights

3. **"Search my highlights for productivity tips"**
   - Searches across all your highlights

4. **"Save this article to Readwise: https://example.com/article"**
   - Saves new content to your library

5. **"List all my tags"**
   - Shows your document tags

### Available Features

✅ Save web pages, articles, PDFs
✅ List and search documents
✅ Update document metadata
✅ Browse highlights by book
✅ Daily review (spaced repetition)
✅ Search all highlights
✅ Export for backup
✅ Create manual highlights

---

## 📱 Use Anywhere

Once configured, you can use your Readwise integration:
- ✅ On Claude.ai (web)
- ✅ On your phone (via Claude.ai mobile)
- ✅ On any device with a browser
- ✅ No local installation needed!

---

## 🛠️ Troubleshooting

### "Connection Failed" Error

1. Check your Render service is running (visit health URL)
2. Verify `MCP_API_KEY` matches in both Render and Claude.ai
3. Ensure no extra spaces in the API key

### "Authentication Error"

1. Double-check your Render URL is correct
2. Verify Bearer token format: `Bearer YOUR_API_KEY`
3. Try regenerating the API key

### Health Check Returns Error

1. View logs in Render dashboard
2. Check `READWISE_TOKEN` is set correctly
3. Verify token at https://readwise.io/access_token

### Need More Help?

- 📖 Full docs: [server/README.md](./server/README.md)
- 🚀 Deployment guide: [server/DEPLOYMENT.md](./server/DEPLOYMENT.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/your-repo/issues)

---

## 💰 Costs

**Free Tier** (sufficient for personal use):
- ✅ Render: 750 hours/month (24/7 uptime)
- ✅ Readwise: Uses your existing subscription
- ⚠️ Cold starts after 15 min inactivity (10 sec delay)

**Paid Tier** (for production):
- 💵 Render Starter: $7/month (always-on, no cold starts)
- 💵 Claude.ai: Your existing Pro/Max plan

---

## 🔐 Security Notes

✅ All requests encrypted via HTTPS
✅ Two-layer authentication (MCP key + Readwise token)
✅ Your Readwise token stays on the server (never exposed)
✅ Bearer token authentication for all API calls

**Keep your API keys secure!**
- Never commit to Git
- Don't share publicly
- Rotate periodically

---

## 🎯 Next Steps

1. ✅ Complete this Quick Start
2. 📚 Read [server/README.md](./server/README.md) for advanced features
3. 🚀 Explore all 13 tools in Claude.ai
4. 🔄 Set up automatic backups using the export tool
5. 🤝 Share with your team (for Team/Enterprise plans)

---

**Happy reading! 📖✨**
