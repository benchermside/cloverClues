# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clover Clues is a web-based word puzzle game built with vanilla HTML, CSS, and JavaScript. The game involves dragging cards with words on their edges to arrange them on a game board to solve clues.

## Architecture

- **Static HTML files**: Each page (index.html, create.html, solve.html, tutorial.html) contains its own embedded JavaScript
- **Shared styling**: All pages use the same style.css file
- **No build process**: This is a pure client-side application with no compilation or bundling required
- **Drag and drop system**: Common JavaScript functionality across game pages for card manipulation

## File Structure

- `index.html` - Main menu with navigation to other pages
- `create.html` - Page for creating new clues/puzzles
- `solve.html` - Page for solving existing clues
- `tutorial.html` - Tutorial page explaining how to play
- `style.css` - Shared styles for all pages
- `cloverImage.jpg` - Background image used across all pages

## Key Components

### Game Cards
- Cards have words on four edges (top, right, bottom, left)
- Implemented as `.game-card` elements with positioned `.card-word` children
- Cards are draggable using HTML5 drag and drop API

### Game Board
- 2x2 grid of card slots (`.card-slot`) within `.board-grid`
- Card holders area below the board for available cards
- Drag and drop logic handles card placement and movement

### Common JavaScript Pattern
All game pages (create.html, solve.html, tutorial.html) share identical drag-and-drop functionality:
- `handleDragStart()` - Initiates card dragging
- `handleDragEnd()` - Cleans up after drag operation
- `handleDragOver()` - Prevents default to allow drop
- `handleDrop()` - Handles card placement logic

## Development Notes

- No package.json or build tools - this is a static HTML/CSS/JS project
- To run locally: Simply open any HTML file in a web browser
- All JavaScript is inline within `<script>` tags
- CSS uses flexbox and grid for layout
- Background image styling is applied to body element across all pages

## Testing

No automated testing framework is present. Testing should be done manually by:
1. Opening each HTML file in a browser
2. Testing drag and drop functionality
3. Verifying navigation between pages works correctly
4. Checking responsive behavior and styling