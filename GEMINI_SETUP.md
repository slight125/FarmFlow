# 🤖 Gemini AI Integration Guide for FarmFlow

## Overview
FarmFlow now uses **Google Gemini Pro** to provide intelligent, context-aware responses based on your actual farm data!

## Quick Setup (5 minutes)

### Step 1: Get Your Free Gemini API Key

1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated API key

### Step 2: Configure FarmFlow

1. Create a `.env` file in your FarmFlow root directory:
   ```bash
   # In PowerShell
   cd "c:\Users\hp\Downloads\farmflow-suite-main(1)\farmflow-suite-main"
   Copy-Item .env.example .env
   ```

2. Open `.env` file and add your API key:
   ```
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   ```

3. Save the file

### Step 3: Restart the Server

```bash
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

That's it! 🎉

## How It Works

### Gemini-Powered Features

1. **Context-Aware Responses**
   - Analyzes your actual crop data
   - Considers your livestock status
   - Reviews your financial performance
   - Checks pending tasks and inventory

2. **Smart Recommendations**
   - Personalized farming advice
   - Weather-based suggestions
   - Crop-specific guidance
   - Livestock care plans
   - Financial optimization tips

3. **Natural Conversations**
   - Ask questions in plain English
   - Get detailed, expert-level answers
   - Receive follow-up suggestions
   - Learn best practices

### Example Conversations

**Question:** "How are my crops doing?"

**Gemini Response:** 
"Based on your current farm data, you have 3 active crops being monitored. Your Tomato crop (planted 45 days ago) is in the growing stage and appears healthy - it's about 15 days from optimal harvest time. The Wheat field covering 5 acres is progressing well towards its expected harvest in 30 days.

I recommend:
1. Begin preparing harvest equipment for the tomatoes
2. Monitor for early blight signs as we're in the critical growth phase
3. Consider a final fertilization for the wheat crop

Would you like specific advice on harvest timing, pest management, or yield optimization?"

---

**Question:** "What should I focus on today?"

**Gemini Response:**
"Looking at your priorities, here's what needs attention today:

HIGH PRIORITY:
• Cattle vaccination overdue (3 animals) - Schedule vet visit immediately
• Wheat harvest due in 7 days - Check equipment and arrange labor

MEDIUM PRIORITY:
• Low inventory: Fertilizer stock below reorder level
• Financial review: Monthly expenses tracking $2,500 vs $3,000 budget

Your net income this month is positive ($1,200), which is excellent! The main concern is the overdue livestock vaccinations - this should be your top priority today.

Need help scheduling the vet visit or planning the wheat harvest?"

---

## Benefits Over Basic AI

### Before (Basic AI):
- Generic responses
- No context from your farm
- Limited advice
- Pre-programmed answers

### After (Gemini AI):
- ✅ Uses YOUR actual farm data
- ✅ Considers current conditions
- ✅ Provides specific numbers and dates
- ✅ Adapts to your situation
- ✅ Expert-level agricultural knowledge
- ✅ Natural conversation flow

## API Key Security

**Important Security Notes:**

✅ **DO:**
- Keep your API key in the `.env` file
- Add `.env` to `.gitignore`
- Never share your API key publicly
- Regenerate key if exposed

❌ **DON'T:**
- Commit `.env` to Git
- Share screenshots with API keys
- Use API keys in frontend code
- Store keys in database

## Troubleshooting

### "API key not configured" Error

**Solution:**
1. Check `.env` file exists in root directory
2. Verify `GEMINI_API_KEY=` line is present
3. Ensure no spaces around the `=` sign
4. Restart Django server after adding key

### "API quota exceeded" Error

**Solutions:**
- Free tier: 60 requests/minute
- Wait a minute and try again
- Upgrade to paid tier if needed
- Check: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com

### Gemini Not Responding

**Fallback Behavior:**
- FarmFlow automatically falls back to basic AI
- You'll still get responses (just less intelligent)
- Fix the API key issue and restart

## Advanced Configuration

### Custom Model Settings

Edit `farm/gemini_chatbot.py` to customize:

```python
# Use different Gemini model
self.model = genai.GenerativeModel('gemini-pro')

# Configure generation parameters
generation_config = {
    'temperature': 0.7,  # 0.0-1.0 (higher = more creative)
    'top_p': 0.8,
    'top_k': 40,
    'max_output_tokens': 1024,
}
self.model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config
)
```

### Rate Limiting

Free tier limits:
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**

For production/heavy use, consider:
- Implementing caching
- Response throttling
- Paid tier upgrade

## API Key Management

### Get Free API Key:
1. Visit: https://makersuite.google.com/app/apikey
2. Google Account required
3. Free tier generous for personal use

### Monitor Usage:
- Dashboard: https://console.cloud.google.com
- Check quota and billing
- View API call metrics

### Paid Tier (Optional):
- Higher rate limits
- More requests
- Priority support
- Visit: https://cloud.google.com/vertex-ai/pricing

## Testing Your Setup

### Quick Test in AI Chat:

1. Login to FarmFlow
2. Click the floating AI button (🤖)
3. Ask: "Tell me about my farm"
4. You should get detailed response with your actual data

### Verification Checklist:

✅ Gemini package installed (`google-generativeai`)
✅ `.env` file created with API key
✅ Server restarted after configuration
✅ No error messages in chat
✅ Responses include your farm data
✅ Follow-up suggestions appear

## Support

### Get Help:
- **Email:** allanmurage125@gmail.com
- **Developer:** Allan Murage (https://allanmurage.tech)
- **Gemini Docs:** https://ai.google.dev/docs

### Useful Links:
- 🔑 Get API Key: https://makersuite.google.com/app/apikey
- 📚 Gemini Docs: https://ai.google.dev/tutorials/python_quickstart
- 💬 Community: https://stackoverflow.com/questions/tagged/google-gemini

---

**Developed with ❤️ by Allan Murage**

**FarmFlow v2.1 - Now with Gemini AI Power!** 🚀
