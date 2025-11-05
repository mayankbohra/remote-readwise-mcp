# Testing Checklist

Use this checklist before deploying to production.

## Local Testing

### Setup
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid tokens
- [ ] `READWISE_TOKEN` set correctly
- [ ] `MCP_API_KEY` generated (32+ chars)

### Server Startup
- [ ] Server starts without errors (`python main.py`)
- [ ] Listens on correct port (8000)
- [ ] Logs show "Authentication: Enabled"
- [ ] No Python import errors

### Health Check
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] Returns JSON with "status": "healthy"
- [ ] Shows correct authentication status
- [ ] Response time < 100ms

### Authentication
- [ ] Request without auth returns 401
  ```bash
  curl http://localhost:8000/list_tools
  # Should return 401
  ```
- [ ] Request with wrong key returns 401
  ```bash
  curl -H "Authorization: Bearer wrong_key" http://localhost:8000/list_tools
  # Should return 401
  ```
- [ ] Request with correct key succeeds
  ```bash
  curl -H "Authorization: Bearer $MCP_API_KEY" http://localhost:8000/list_tools
  # Should list 13 tools
  ```

### Tool Testing
Test each tool category:

#### Reader Tools
- [ ] `readwise_list_documents` - Returns documents
- [ ] `readwise_list_tags` - Returns tags list
- [ ] `readwise_topic_search` - Search works
- [ ] `readwise_save_document` - Can save URL
- [ ] `readwise_update_document` - Updates metadata
- [ ] `readwise_delete_document` - Removes document

#### Highlights Tools
- [ ] `readwise_list_highlights` - Returns highlights
- [ ] `readwise_get_daily_review` - Gets review
- [ ] `readwise_search_highlights` - Search works
- [ ] `readwise_list_books` - Returns books
- [ ] `readwise_get_book_highlights` - Gets book highlights
- [ ] `readwise_export_highlights` - Exports data
- [ ] `readwise_create_highlight` - Creates highlight

### Error Handling
- [ ] Invalid Readwise token shows clear error
- [ ] Network errors handled gracefully
- [ ] Rate limits respected (429 responses)
- [ ] Malformed requests return helpful errors

### Performance
- [ ] Response time < 500ms for most requests
- [ ] Memory usage stable over 10 requests
- [ ] No memory leaks after repeated calls
- [ ] Handles concurrent requests

## Docker Testing

### Build
- [ ] Dockerfile builds successfully
  ```bash
  docker build -t readwise-mcp ./server
  ```
- [ ] Build completes without errors
- [ ] Image size reasonable (< 500MB)
- [ ] All dependencies installed

### Run
- [ ] Container starts with env vars
  ```bash
  docker run -p 8000:8000 \
    -e READWISE_TOKEN=your_token \
    -e MCP_API_KEY=your_key \
    readwise-mcp
  ```
- [ ] Health check accessible
- [ ] Authentication works
- [ ] Tools functional

### Container Health
- [ ] Container stays running
- [ ] No crash loops
- [ ] Logs appear correctly
- [ ] Graceful shutdown on SIGTERM

## Render Deployment Testing

### Pre-Deployment
- [ ] `render.yaml` syntax valid
- [ ] Dockerfile in correct location
- [ ] `.dockerignore` excludes unnecessary files
- [ ] Git repository pushed to GitHub

### Deployment
- [ ] Render build succeeds
- [ ] Environment variables set
- [ ] Service starts successfully
- [ ] Health check passes in Render dashboard

### Post-Deployment
- [ ] Public URL accessible
- [ ] HTTPS working
- [ ] Health endpoint returns 200
  ```bash
  curl https://your-service.onrender.com/health
  ```
- [ ] Authentication required for tools
- [ ] All 13 tools available

### Load Testing
- [ ] Handles 10 concurrent requests
- [ ] Response time < 1 second
- [ ] No 500 errors under load
- [ ] Cold start < 15 seconds (free tier)

## Claude.ai Integration Testing

### Connector Setup
- [ ] Can add custom connector
- [ ] Server URL accepted
- [ ] Bearer token authentication works
- [ ] Connection test passes
- [ ] Shows 13 available tools

### Tool Execution
Test in Claude.ai:

- [ ] "List my Readwise documents" works
- [ ] "Get my daily review" returns highlights
- [ ] "Search highlights for X" finds results
- [ ] "Save this article: URL" saves to Readwise
- [ ] "List all my tags" returns tags

### Error Scenarios
- [ ] Invalid queries handled gracefully
- [ ] Network timeouts show user-friendly errors
- [ ] Rate limit errors explained clearly
- [ ] Server downtime detected

## Security Testing

### Authentication
- [ ] Cannot access without API key
- [ ] Expired/invalid keys rejected
- [ ] CORS headers set correctly
- [ ] No token exposure in responses

### Environment Security
- [ ] `.env` not committed to Git
- [ ] Secrets not in logs
- [ ] Health check doesn't expose secrets
- [ ] Error messages don't leak sensitive data

### HTTPS
- [ ] All requests use HTTPS
- [ ] No mixed content warnings
- [ ] Valid SSL certificate
- [ ] Secure headers present

## Documentation Testing

### Accuracy
- [ ] README instructions work
- [ ] QUICK_START_REMOTE.md deployable
- [ ] Code examples run without modification
- [ ] URLs and links valid

### Completeness
- [ ] All tools documented
- [ ] Environment variables explained
- [ ] Troubleshooting covers common issues
- [ ] Examples for each tool provided

## Production Readiness

### Monitoring
- [ ] Logs accessible in Render dashboard
- [ ] Health check configured
- [ ] Uptime monitoring setup (optional)
- [ ] Error tracking configured (optional)

### Maintenance
- [ ] Backup strategy documented
- [ ] Update procedure clear
- [ ] Rollback plan exists
- [ ] API key rotation process defined

### Performance
- [ ] Meets SLA requirements
- [ ] Handles expected load
- [ ] Scales appropriately
- [ ] Cold starts acceptable

### Cost
- [ ] Free tier limits understood
- [ ] Upgrade path clear
- [ ] Usage monitoring configured
- [ ] Budget alerts set (optional)

## Sign-Off

**Tested by:** _________________
**Date:** _________________
**Environment:** _________________
**Status:** ⬜ Pass  ⬜ Fail

**Notes:**
```
[Add any testing notes, issues found, or recommendations]
```

---

## Automated Test Script

Use the provided test script for quick validation:

```bash
# Local testing
./server/test_server.sh http://localhost:8000 YOUR_API_KEY

# Remote testing
./server/test_server.sh https://your-service.onrender.com YOUR_API_KEY
```

Expected output:
- ✅ All tests pass
- 13 tools listed
- Authentication working
- No errors

---

## Common Issues & Solutions

### "Connection refused"
- Check server is running
- Verify correct port
- Check firewall rules

### "401 Unauthorized"
- Verify API key correct
- Check Bearer token format
- Ensure no extra spaces

### "Readwise API error"
- Validate Readwise token
- Check API rate limits
- Verify token hasn't expired

### "Cold start timeout"
- Normal on free tier
- Wait 10-15 seconds
- Consider upgrading plan

---

**Remember:** Test thoroughly in local/staging before production deployment!
