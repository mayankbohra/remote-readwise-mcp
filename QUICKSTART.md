# Readwise MCP Enhanced - Quick Start 🚀

Get Readwise working with Claude.ai in 5 minutes!

## Step 1: Get Your Readwise Token (1 min)

1. Go to https://readwise.io/access_token
2. Copy your token
3. Done!

## Step 2: Deploy to Render (3 min)

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect this GitHub repo
4. Fill in:
   - **Root Directory**: `server`
   - **Environment Variable**:
     - Name: `READWISE_TOKEN`
     - Value: (paste your token from Step 1)
5. Click "Create Web Service"
6. Wait 2-3 minutes for deployment
7. Copy your URL: `https://YOUR-SERVICE-NAME.onrender.com`

## Step 3: Connect to Claude.ai (1 min)

1. Open Claude.ai → Settings → Connectors
2. Click "+ Add custom connector"
3. Fill in:
   - **Name**: `Readwise`
   - **URL**: `https://YOUR-SERVICE-NAME.onrender.com/mcp`

     ⚠️ **Important**: Add `/mcp` at the end!
4. Click "Add"
5. Done! ✨

## Step 4: Try It Out!

Ask Claude:

```
"List my Readwise documents in the 'later' location"
```

```
"Get my daily review highlights"
```

```
"Search my highlights for 'productivity'"
```

```
"Save this article: https://paulgraham.com/startupideas.html"
```

## That's It!

You now have 13 Readwise tools available in Claude.ai:

### Reader Tools (6)
✅ Save documents
✅ List & browse
✅ Update metadata
✅ Delete documents
✅ Manage tags
✅ Topic search

### Highlights Tools (7)
✅ List highlights
✅ Daily review
✅ Search highlights
✅ Browse books
✅ Book highlights
✅ Export highlights
✅ Create highlights

## Need Help?

- 📖 [Full Documentation](./server/CLAUDE_AI_SETUP.md)
- 🐛 [Report Issues](https://github.com/YOUR_USERNAME/readwise-mcp-enhanced/issues)
- ❓ [Common Problems](./server/CLAUDE_AI_SETUP.md#troubleshooting)

## Pro Tips

### Add Authentication (Optional)

For extra security:

1. Generate a key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Add to Render: `MCP_API_KEY=your_generated_key`
3. In Claude.ai: Advanced settings → OAuth Client Secret → (paste key)
4. Redeploy

### Upgrade for Better Performance

Render Free tier has cold starts (10-15 sec first request).

Upgrade to Starter ($7/month) for:
- ✅ Always-on (no cold starts)
- ✅ Faster response times
- ✅ Better for team use

## Next Steps

- ⭐ Star the repository
- 🔔 Watch for updates
- 🤝 Share with Readwise users
- 💡 Suggest new features

Enjoy using Readwise with Claude! 🎉
