from search_engine import search_loop
from BST import BST
import sys

bst = None
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expected path to dictionary")
        exit(-1)

    bst = BST(sys.argv[1], file=True)

    search_loop(bst)
