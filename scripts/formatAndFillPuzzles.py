#!/usr/bin/env python3
"""
Convert puzzle format from test_puzzles.txt to JSON format.

Usage: python formatAndFillPuzzles.py <input_file> <output_file>
"""

import sys
import json
import re


def parse_puzzles(input_file):
    """Parse puzzles from the input file format."""
    puzzles = []
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split by puzzle sections
    puzzle_sections = re.split(r'Puzzle \d+:', content)[1:]  # Skip empty first element
    
    for section in puzzle_sections:
        lines = section.strip().split('\n')
        if len(lines) < 4:
            continue
            
        puzzle_data = {
            "cards": [],
            "clues": [],
            "solution": []
        }
        
        # Parse the 4 pairs
        for i in range(4):
            if i < len(lines):
                # Match pattern: "Pair X: word1, word2: clue"
                match = re.match(r'\s*Pair \d+:\s*(.+?),\s*(.+?):\s*(.+)', lines[i])
                if match:
                    word1 = match.group(1).strip()
                    word2 = match.group(2).strip()
                    clue = match.group(3).strip()
                    
                    # Add card with id i+1
                    card = {
                        "id": i + 1,
                        "words": [word1, word2, "null", "null"]
                    }
                    puzzle_data["cards"].append(card)
                    
                    # Add clue
                    puzzle_data["clues"].append(clue)
                    
                    # Add solution entry
                    puzzle_data["solution"].append({
                        "id": i + 1,
                        "orient": 0
                    })
        
        # Add 5th card with all null words
        puzzle_data["cards"].append({
            "id": 5,
            "words": ["null", "null", "null", "null"]
        })
        
        if len(puzzle_data["cards"]) == 5 and len(puzzle_data["clues"]) == 4:
            puzzles.append(puzzle_data)
    
    return puzzles


def main():
    if len(sys.argv) != 3:
        print("Usage: python formatAndFillPuzzles.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        puzzles = parse_puzzles(input_file)
        
        # Write to output file
        with open(output_file, 'w') as f:
            json.dump(puzzles, f, indent=2)
        
        print(f"Successfully converted {len(puzzles)} puzzles from {input_file} to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()