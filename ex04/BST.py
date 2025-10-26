import requests

class Node:
    def __init__(self, word: str):
        self.word = word
        self.right = None
        self.left = None

class BST:
    def __init__(self, source: str, **kwargs):
        def load_url(url) -> list[str]:
            return requests.get(url).content.decode("utf-8").splitlines()

        def load_file(path) -> list[str]:
            return open(path, "r").read().splitlines()

        words = []
        if kwargs.get("url", False):
            words = load_url(source)
        elif kwargs.get("file", False):
            words = load_file(source)
        else:
            raise ValueError("Unspecified type of source")

        self.root = self._build_tree(words, 0, len(words))

    @staticmethod
    def _build_tree(words: list[str], start: int, end: int) -> Node:
        if start >= end:
            return None

        mid = (start + end) // 2
        node = Node(words[mid])
        node.right = BST._build_tree(words, start, mid)
        node.left = BST._build_tree(words, mid + 1, end)

        return node

    def autocomplete(self, prefix: str) -> list[str]:
        results = []
        self._collect(self.root, prefix, results)
        return results

    def _collect(self, node: Node, prefix: str, results: list[str]):
        if node is None:
            return

        self._collect(node.left, prefix, results)
        if node.word.startswith(prefix):
            results.append(node.word)
        self._collect(node.right, prefix, results)
