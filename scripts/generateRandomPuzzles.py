#!/usr/bin/env python3

import sys
import random
import os

NUMBER_OF_PUZZLES = 50

def selectRandomWord(all_words, used_words):
    while True:
        word = random.choice(all_words)
        
        if word in used_words:
            continue
            
        if len(word) < 3:
            continue
            
        if not word.isalpha():
            continue
            
        return word.capitalize()

def main():
    if len(sys.argv) != 2:
        print("Usage: python generateRandomPuzzles.py <output_file>")
        sys.exit(1)
    
    output_file = sys.argv[1]
    wordlist_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'wordlist.txt')
    
    try:
        with open(wordlist_file, 'r') as f:
            all_words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find wordlist file at {wordlist_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading wordlist file: {e}")
        sys.exit(1)
    
    words_needed = NUMBER_OF_PUZZLES * 8
    if len(all_words) < words_needed:
        print(f"Error: Not enough words in wordlist. Found {len(all_words)}, need at least {words_needed}")
        sys.exit(1)
    
    selected_words = []
    used_words = set()
    
    for _ in range(words_needed):
        word = selectRandomWord(all_words, used_words)
        selected_words.append(word)
        used_words.add(word.lower())
    
    puzzles = []
    for i in range(0, words_needed, 8):
        puzzle_words = selected_words[i:i+8]
        puzzle_pairs = []
        for j in range(0, 8, 2):
            puzzle_pairs.append((puzzle_words[j], puzzle_words[j+1]))
        puzzles.append(puzzle_pairs)
    
    try:
        with open(output_file, 'w') as f:
            for puzzle_num, puzzle in enumerate(puzzles, 1):
                f.write(f"Puzzle {puzzle_num}:\n")
                for pair_num, (word1, word2) in enumerate(puzzle, 1):
                    f.write(f"  Pair {pair_num}: {word1}, {word2}\n")
                f.write("\n")
        
        print(f"Successfully generated {NUMBER_OF_PUZZLES} puzzles and saved to {output_file}")
    
    except Exception as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()