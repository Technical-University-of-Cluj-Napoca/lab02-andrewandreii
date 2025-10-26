from functools import reduce

def multiply_all(*args: int) -> int:
    return reduce(lambda x, y: x * y, args, 1)

if __name__ == "__main__":
    print(multiply_all(*range(1, 6)))
