# 🍽️ Lunch Time - Daily Lunch Specials Scraper

Automatically scrapes daily lunch specials from nearby restaurants and posts them to Slack. Results also display on a beautiful static HTML website via GitHub Pages. Runs completely free using GitHub Actions scheduling.

## Features

✅ **HTML Scraping** - Extracts daily specials from restaurant menu pages  
✅ **Slack Integration** - Posts beautifully formatted menu updates to your Slack workspace  
✅ **GitHub Pages Website** - View specials on a responsive HTML site  
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

### 2. Configure Restaurants

Edit [restaurants.json](restaurants.json) to add or modify restaurants:

```json
{
  "restaurants": [
    {
      "name": "Padagali",
      "url": "https://padagali.choiceqr.com/section:denni-menu/utery"
    },
    {
      "name": "Seminář",
      "url": "https://www.useminaru.cz/menu.php"
    },
    {
      "name": "Garden Food Concept",
      "url": "https://www.gardenfoodconcept.cz/poledni-menu/"
    }
  ]
}
```

### 3. Configure GitHub Secrets (for GitHub Actions)

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add:

| Name | Value |
|------|-------|
| `SLACK_WEBHOOK_URL` | Your Slack webhook URL from step 1 |
| `RESTAURANTS_URL` | *(Optional)* Comma-separated URLs if not using restaurants.json |

**Note:** If you commit `restaurants.json` to the repo, you don't need to set `RESTAURANTS_URL`. The scraper will automatically use `restaurants.json`. The `RESTAURANTS_URL` env var is only needed if you want to override it in GitHub Actions or run without a config file.

### 4. Enable GitHub Pages

1. Go to Settings → Pages
2. Under "Source", select "Deploy from a branch"
3. Select branch: `main`, folder: `/ (root)` → `docs`
4. Click "Save"

Your site will be live at: `https://YOUR_USERNAME.github.io/lunch_time`

### 5. Deploy

JusUsage

### View Lunch Specials

**On the Web:** 🌐 Visit `https://YOUR_USERNAME.github.io/lunch_time` after enabling Pages (updates twice daily)

**In Slack:** Receive Slack notifications at 9 AM and 10:45 AM UTC (weekdays)

**Manual Test:** Go to Actions → "Daily Lunch Specials Scraper" → "Run workflow"
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
    - cron: '0 9 * * 1-5'    # 9 AM, Monday-Friday
    - cron: '45 10 * * 1-5'  # 10:45 AM, Monday-Friday
```

**Cron format:** `minute hour day month day-of-week`

Common examples:
- `'0 9 * * *'` - Daily at 9 AM
- `'0 9 * * 1-5'` - 9 AM on weekdays
- `'45 10 * * 1-5'` - 10:45 AM on weekdays
- Multiple crons run the workflow multiple times per day

Use [crontab.guru](https://crontab.guru) to generate expressions.

### Add More Restaurants

Add comma-separated URLs to the `RESTAURANTS_URL` secret:
```
https://restaurant1.com/menu,https://restaurant2.com/menu,https://restaurant3.com/menu
```

### Modify Scraper Logic

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

### Website Output
Visit your GitHub Pages site to see a mobile-friendly lunch specials page with:
- Restaurant names and daily specials
- Links to full menus
- Beautiful gradient background
- Mobile-responsive design

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
