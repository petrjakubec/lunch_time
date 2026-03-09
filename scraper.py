#!/usr/bin/env python3
"""
Lunch Specials Scraper
Scrapes daily lunch specials from restaurants and posts to Slack
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import json

def scrape_lunch_specials(url):
    """
    Scrapes lunch specials from the provided URL
    Returns a dict with restaurant data and special items
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract title/restaurant name
        title = soup.find('h1')
        restaurant_name = title.get_text(strip=True) if title else "Padagali"
        
        # Extract menu items
        items = []
        menu_section = soup.find('div', class_='menu-section')
        
        if menu_section:
            # Look for menu items in various common structures
            item_elements = menu_section.find_all(['div', 'li'], class_=['menu-item', 'item', 'dish'])
            
            if not item_elements:
                # Fallback: get all text content from menu section
                item_text = menu_section.get_text(strip=True)
                items = [item.strip() for item in item_text.split('\n') if item.strip()][:5]
            else:
                for elem in item_elements[:5]:  # Limit to 5 items
                    item_name = elem.find(['span', 'p', 'div'], class_=['name', 'title'])
                    price = elem.find(['span', 'p'], class_=['price', 'cost'])
                    
                    name_text = item_name.get_text(strip=True) if item_name else elem.get_text(strip=True)
                    price_text = price.get_text(strip=True) if price else ""
                    
                    item_str = f"{name_text} {price_text}".strip()
                    if item_str and len(item_str) > 3:
                        items.append(item_str)
        
        if not items:
            # Fallback: extract all text and parse
            text_content = soup.get_text()
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            items = lines[:5]
        
        return {
            'name': restaurant_name,
            'url': url,
            'items': items if items else ['Menu information available on restaurant website'],
            'scraped_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}", file=sys.stderr)
        return {
            'name': 'Unknown Restaurant',
            'url': url,
            'items': [f'Error scraping menu: {str(e)}'],
            'error': True
        }

def generate_html(specials_data):
    """
    Generates a static HTML file with lunch specials
    """
    try:
        today = datetime.now()
        date_str = today.strftime('%A, %B %d, %Y')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Today's Lunch Specials 🍽️</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding-top: 20px;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header .date {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .restaurant-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .restaurant-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .restaurant-name {{
            font-size: 1.5em;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .menu-items {{
            list-style: none;
        }}
        
        .menu-items li {{
            padding: 10px 0;
            color: #555;
            border-bottom: 1px solid #eee;
        }}
        
        .menu-items li:last-child {{
      Generate HTML
    generate_html(specials)
    
    #       border-bottom: none;
        }}
        
        .menu-items li:before {{
            content: "🍴 ";
            margin-right: 8px;
        }}
        
        .view-menu {{
            display: inline-block;
            margin-top: 12px;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9em;
            transition: background 0.3s;
        }}
        
        .view-menu:hover {{
            background: #764ba2;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
            font-size: 0.9em;
        }}
        
        .error {{
            background: #ffe0e0;
            color: #c00;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        @media (max-width: 600px) {{
            header h1 {{ font-size: 1.8em; }}
            .restaurant-name {{ font-size: 1.2em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍽️ Lunch Specials</h1>
            <div class="date">{date_str}</div>
        </header>
        
        <main>
"""
        
        # Add restaurant cards
        for special in specials_data:
            if special.get('error'):
                html_content += f"""            <div class="error">
                <strong>⚠️ {special['name']}</strong><br>
                {special['items'][0]}
            </div>
"""
            else:
                items_html = "\n".join([f"                <li>{item}</li>" for item in special['items']])
                html_content += f"""            <div class="restaurant-card">
                <div class="restaurant-name">{special['name']}</div>
                <ul class="menu-items">
{items_html}
                </ul>
                <a href="{special['url']}" target="_blank" class="view-menu">View Full Menu →</a>
            </div>
"""
        
        html_content += """        </main>
        
        <footer>
            <p>Last updated: {time}</p>
            <p><a href="https://github.com" style="color: white; opacity: 0.8;">Updates daily at 9 AM UTC</a></p>
        </footer>
    </div>
</body>
</html>
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
        
        # Write to docs folder (GitHub Pages)
        os.makedirs('docs', exist_ok=True)
        output_path = 'docs/index.html'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error generating HTML: {str(e)}", file=sys.stderr)
        return False

def post_to_slack(webhook_url, specials_data):
    """
    Posts lunch specials to Slack via webhook
    Returns True if successful, False otherwise
    """
    try:
        # Build Slack message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🍽️ Lunch Specials"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_{datetime.now().strftime('%A, %B %d, %Y')}_"
                }
            }
        ]
        
        # Add each restaurant's specials
        for special in specials_data:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{special['name']}*\n" + 
                            "\n".join([f"• {item}" for item in special['items']]) +
                            f"\n<{special['url']}|View Menu>"
                }
            })
        
        blocks.append({
            "type": "divider"
        })
        
        payload = {
            "blocks": blocks
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        
        print(f"✓ Successfully posted to Slack")
        return True
        
    except Exception as e:
        print(f"✗ Error posting to Slack: {str(e)}", file=sys.stderr)
        return False

def load_restaurants():
    """
    Load restaurants from config file or environment variable
    """
    # First, check if restaurants.json exists
    if os.path.exists('restaurants.json'):
        try:
            with open('restaurants.json', 'r') as f:
                config = json.load(f)
                return [(r['name'], r['url']) for r in config.get('restaurants', [])]
        except Exception as e:
            print(f"Warning: Could not load restaurants.json: {e}", file=sys.stderr)
    
    # Fallback to environment variable (for GitHub Actions)
    restaurants_url = os.getenv('RESTAURANTS_URL', '')
    if restaurants_url:
        urls = [url.strip() for url in restaurants_url.split(',')]
        # Parse URL only, no names from env var
        return [(f"Restaurant {i+1}", url) for i, url in enumerate(urls) if url]
    
    return []

def main():
    """
    Main function to orchestrate scraping and posting
    """
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    
    if not slack_webhook:
        print("✗ Error: SLACK_WEBHOOK_URL environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Load restaurants from config or env
    restaurants = load_restaurants()
    
    if not restaurants:
        print("✗ Error: No restaurants configured. Add restaurants to restaurants.json or RESTAURANTS_URL env var", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scraping {len(restaurants)} restaurant(s)...")
    
    # Scrape restaurants
    specials = []
    for name, url in restaurants:
        print(f"  Scraping: {name}")
        data = scrape_lunch_specials(url)
        # Override auto-detected name with config name
        data['name'] = name
        specials.append(data)
    
    if not specials:
        print("✗ No restaurants to scrape", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Scraped {len(specials)} restaurant(s)")
    
    # Post to Slack
    success = post_to_slack(slack_webhook, specials)
    
    if not success:
        sys.exit(1)
    
    print("✓ Lunch specials posted successfully!")

if __name__ == '__main__':
    main()
