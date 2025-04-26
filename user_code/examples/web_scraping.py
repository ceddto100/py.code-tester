"""
Sample Web Scraping Script
-------------------------
This script demonstrates web scraping using requests and BeautifulSoup.
It retrieves and analyzes news headlines from a sample website.
"""
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
import numpy as np

# NLTK setup
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Configuration
url = "https://news.ycombinator.com/"  # Hacker News as an example
print(f"Scraping headlines from: {url}")

# Make HTTP request
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise exception for 4XX/5XX status codes
    
    print(f"Request successful! Status code: {response.status_code}")
    print(f"Content type: {response.headers.get('content-type')}")
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract headlines (specific to Hacker News structure)
    headlines = []
    for story in soup.select('.titleline > a'):
        headlines.append(story.text)
    
    # Display the number of headlines found
    print(f"\nFound {len(headlines)} headlines")
    
    # Print top 10 headlines
    print("\nTop 10 Headlines:")
    for i, headline in enumerate(headlines[:10], 1):
        print(f"{i}. {headline}")
    
    # Text analysis
    if headlines:
        # Combine headlines and convert to lowercase
        all_text = ' '.join(headlines).lower()
        
        # Remove non-alphanumeric characters
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', all_text)
        
        # Split into words
        words = clean_text.split()
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_counts = Counter(filtered_words)
        top_words = word_counts.most_common(15)
        
        print("\nMost common words in headlines:")
        for word, count in top_words:
            print(f"{word}: {count}")
        
        # Create a bar chart of top words
        words, counts = zip(*top_words) if top_words else ([], [])
        
        plt.figure(figsize=(12, 6))
        y_pos = np.arange(len(words))
        
        plt.barh(y_pos, counts, align='center')
        plt.yticks(y_pos, words)
        plt.xlabel('Frequency')
        plt.title('Most Common Words in Headlines')
        
        plt.tight_layout()
        plt.show()
        
        # Headline length analysis
        headline_lengths = [len(headline) for headline in headlines]
        avg_length = sum(headline_lengths) / len(headline_lengths)
        
        print(f"\nHeadline Length Analysis:")
        print(f"Average length: {avg_length:.1f} characters")
        print(f"Shortest: {min(headline_lengths)} characters")
        print(f"Longest: {max(headline_lengths)} characters")
        
        # Create a histogram of headline lengths
        plt.figure(figsize=(10, 6))
        plt.hist(headline_lengths, bins=20, alpha=0.7, color='green')
        plt.axvline(avg_length, color='red', linestyle='dashed', linewidth=1, label=f'Average ({avg_length:.1f})')
        plt.xlabel('Character Length')
        plt.ylabel('Frequency')
        plt.title('Distribution of Headline Lengths')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
except requests.exceptions.RequestException as e:
    print(f"Error during request: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

print("\nWeb scraping and analysis complete!") 