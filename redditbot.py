import praw
import pandas as pd
import time
from datetime import datetime

# Initialize Reddit API
reddit = praw.Reddit(
    client_id='LdpCyuLbaa6Dk81aU1O0sA',
    client_secret='fllacT4prjEHYjdy2RbOSaJLALvkww',
    user_agent='Windows:RedditScraper:1.0 (by /u/Evening_Front5923)'
)

def scrape_reddit(subreddit_name, query, max_posts=1000, time_filter="all", start_date=None, end_date=None, max_comments=50):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    try:
        # Fetch posts using search
        for post in subreddit.search(query, sort="top", time_filter=time_filter, limit=max_posts):
            # Filter by custom date range if provided
            post_date = datetime.utcfromtimestamp(post.created_utc)
            if start_date and end_date and not (start_date <= post_date <= end_date):
                continue  # Skip posts outside the date range
            
            # Collect post data
            post_data = {
                "Title": post.title,  # Title of the post
                "Author": post.author.name if post.author else None,  # Author's username
                "Upvotes": post.score,  # Upvotes for the post
                "Comments": post.num_comments,  # Number of comments
                "URL": post.url,  # Link to the post
                "Created_UTC": post.created_utc,  # Timestamp of post creation
                "Created_Date": post_date.strftime('%Y-%m-%d %H:%M:%S')  # Date of post creation
            }

            # Collect comments for the post (limit number of comments to `max_comments`)
            post.comments.replace_more(limit=0)  # This removes the "MoreComments" object
            for comment in post.comments[:max_comments]:  # Limit the number of comments
                comments_data = {
                    "Post_Title": post.title,
                    "Comment_Author": comment.author.name if comment.author else None,
                    "Comment_Text": comment.body,
                    "Comment_Upvotes": comment.score,
                    "Created_UTC": comment.created_utc,
                    "Comment_Created_Date": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                }
                posts.append(comments_data)

            # Add the post data itself
            posts.append(post_data)
        
        time.sleep(1)  # Avoid rate limiting
    except Exception as e:
        print(f"Error: {e}")

    return pd.DataFrame(posts)

# Example usage
subreddits = ['worldnews', 'MiddleEastNews', 'IsraelPalestine']
query = "Israel Gaza"
time_filter = "all"  # Limit the timeframe to all posts
max_posts = 500  # Increase max posts per subreddit

# Specify custom date range (start and end dates in 'YYYY-MM-DD' format)
start_date = datetime(2023, 10, 7)  # Example: Start date of January 1, 2023
end_date = datetime(2024, 11, 30)  # Example: End date of December 31, 2024

dataset = pd.concat([scrape_reddit(sub, query, max_posts=max_posts, time_filter=time_filter, start_date=start_date, end_date=end_date) 
                     for sub in subreddits], ignore_index=True)

# Remove columns with single-word values
columns_to_remove = ['Author']  # Explicitly specify columns to remove
dataset = dataset.drop(columns=columns_to_remove)

# Save the dataset to a CSV file
dataset.to_csv('Israel_Gaza_War_Reddit_Data_Optimized_with_Comments.csv', index=False)
print(f"Dataset saved as 'Israel_Gaza_War_Reddit_Data_Optimized_with_Comments.csv' with {len(dataset)} posts and comments")

# Display first few rows of the dataset (for verification)
print(dataset.head())
