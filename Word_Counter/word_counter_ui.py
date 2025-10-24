from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from word_counter import count_words


def choose_file(result_var: tk.StringVar) -> None:
    """Prompt the user to pick a file and update the result label."""
    file_path_str = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if not file_path_str:
        return

    file_path = Path(file_path_str)

    try:
        total_words = count_words(file_path)
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"Cannot find '{file_path}'.")
        return
    except OSError as exc:
        messagebox.showerror("Read Error", f"Unable to read '{file_path}': {exc}")
        return

    result_var.set(f"Word count: {total_words}")


def main() -> None:
    root = tk.Tk()
    root.title("Word Counter")

    instructions = tk.Label(
        root,
        text=(
            "Upload a document to count its words.\n"
            "Make sure the file is accessible from this workspace."
        ),
        justify=tk.CENTER,
        padx=10,
        pady=10,
    )
    instructions.pack()

    result_var = tk.StringVar(value="Word count: N/A")

    upload_button = tk.Button(
        root,
        text="Choose File",
        command=lambda: choose_file(result_var),
        padx=10,
        pady=5,
    )
    upload_button.pack()

    result_label = tk.Label(root, textvariable=result_var, pady=10)
    result_label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
