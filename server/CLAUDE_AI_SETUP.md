# Setting Up Readwise MCP with Claude.ai

Complete guide to connect your Readwise MCP server to Claude.ai web interface.

## Prerequisites

- Claude Pro, Max, Team, or Enterprise plan
- Readwise account with API access
- Deployed MCP server (Render, Railway, etc.)

## Step 1: Deploy Your Server

### Option A: Deploy to Render (Recommended)

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `readwise-mcp-enhanced`
   - **Root Directory**: `server`
   - **Runtime**: Docker
   - **Instance Type**: Free (or paid for better performance)

6. Add Environment Variables:
   ```
   READWISE_TOKEN=your_readwise_token_here
   PORT=10000
   HOST=0.0.0.0
   ```

7. **Optional - Add Authentication** (recommended for production):
   ```
   MCP_API_KEY=your_secure_random_key_here
   ```
   Generate a secure key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

8. Click "Create Web Service" and wait 2-3 minutes

9. Your server URL will be: `https://YOUR-SERVICE-NAME.onrender.com`

## Step 2: Verify Deployment

Test your server is working:

```bash
# Health check
curl https://YOUR-SERVICE-NAME.onrender.com/health

# Expected response:
# {"status":"healthy","service":"readwise-mcp-enhanced","version":"1.0.0"}
```

## Step 3: Connect to Claude.ai

### For Individual Users (Pro/Max)

1. **Open Claude.ai Settings**
   - Go to https://claude.ai
   - Click your profile icon (bottom left)
   - Select "Settings"
   - Click "Connectors" in the sidebar

2. **Add Custom Connector**
   - Scroll to bottom
   - Click "+ Add custom connector"

3. **Configure Connection**

   **Important: Add `/mcp` to your URL!**

   Fill in:
   - **Name**: `Readwise MCP Enhanced`
   - **Server URL**: `https://YOUR-SERVICE-NAME.onrender.com/mcp`

   ⚠️ **Critical**: The URL must end with `/mcp` (not just your domain)

4. **Authentication (if you set MCP_API_KEY)**

   If you added `MCP_API_KEY` environment variable:
   - Click "Advanced settings"
   - Enter in **OAuth Client Secret**: Your `MCP_API_KEY` value
   - Leave OAuth Client ID empty

   If you did NOT set MCP_API_KEY (authless mode):
   - Leave Advanced settings empty
   - Click "Add"

5. **Test Connection**
   - Click "Add"
   - Claude will verify the server
   - You should see "Connected" status

### For Team/Enterprise

Team Admins/Owners:
1. Go to Admin Console → Connectors
2. Follow the same steps as above
3. The connector will be available to all team members

## Step 4: Start Using

Once connected, you can ask Claude:

```
"List my Readwise documents in the 'later' location"
"Get my daily review highlights"
"Search my highlights for 'productivity'"
"Save this article to Readwise: https://example.com/article"
```

## Available Tools

### Reader Tools (6)
1. **readwise_save_document** - Save URLs to Reader
2. **readwise_list_documents** - Browse your library
3. **readwise_update_document** - Update metadata
4. **readwise_delete_document** - Remove documents
5. **readwise_list_tags** - View all tags
6. **readwise_topic_search** - Search by topic

### Highlights Tools (7)
7. **readwise_list_highlights** - Browse highlights
8. **readwise_get_daily_review** - Spaced repetition review
9. **readwise_search_highlights** - Search highlight text
10. **readwise_list_books** - View source books
11. **readwise_get_book_highlights** - Highlights from specific book
12. **readwise_export_highlights** - Bulk export
13. **readwise_create_highlight** - Manually add highlights

## Troubleshooting

### Connection Fails

**Issue**: "Failed to connect" error

**Solutions**:
1. ✅ Verify URL ends with `/mcp`: `https://your-server.com/mcp`
2. ✅ Check server is running: `curl https://your-server.com/health`
3. ✅ If using authentication, verify API key matches
4. ✅ Check Render logs for errors
5. ✅ Try removing and re-adding the connector

### "No tools available"

**Issue**: Connected but Claude says "no tools available"

**Solutions**:
1. Check `READWISE_TOKEN` is set correctly in Render environment
2. Test Readwise API directly:
   ```bash
   curl -H "Authorization: Token YOUR_TOKEN" \
        https://readwise.io/api/v3/list
   ```
3. Restart the Render service
4. Check logs for startup errors

### Authentication Errors

**Issue**: 401 Unauthorized or 403 Forbidden

**Solutions**:
1. If using `MCP_API_KEY`:
   - Verify it's set in Render environment
   - Verify you entered it correctly in Claude.ai Advanced settings
   - Try regenerating a new key
2. If NOT using `MCP_API_KEY`:
   - Remove it from Render environment
   - Don't enter anything in Advanced settings
   - Redeploy the service

### Cold Starts (Free Tier)

**Issue**: First request after inactivity is slow

**Explanation**: Render free tier spins down after 15 min of inactivity

**Solutions**:
1. Upgrade to Render Starter ($7/month) for always-on
2. Accept 10-15 second cold start (fine for personal use)
3. Use a ping service to keep it warm (e.g., UptimeRobot)

## Security Best Practices

### For Personal Use
- ✅ Use `MCP_API_KEY` for basic auth
- ✅ Keep your API keys secret
- ✅ Don't share your server URL publicly

### For Team/Production Use
- ✅ Use paid Render instance (always-on, better security)
- ✅ Implement proper OAuth (see OAuth setup guide)
- ✅ Monitor usage in Render dashboard
- ✅ Rotate API keys periodically
- ✅ Review logs regularly

## Advanced: OAuth Setup

For production/team use, consider implementing OAuth with:
- Auth0
- WorkOS
- Descope
- AWS Cognito

See `server/docs/OAuth_SETUP.md` for detailed guide.

## Support

- **Server Issues**: Check [Render Dashboard](https://dashboard.render.com) logs
- **Readwise API**: Visit [Readwise Help](https://readwise.io/help)
- **Claude.ai Connectors**: See [Claude Help Center](https://support.claude.com)
- **GitHub Issues**: Report bugs at project repository

## Cost Summary

- **Readwise**: Existing subscription ($7.99/month)
- **Render Free**: $0 (with cold starts)
- **Render Starter**: $7/month (always-on, recommended)
- **Claude**: Pro ($20/month) or Team/Enterprise

**Total**: $0-7/month + Claude subscription
