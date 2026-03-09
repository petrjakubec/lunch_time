# 🍽️ Lunch Time - Daily Lunch Specials Scraper

Automatically scrapes daily lunch specials from nearby restaurants and posts them to Slack. Runs completely free using GitHub Actions scheduling.

## Features

✅ **HTML Scraping** - Extracts daily specials from restaurant menu pages  
✅ **Slack Integration** - Posts beautifully formatted menu updates to your Slack workspace  
✅ **GitHub Actions** - Free scheduling, no external servers needed  
✅ **Customizable** - Easy to add multiple restaurants or change posting destination  

## Setup

### 1. Get Your Slack Webhook URL

1. Go to [Slack App Directory](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name it "Lunch Notifier" and select your workspace
4. Click "Incoming Webhooks" in the sidebar
5. Toggle "Activate Incoming Webhooks" to ON
6. Click "Add New Webhook to Workspace"
7. Select the channel where you want lunch specials posted
8. Copy the Webhook URL (looks like `https://hooks.slack.com/services/...`)

### 2. Configure GitHub Secrets

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add these secrets:

| Name | Value |
|------|-------|
| `SLACK_WEBHOOK_URL` | Your Slack webhook URL from step 1 |
| `RESTAURANTS_URL` | `https://padagali.choiceqr.com/section:denni-menu/utery` (or comma-separated URLs) |

**Example with multiple restaurants:**
```
https://restaurant1.com/menu,https://restaurant2.com/menu
```

### 3. Deploy

Just push this code to GitHub:
```bash
git add .
git commit -m "Initial lunch scraper setup"
git push
```

The GitHub Actions workflow will automatically run every weekday at 9 AM UTC.

## Manual Testing

To test immediately without waiting for the schedule:

1. Go to Actions tab in your GitHub repo
2. Click "Daily Lunch Specials Scraper" workflow
3. Click "Run workflow" → "Run workflow"

Check Slack after a few seconds to see the results.

## Customization

### Change the Schedule

Edit [/.github/workflows/lunch-scraper.yml](.github/workflows/lunch-scraper.yml):

```yaml
on:
  schedule:
    - cron: '0 9 * * 1-5'  # 9 AM, Monday-Friday
```

**Cron format:** `minute hour day month day-of-week`

Common examples:
- `'0 9 * * *'` - Daily at 9 AM
- `'0 9 * * 1-5'` - Weekdays only (default)
- `'0 11,14 * * 1-5'` - 11 AM and 2 PM on weekdays

Use [crontab.guru](https://crontab.guru) to generate expressions.

### Add More Restaurants

Add comma-separated URLs to the `RESTAURANTS_URL` secret:
```
https://restaurant1.com/menu,https://restaurant2.com/menu,https://restaurant3.com/menu
```

### Modify the Scraper

Edit [scraper.py](scraper.py) to:
- Change HTML parsing selectors for different website structures
- Add parsing for prices, descriptions, etc.
- Modify Slack message formatting

## Troubleshooting

### Workflow did not run
- Check that GitHub Actions is enabled (Settings → Actions → General)
- GitHub Actions cron uses UTC timezone

### Scraper fails
- Check the GitHub Actions logs (Actions tab → workflow run → logs)
- Verify `SLACK_WEBHOOK_URL` secret is set correctly
- Test the webhook URL with curl:
  ```bash
  curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"Test"}' \
    YOUR_WEBHOOK_URL
  ```

### Menu not parsing correctly
The scraper tries multiple HTML parsing strategies. If your restaurant uses a different structure:
1. Inspect the restaurant website (View Source)
2. Update the CSS selectors in `scraper.py`
3. Push changes and test with manual workflow trigger

## Examples

### Slack Output
```
🍽️ Lunch Specials
Monday, March 10, 2025

Padagali
• Chicken Schnitzel with Fries - $12.99
• Grilled Salmon - $14.99
• Vegetarian Buddha Bowl - $11.99
[View Menu](https://...)
```

## Tech Stack

- **Python 3.11** - Scraping logic
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **GitHub Actions** - Free scheduling
- **Slack API** - Webhook integration

## License

MIT - Free to use and modify

---

**Note:** This project runs completely free using GitHub's provided Actions minutes (2,000/month included for public repos).
