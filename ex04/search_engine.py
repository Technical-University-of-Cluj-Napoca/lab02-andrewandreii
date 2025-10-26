"""
This module is implementing a search loop for autocomplete suggestions using a binary search tree (BST)
inside the `search_loop` function.
"""

from BST import BST
import sys
import os

def get_char() -> str:
    """
    Read one character from stdin without pressing Enter.
    Returns:
        str: The character read from stdin.
    """
    ch = ""
    try:
        # Unix-like system (i.e. Mac, Linux)
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except ImportError:
        # Windows system
        import msvcrt
        ch =  msvcrt.getch().decode("utf-8")
    return ch


def search_loop(bst: BST) -> None:
    """
    Prompts the user to type a word, and it will display the first 7 autocomplete suggestions
    from a given knowledge base dictionary. The loop runs until the user is pressing ESC to quit.
    Args:
        bst (BST): The binary search tree containing the dictionary words.
    Returns:
        None
    """
    prefix = ""
    while True:
        ch = get_char()

        # Exit on ESC
        if ord(ch) == 27:
            print("\nExiting...")
            break

        # Backspace (delete last char)
        if ch in ("\b", "\x7f"):            # \x7f for Linux/mac
            prefix = prefix[:-1]
        elif ch == "\r":                    # ignore carriage return key (aka, Windows Enter)
            continue
        else:
            prefix += ch.lower()

        # Clear screen for nice output
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Search for >> {prefix}")
        suggestions = bst.autocomplete(prefix)
        if suggestions:
            for s in suggestions[:7]:  # show only first 7 suggestions
                print(s)
        else:
            print("No matches found.")
        print("\n(Press ESC to quit)")
