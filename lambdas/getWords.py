#!/usr/bin/env python3

import json
import random

def get_random_words(filename='data/wordlist.txt', count=20):
    """
    Read words from a file and return a random selection as JSON.
    
    Args:
        filename: Path to the wordlist file (default: 'wordlist.txt')
        count: Number of random words to select (default: 20)
    
    Returns:
        JSON string containing list of random words
    """
    try:
        with open(filename, 'r') as f:
            # Read all lines and strip whitespace
            words = [line.strip() for line in f if line.strip()]
        
        # Select random words (without replacement)
        selected_words = random.sample(words, min(count, len(words)))
        
        # Return as JSON
        return json.dumps(selected_words)
    
    except FileNotFoundError:
        return json.dumps({"error": f"File '{filename}' not found"})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print(get_random_words())