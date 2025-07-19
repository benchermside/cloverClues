#!/usr/bin/env python3
"""
Shared library for random word selection functionality.
"""

import random
import os

def load_wordlist():
    """Load the wordlist from the data directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_file = os.path.join(os.path.dirname(script_dir), 'data', 'wordlist.txt')
    
    try:
        with open(wordlist_file, 'r') as f:
            all_words = [line.strip() for line in f if line.strip()]
        return all_words
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find wordlist file at {wordlist_file}")
    except Exception as e:
        raise Exception(f"Error reading wordlist file: {e}")

def selectRandomWord(all_words, used_words=None):
    """
    Select a random word from all_words that meets criteria and hasn't been used.
    
    Args:
        all_words: List of all available words
        used_words: Set of words already used (optional)
    
    Returns:
        A capitalized word that is at least 3 chars long and alphabetic
    """
    if used_words is None:
        used_words = set()
    
    while True:
        word = random.choice(all_words)
        
        if word in used_words:
            continue
            
        if len(word) < 3:
            continue
            
        if not word.isalpha():
            continue
            
        return word.capitalize()

def get_random_word():
    """
    Convenience function to get a single random word without tracking used words.
    Loads the wordlist if needed.
    """
    if not hasattr(get_random_word, '_wordlist'):
        get_random_word._wordlist = load_wordlist()
    
    return selectRandomWord(get_random_word._wordlist)