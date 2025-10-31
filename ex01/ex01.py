from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    anagrams = defaultdict(list)
    for s in strs:
        c = "".join(sorted(s))
        anagrams[c].append(s)
    return list(anagrams.values())

if __name__ == "__main__":
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
