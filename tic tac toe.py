import random
from typing import List, Optional, Tuple

# ----- Board Utilities -----

Board = List[str]  # 9-length list with "X", "O", or " "

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),         # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),         # cols
    (0, 4, 8), (2, 4, 6)                      # diags
]

def new_board() -> Board:
    return [" "] * 9

def print_board(b: Board) -> None:
    def cell(i):
        return b[i] if b[i] != " " else str(i+1)
    rows = [
        f" {cell(0)} | {cell(1)} | {cell(2)} ",
        "---+---+---",
        f" {cell(3)} | {cell(4)} | {cell(5)} ",
        "---+---+---",
        f" {cell(6)} | {cell(7)} | {cell(8)} "
    ]
    print("\n".join(rows))

def available_moves(b: Board) -> List[int]:
    return [i for i, v in enumerate(b) if v == " "]

def winner(b: Board) -> Optional[str]:
    for a, c, d in WIN_LINES:
        if b[a] != " " and b[a] == b[c] == b[d]:
            return b[a]
    return None

def is_draw(b: Board) -> bool:
    return winner(b) is None and all(v != " " for v in b)

# ----- Human Move -----

def get_human_move(b: Board) -> int:
    legal = set(available_moves(b))
    while True:
        raw = input("Choose a cell (1-9): ").strip()
        if not raw.isdigit():
            print("Enter a number 1-9.")
            continue
        i = int(raw) - 1
        if i in legal:
            return i
        print("That cell is not available. Try again.")

# ----- Medium AI helpers (win/block) -----

def find_winning_move(b: Board, mark: str) -> Optional[int]:
    for i in available_moves(b):
        b[i] = mark
        if winner(b) == mark:
            b[i] = " "
            return i
        b[i] = " "
    return None

# ----- Minimax (Hard AI / Unbeatable) -----

def minimax(b: Board, ai: str, human: str, maximizing: bool) -> Tuple[int, Optional[int]]:
    w = winner(b)
    if w == ai:   return (1, None)
    if w == human:return (-1, None)
    if is_draw(b):return (0, None)

    best_move = None
    if maximizing:
        best_score = -10
        # simple move ordering: center -> corners -> edges
        for i in sorted(available_moves(b), key=move_priority, reverse=True):
            b[i] = ai
            score, _ = minimax(b, ai, human, False)
            b[i] = " "
            if score > best_score:
                best_score, best_move = score, i
                if best_score == 1:
                    break  # small pruning: can't beat a sure win
        return best_score, best_move
    else:
        best_score = 10
        for i in sorted(available_moves(b), key=move_priority, reverse=True):
            b[i] = human
            score, _ = minimax(b, ai, human, True)
            b[i] = " "
            if score < best_score:
                best_score, best_move = score, i
                if best_score == -1:
                    break
        return best_score, best_move

def move_priority(i: int) -> int:
    # Center highest, then corners, then edges
    if i == 4: return 3
    if i in (0, 2, 6, 8): return 2
    return 1

def ai_move(b: Board, ai: str, human: str, difficulty: str) -> int:
    difficulty = difficulty.lower()
    if difficulty == "easy":
        return random.choice(available_moves(b))
    if difficulty == "medium":
        # 1) Try to win
        m = find_winning_move(b, ai)
        if m is not None:
            return m
        # 2) Block human win
        m = find_winning_move(b, human)
        if m is not None:
            return m
        # 3) Prefer center/corners, else random
        pref = [4, 0, 2, 6, 8]
        for p in pref:
            if p in available_moves(b):
                return p
        return random.choice(available_moves(b))
    # hard (default): Minimax
    _, m = minimax(b, ai, human, maximizing=True)
    return m if m is not None else random.choice(available_moves(b))

# ----- Game Loop -----

def play(difficulty: str = "hard", human_starts: bool = True) -> None:
    print(f"\nTic-Tac-Toe — difficulty: {difficulty.title()}, {'You start' if human_starts else 'AI starts'}")
    b = new_board()
    human, ai = ("X", "O") if human_starts else ("O", "X")
    current = "X"
    print_board(b)

    while True:
        if current == human:
            i = get_human_move(b)
            b[i] = human
        else:
            print("\nAI is thinking...")
            i = ai_move(b, ai, human, difficulty)
            b[i] = ai
            print(f"AI plays at {i+1}")

        print()
        print_board(b)

        w = winner(b)
        if w:
            print("\nYou win! 🎉" if w == human else "\nAI wins! 🤖")
            break
        if is_draw(b):
            print("\nIt's a draw.")
            break

        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    # Configure here or prompt the user:
    # difficulty: "easy", "medium", or "hard"
    diff = input("Choose difficulty (easy/medium/hard) [hard]: ").strip().lower() or "hard"
    first = input("Do you want to start? (y/n) [y]: ").strip().lower() or "y"
    play(difficulty=diff, human_starts=(first == "y"))
