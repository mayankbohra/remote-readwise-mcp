# Deployment Guide

## Quick Deploy to Render

### Step 1: Prepare Your Repository

```bash
# Ensure server/ directory is committed
git add server/
git commit -m "Add FastMCP remote server"
git push
```

### Step 2: Create Render Web Service

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `readwise-mcp-enhanced` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `server`
   - **Runtime**: Docker
   - **Instance Type**: Free

### Step 3: Environment Variables

Add in Render dashboard under "Environment":

```bash
READWISE_TOKEN=<your_readwise_token>
MCP_API_KEY=<generate_secure_random_string>
PORT=8000
HOST=0.0.0.0
```

Generate secure API key:
```bash
# Option 1: Using OpenSSL
openssl rand -hex 32

# Option 2: Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 3: Online
# Visit: https://www.random.org/strings/
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait 2-3 minutes for build and deployment
3. Your service URL: `https://YOUR-SERVICE-NAME.onrender.com`

### Step 5: Verify Deployment

```bash
# Test health endpoint
curl https://YOUR-SERVICE-NAME.onrender.com/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "readwise-mcp-enhanced",
#   "version": "1.0.0",
#   "authentication": "enabled"
# }
```

---

## Alternative Platforms

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
cd server
railway init

# Add environment variables
railway variables set READWISE_TOKEN=your_token
railway variables set MCP_API_KEY=your_api_key

# Deploy
railway up
```

### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch (in server directory)
cd server
flyctl launch

# Set secrets
flyctl secrets set READWISE_TOKEN=your_token
flyctl secrets set MCP_API_KEY=your_api_key

# Deploy
flyctl deploy
```

### Google Cloud Run

```bash
# Prerequisites: Install gcloud CLI and authenticate

# Deploy
cd server
gcloud run deploy readwise-mcp-enhanced \
  --source . \
  --region us-central1 \
  --set-env-vars READWISE_TOKEN=your_token,MCP_API_KEY=your_api_key \
  --allow-unauthenticated

# Get URL
gcloud run services describe readwise-mcp-enhanced --region us-central1 --format 'value(status.url)'
```

---

## Connecting to Claude.ai

### For Pro/Max/Team/Enterprise Users

1. **Open Claude.ai Settings**
   - Navigate to https://claude.ai
   - Click profile icon → Settings
   - Select "Connectors" tab

2. **Add Custom Connector**
   - Click "+ Add Connector"
   - Select "Custom MCP Server"

3. **Configure**
   ```
   Name: Readwise MCP Enhanced
   Server URL: https://your-service.onrender.com
   Authentication Type: Bearer Token
   Token: <your_MCP_API_KEY>
   ```

4. **Test Connection**
   - Claude will verify the server
   - You should see 13 tools available

5. **Start Using**
   - "List my Readwise documents"
   - "Get my daily review highlights"
   - "Search my highlights for 'productivity'"

---

## Monitoring & Maintenance

### Check Logs (Render)

1. Go to Render dashboard
2. Select your service
3. Click "Logs" tab
4. Monitor requests and errors

### Update Server

```bash
# Make changes to server code
git add server/
git commit -m "Update server"
git push

# Render auto-deploys on push
```

### Rotate API Key

1. Generate new API key
2. Update in Render environment variables
3. Update in Claude.ai connector settings
4. Old key stops working immediately

---

## Troubleshooting

### Health Check Fails

```bash
# Check service status in Render dashboard
# View logs for error messages
# Verify environment variables are set

# Test locally first:
cd server
python main.py
curl http://localhost:8000/health
```

### Authentication Errors

```bash
# Test with correct header
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://your-service.onrender.com/list_tools

# Verify API key matches between Render and Claude.ai
```

### Readwise API Errors

```bash
# Verify token
curl -H "Authorization: Token YOUR_READWISE_TOKEN" \
     https://readwise.io/api/v3/list

# Check token at: https://readwise.io/access_token
```

### Cold Starts (Free Tier)

Free tier spins down after 15 minutes of inactivity.
First request after spin-down takes ~10 seconds.

**Solutions:**
1. Upgrade to paid tier ($7/month) for always-on
2. Use a cron job to ping health endpoint every 10 minutes
3. Accept cold starts (usually fine for personal use)

---

## Security Best Practices

1. **Never commit secrets**
   - Add `.env` to `.gitignore`
   - Use environment variables only

2. **Use strong API keys**
   - Minimum 32 characters
   - Random hex strings
   - Rotate periodically

3. **Monitor usage**
   - Check Render logs regularly
   - Set up alerts for errors
   - Track API rate limits

4. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade fastmcp httpx
   ```

---

## Cost Optimization

### Free Tier Limits

**Render Free:**
- 750 hours/month (31 days × 24 hours = 744 hours)
- Sufficient for 24/7 uptime
- 512 MB RAM
- Spins down after 15 min inactivity

**Readwise:**
- Uses existing subscription
- API rate limits: 20 req/min (GET), 50 req/min (POST)

### When to Upgrade

Upgrade to Render Starter ($7/month) if:
- You need instant response (no cold starts)
- High traffic (>10 requests/hour consistently)
- Multiple users sharing one server
- Professional/production use

---

## Support

- **Server Issues**: Check logs in Render dashboard
- **Readwise API**: https://readwise.io/help
- **Claude.ai Connectors**: https://support.claude.com
- **GitHub Issues**: https://github.com/your-repo/issues
