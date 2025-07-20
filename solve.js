let draggedCard = null;
let draggedCardOriginalParent = null;
let draggedCardOriginalNextSibling = null;

// Track rotation state for each card (0, 1, 2, 3 representing 0°, 90°, 180°, 270°)
const cardRotations = new Map();
// Track card IDs
const cardIds = new Map();
// Store puzzle solution for checking
let puzzleSolution = null;

// Add drag event listeners to all cards
document.querySelectorAll('.game-card').forEach(card => {
    card.addEventListener('dragstart', handleDragStart);
    card.addEventListener('dragend', handleDragEnd);
    // Initialize rotation state
    cardRotations.set(card, 0);
});

// Add drop event listeners to all card slots
document.querySelectorAll('.card-slot').forEach(slot => {
    slot.addEventListener('dragover', handleDragOver);
    slot.addEventListener('drop', handleDrop);
});

// Add click event listeners to all rotate buttons
document.querySelectorAll('.rotate-btn').forEach(btn => {
    btn.addEventListener('click', handleRotate);
});

function handleDragStart(e) {
    draggedCard = e.target;

    // any animations on a card should be canceled if we start to drag it
    draggedCard.classList.remove("rotate-animation");

    draggedCardOriginalParent = e.target.parentNode;
    draggedCardOriginalNextSibling = e.target.nextSibling;
    
    e.target.style.opacity = '0.5';
    e.dataTransfer.effectAllowed = 'move';
}

function handleDragEnd(e) {
    e.target.style.opacity = '1';
    draggedCard = null;
    draggedCardOriginalParent = null;
    draggedCardOriginalNextSibling = null;
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
}

function handleDrop(e) {
    e.preventDefault();
    
    if (!draggedCard) return;

    const dropTarget = e.target.closest('.card-slot');
    
    if (dropTarget && dropTarget.children.length === 0) {
        // Remove occupied class from previous slot
        document.querySelectorAll('.card-slot.occupied').forEach(slot => {
            if (slot.children.length === 0) {
                slot.classList.remove('occupied');
            }
        });
        
        // Add card to new slot
        dropTarget.appendChild(draggedCard);
        
        // Add occupied class only to board slots, not card holders
        if (!dropTarget.classList.contains('card-holder')) {
            dropTarget.classList.add('occupied');
        }
    }
}

function handleRotate(e) {
    e.stopPropagation(); // Prevent triggering drag
    const gameCard = e.target.closest('.game-card');
    if (!gameCard) return;

    // Get current rotation
    let currentRotation = cardRotations.get(gameCard) || 0;
    
    // Rotate counterclockwise (increment rotation count)
    currentRotation = (currentRotation + 1) % 4;
    cardRotations.set(gameCard, currentRotation);
    
    // Get the word elements
    const words = gameCard.querySelectorAll('.card-word');
    const wordTexts = Array.from(words).map(word => word.textContent);
    
    // Rotate words counterclockwise: top -> left, right -> top, bottom -> right, left -> bottom
    words[0].textContent = wordTexts[1]; // top gets right's text
    words[1].textContent = wordTexts[2]; // right gets bottom's text
    words[2].textContent = wordTexts[3]; // bottom gets left's text
    words[3].textContent = wordTexts[0]; // left gets top's text

    gameCard.classList.add("rotate-animation");

    // Remove the animation class after it finishes animating
    setTimeout(() => {
        gameCard.classList.remove("rotate-animation");
    }, 500);
}

// TODO: Remove this
async function loadPuzzleFromFile(filename) {
    try {
        const response = await fetch(filename);
        const puzzles = await response.json();
        return puzzles[0];
    } catch (error) {
        console.error('Error loading puzzles.json:', error);
    }
}

/*
 * This loads a puzzle from the server. It is passed the puzzleId (a number)
 * and returns the JSON format of the puzzle.
 */
async function loadPuzzle(puzzleId) {
    try {
        const url = `https://a47pu3b6jocvs6pjo7nmv6fl7a0vldrv.lambda-url.us-east-1.on.aws/?puzzleId=${puzzleId}`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const puzzle = await response.json();
        return puzzle;
    } catch (error) {
        console.error('Error loading puzzle from API:', error);
        throw error;
    }
}

/*
 * This function accepts a puzzle (in JSON format). It returns a new
 * puzzle object with the order of the cards and the orientation of each
 * randomized. The original puzzle is not modified.
 */
