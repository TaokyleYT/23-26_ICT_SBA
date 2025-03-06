


if __name__ == "__main__":
    print(f"{type_check(1, int) = }")
    print(f"{type_check(1, float) = }")
    print(f"{type_check(True, bool) = }")
    print(f"{type_check([1, 2, 3], list[int]) = }")
    print(f"{type_check([1, 'A', 3], list[int]) = }")
    print(f"{type_check((1,2,3,4,5), tuple[int, ...]) = }")
    print(f"{type_check((1, 'A', [0.1, 0.2]), tuple[int, str, list[float]]) = }")
    print(f"{type_check(1, int|bool) = }")
