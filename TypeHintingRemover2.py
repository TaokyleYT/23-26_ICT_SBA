from __future__ import annotations
import re
import os

PATTERNS = [
    # prune imports
    (r"from __future__ import annotations\n", ""),
    (r"from typing.*", ""),
    (r"import typing", ""),

    # match other patterns
    (r":\s[a-zA-Z]+\[[a-zA-Z]+\[[a-zA-Z]+,\s[a-zA-Z]+\[[a-zA-Z]+,\s[a-zA-Z]+\]\]\]", ""), # matches: ': List[Dict[str, Union[float, int]]]'
    (r"\s->\s[a-zA-Z]+\[[a-zA-Z]+\[[a-zA-Z]+\],\s[a-zA-Z]+\[[a-zA-Z]+\]\]", ""),    # matches: ' -> Tuple[List[Note], List[Error]]'
    (r":\s[a-zA-Z]+\[[a-zA-Z]+,\s[a-zA-Z]+\]", ""), # matches ': Union[int, Note]'
    (r":\s[a-zA-Z]+\[[a-zA-Z]+\[[a-zA-Z]+\],\s[a-zA-Z]+\]", ""),  # matches ': Union[List[Note], Note]'
    (r":\s[a-zA-Z]+\[[a-zA-Z]+\]", ""),  # matches ': List[float]'
    (r"\s->\s[a-zA-Z]+\[[a-zA-Z]+,\s[a-zA-Z]+\]", ""),  # matches ' -> Union[int, Note]'
    (r"\s->\s[a-zA-Z]+\[[a-zA-Z]+\]", ""),  # matches ' -> List[float]'
    (r"\s->\s[a-zA-Z]+", ""),  # matches ' -> Note')

    # prune single type
    (r"(?<!\"):\s[a-zA-Z]+,", ","),
    (r":\s[a-zA-Z]+\)", ")"),
    (r":\s[a-zA-Z]+\s\=(?!\=)", " =")

]

def main():
    if not os.path.exists("NoTypeHintPy2"):
        os.mkdir("NoTypeHintPy2")
    for file in os.listdir("."):
        if not file.endswith(".py") or os.path.samefile(file, __file__) or "TypeHintingRemover" in file:
            continue
        print("Attempting to remove type hints for", file)
        try:
            with open(file, "r", errors="ignore") as sourceFile:
                source = "".join(sourceFile.readlines())
                for pattern in PATTERNS:
                    dest = re.sub(pattern[0], pattern[1], source)
                with open(
                    os.path.join(os.path.dirname(file), f"NoTypeHintPy2/{file}"), "w"
                ) as destFile:
                    destFile.write(dest)
                print("Successfully removed type hints for", file, "\n")
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    print("All processed files have been saved in the 'NoTypeHintPy2' directory.")


if __name__ == "__main__":
    main()
