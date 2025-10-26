"""
Simple file encryption and decryption utility using a Caesar cipher.

Provides both CLI arguments and interactive prompts so the user can choose
between encrypting or decrypting any text file on disk.
"""
from __future__ import annotations
"""
Workflow:

1. Enter "encrypt" to encrypt a file or "decrypt" to decrypt a file.
2. Provide the path to the text file.
3. Optionally specify an output file path and shift value for the Ceaser Cipher. Else it would be defaulted to 3.
4. Enter the path to store the processed cipher file.

Sample Command:

    python file_encryptor.py encrypt input.txt -o output.txt --shift 3
    python file_encryptor.py decrypt input_encrypted.txt -o output_decrypted.txt --shift 3
    
    Or (You can specify line by line CLI)
    
    python file_encryptor.py
    encrypt
    input.txt (path to input file)
    6 (shift value)
    output.txt (path to output file)
    
"""

import argparse
from pathlib import Path
from typing import Optional

DEFAULT_SHIFT = 3


def caesar_cipher(text: str, shift: int) -> str:
    """Apply a Caesar cipher shift to text."""
    result_chars = []
    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
            offset = (ord(char) - base + shift) % 26
            result_chars.append(chr(base + offset))
        elif "A" <= char <= "Z":
            base = ord("A")
            offset = (ord(char) - base + shift) % 26
            result_chars.append(chr(base + offset))
        else:
            result_chars.append(char)
    return "".join(result_chars)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"Unsupported encoding for {path}. Use UTF-8 text files.")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def process_file(
    input_path: Path,
    output_path: Optional[Path],
    shift: int,
    *,
    encrypt: bool,
) -> Path:
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = output_path or default_output_path(input_path, encrypt=encrypt)

    original_text = read_text(input_path)
    effective_shift = shift if encrypt else -shift
    processed_text = caesar_cipher(original_text, effective_shift)
    write_text(output_path, processed_text)
    return output_path


def default_output_path(input_path: Path, *, encrypt: bool) -> Path:
    suffix = "_encrypted" if encrypt else "_decrypted"
    return input_path.with_name(f"{input_path.stem}{suffix}{input_path.suffix}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt text files using a Caesar cipher.",
    )
    subparsers = parser.add_subparsers(dest="command")

    def add_common_arguments(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "input_file",
            nargs="?",
            type=Path,
            help="Path to the text file to process.",
        )
        subparser.add_argument(
            "-o",
            "--output",
            type=Path,
            help="Path where the processed file should be saved.",
        )
        subparser.add_argument(
            "--shift",
            type=int,
            default=DEFAULT_SHIFT,
            help=f"Shift used by the Caesar cipher (default: {DEFAULT_SHIFT}).",
        )

    add_common_arguments(
        subparsers.add_parser("encrypt", help="Encrypt a text file."),
    )
    add_common_arguments(
        subparsers.add_parser("decrypt", help="Decrypt a text file."),
    )

    return parser


def interactive_prompt(parser: argparse.ArgumentParser) -> argparse.Namespace:
    print("No arguments supplied; entering interactive mode.\n")
    command = ""
    while command not in {"encrypt", "decrypt"}:
        command = input("Do you want to encrypt or decrypt a file? [encrypt/decrypt]: ").strip().lower()

    input_file = None
    while not input_file:
        raw_path = input("Enter the path to the text file: ").strip()
        path = Path(raw_path)
        if path.is_file():
            input_file = path
        else:
            print(f"File not found: {raw_path}")

    while True:
        shift_raw = input(f"Enter shift amount (press Enter for default {DEFAULT_SHIFT}): ").strip()
        if not shift_raw:
            shift = DEFAULT_SHIFT
            break
        try:
            shift = int(shift_raw)
            break
        except ValueError:
            print("Shift must be an integer. Try again.")

    output_raw = input("Enter output path (press Enter to use the default naming): ").strip()
    output = Path(output_raw) if output_raw else None

    args_list = [command, str(input_file), "--shift", str(shift)]
    if output:
        args_list[2:2] = ["-o", str(output)]

    return parser.parse_args(args_list)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        args = interactive_prompt(parser)

    try:
        output_path = process_file(
            args.input_file,
            args.output,
            args.shift,
            encrypt=(args.command == "encrypt"),
        )
        print(f"Success! Output written to: {output_path}")
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
