#Using the Path module to make path-halding easier for reading files.
from pathlib import Path
import sys


def count_words(file_path: Path) -> int:
    """Return the number of whitespace-delimited words in the target file."""
    # Using split() without arguments collapses consecutive whitespace.
    text = file_path.read_text(encoding="utf-8")
    return len(text.split())


def main() -> None:
    print("================================ WORD COUNTER ==========================")
    print("Please run the script with a file path as an argument. And make sure to have it in the same workspace\n")
    print("Example: python word_counter.py <file_path>\n")

    raw_path = input("Enter file path: ").strip()

    if not raw_path:
        print("Error: no file path provided.\n")
        return

    target_path = Path(raw_path)
    if not target_path.is_absolute():
        target_path = Path(__file__).resolve().parent / target_path

    try:
        total_words = count_words(target_path)
    except FileNotFoundError:
        print(f"Error: file '{target_path}' not found.\n")
        sys.exit(1)
    except OSError as exc:
        print(f"Error reading file '{target_path}': {exc}")
        sys.exit(1)

    print(f"\nWord count: {total_words}")


if __name__ == "__main__":
    main()
