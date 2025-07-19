#!/usr/bin/env python3

import sys
from word_selector import load_wordlist, selectRandomWord

NUMBER_OF_PUZZLES = 50

def main():
    if len(sys.argv) != 2:
        print("Usage: python generateRandomPuzzles.py <output_file>")
        sys.exit(1)
    
    output_file = sys.argv[1]
    
    try:
        all_words = load_wordlist()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
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