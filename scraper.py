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

def main():
    """
    Main function to orchestrate scraping and posting
    """
    # Get configuration from environment variables
    restaurants_url = os.getenv('RESTAURANTS_URL', 'https://padagali.choiceqr.com/section:denni-menu/utery')
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    
    if not slack_webhook:
        print("✗ Error: SLACK_WEBHOOK_URL environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scraping lunch specials from: {restaurants_url}")
    
    # Scrape restaurants
    specials = []
    if restaurants_url:
        urls = [url.strip() for url in restaurants_url.split(',')]
        for url in urls:
            if url:
                print(f"  Scraping: {url}")
                data = scrape_lunch_specials(url)
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