function shuffleCards(puzzle) {
    // Create a deep copy of the puzzle to avoid modifying the original
    const shuffledPuzzle = JSON.parse(JSON.stringify(puzzle));
    
    // Shuffle the cards array using Fisher-Yates algorithm
    if (shuffledPuzzle.cards && shuffledPuzzle.cards.length > 0) {
        const cards = shuffledPuzzle.cards;
        
        // Fisher-Yates shuffle
        for (let i = cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cards[i], cards[j]] = [cards[j], cards[i]];
        }

        // Randomly rotate each card (0, 1, 2, or 3 times)
        cards.forEach(card => {
            const rotations = Math.floor(Math.random() * 4);

            // Rotate the words array clockwise
            for (let r = 0; r < rotations; r++) {
                // Rotate clockwise: [top, left, bottom, right] -> [right, top, left, bottom]
                const temp = card.words[3];
                card.words[3] = card.words[2];
                card.words[2] = card.words[1];
                card.words[1] = card.words[0];
                card.words[0] = temp;
            }

            // Update the orient field in the solution for this card
            shuffledPuzzle.solution.forEach(solutionCard => {
                if (solutionCard.id === card.id) {
                    solutionCard.orient = (solutionCard.orient + 4 - rotations) % 4;
                }
            });
        });
    }
    
    return shuffledPuzzle;
}

/*
 * This loads a new puzzle, shuffles it, and populates the board with the
 * information from the puzzle.
 */
async function initSolve(){
    const originalPuzzle = await loadPuzzle(0);
    const puzzle = shuffleCards(originalPuzzle);

    // Get all game cards
    const gameCards = document.querySelectorAll('.game-card');
    
    // Populate each game card with words from the puzzle
    if (puzzle && puzzle.cards) {
        puzzle.cards.forEach((cardData, index) => {
            if (index < gameCards.length && cardData.words && cardData.words.length === 4) {
                const gameCard = gameCards[index];
                const cardWords = gameCard.querySelectorAll('.card-word');
                
                // Map words to card positions: top, right, bottom, left
                cardWords[0].textContent = cardData.words[0]; // top
                cardWords[1].textContent = cardData.words[3]; // right
                cardWords[2].textContent = cardData.words[2]; // bottom
                cardWords[3].textContent = cardData.words[1]; // left

                // Save card ID and initialize rotation
                cardIds.set(gameCard, cardData.id);
                cardRotations.set(gameCard, 0);

                // Add rotate button if it doesn't exist
                if (!gameCard.querySelector('.rotate-btn')) {
                    const rotateBtn = document.createElement('button');
                    rotateBtn.className = 'rotate-btn';
                    rotateBtn.textContent = '↻';
                    rotateBtn.addEventListener('click', handleRotate);
                    gameCard.appendChild(rotateBtn);
                }
            }
        });
    }
    
    // Store puzzle solution
    if (puzzle && puzzle.solution) {
        puzzleSolution = puzzle.solution;
    }
    
    // Populate clues around the board
    if (puzzle && puzzle.clues) {
        // Assuming puzzle.clue contains the clue text sections
        const clueTexts = puzzle.clues || [];
        if (clueTexts.length >= 4) {
            document.querySelector('.top-clue').textContent = clueTexts[0];
            document.querySelector('.right-clue').textContent = clueTexts[1];
            document.querySelector('.bottom-clue').textContent = clueTexts[2];
            document.querySelector('.left-clue').textContent = clueTexts[3];
        }
    }
}

window.addEventListener('load', initSolve);

function checkSolution() {
    if (!puzzleSolution) {
        console.log('No solution data available');
        return false;
    }
    
    const boardSlots = Array.from(document.querySelectorAll('.board-grid .card-slot'));
    const slotOrder = [0,1,3,2];
    for (let i = 0; i < boardSlots.length; i++) {
        const slot = boardSlots[slotOrder[i]];
        const card = slot.querySelector('.game-card');
        
        if (!card) {
            return false; // No card in this slot
        }
        
        const cardId = cardIds.get(card);
        const cardRotation = cardRotations.get(card) || 0;
        const expectedSolution = puzzleSolution[i];
        
        if (!expectedSolution) {
            return false; // No expected solution for this position
        }
        
        const expectedId = expectedSolution.id;
        const expectedRotation = expectedSolution.orient % 4;
        
        if (cardId !== expectedId || cardRotation !== expectedRotation) {
            console.log("found problem", cardId, expectedId, cardRotation, expectedRotation);
            return false; // Card ID or rotation doesn't match
        }
    }
    
    return true; // All positions are correct
}

function solveAttempt() {
    // Get all board slots (not card holders)
    const boardSlots = document.querySelectorAll('.board-grid .card-slot');
    const errorMessageDiv = document.getElementById('error-message');
    let allSlotsFilled = true;
    
    // Clear any previous error message
    errorMessageDiv.textContent = '';
    
    // Check if each board slot has a card
    boardSlots.forEach(slot => {
        if (!slot.querySelector('.game-card')) {
            allSlotsFilled = false;
        }
    });
    
    if (!allSlotsFilled) {
        errorMessageDiv.textContent = 'Bord incomplete';
        return;
    }
    
    // Check if solution is correct
    if (checkSolution()) {
        errorMessageDiv.textContent = 'Correct!';
        errorMessageDiv.style.color = '#27ae60';
    } else {
        errorMessageDiv.textContent = 'Incorrect solution';
        errorMessageDiv.style.color = '#e74c3c';
    }
}