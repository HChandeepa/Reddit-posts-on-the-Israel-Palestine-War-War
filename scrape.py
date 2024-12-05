from playwright.sync_api import sync_playwright
import os
from datetime import datetime
import csv

def scrape_tweets(search_url: str, headless: bool = True, max_tweets: int = 100) -> list:
    """
    Scrape tweets from a search URL.
    """
    tweets = []

    with sync_playwright() as pw:
        # Launch the browser
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Go to the search page
            page.goto(search_url, timeout=60000)
            page.wait_for_selector("article", timeout=60000)

            # Scroll and scrape tweets
            last_tweet_count = 0
            while len(tweets) < max_tweets:
                # Get all visible tweets
                tweet_elements = page.query_selector_all('article')

                for tweet in tweet_elements:
                    try:
                        # Extract tweet details
                        text = tweet.query_selector('[data-testid="tweetText"]').inner_text()
                        author = tweet.query_selector('div.r-1f6r7vd span').inner_text()
                        timestamp = tweet.query_selector('time').get_attribute('datetime')

                        tweets.append({
                            "author": author,
                            "text": text,
                            "timestamp": timestamp
                        })

                        # Stop if the desired number of tweets is reached
                        if len(tweets) >= max_tweets:
                            break
                    except Exception as e:
                        print(f"Error extracting tweet: {e}")
                        continue

                # Scroll down to load more tweets
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                page.wait_for_timeout(3000)

                # Check if new tweets were added
                if len(tweets) == last_tweet_count:
                    print("No more tweets found. Stopping.")
                    break
                last_tweet_count = len(tweets)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

    return tweets

def save_to_csv(data: list, filename: str = "results.csv"):
    """
    Save the scraped data to a CSV file.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        # Open the file and write the data
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["author", "text", "timestamp"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header row
            writer.writerows(data)  # Write the rows

        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    # URL for the search query on Twitter
    search_url = "https://x.com/search?q=israel%20gaza%20conflict&src=typed_query"

    # Step 1: Scrape tweets
    try:
        tweets = scrape_tweets(search_url, headless=True, max_tweets=50)
        print(f"Scraped {len(tweets)} tweets.")
    except Exception as e:
        print(f"Failed to scrape tweets: {e}")
        exit(1)

    # Step 2: Save the tweets to a CSV file
    save_to_csv(tweets, "results/israel_gaza_tweets.csv")
