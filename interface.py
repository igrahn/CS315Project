#---------------------------------------------------------#
# File: interface.py
# Author: Ian Grahn and Matthew Barbarisi
# Purpose: File for user interaction and image processing
# Version: 1.9 Nov 12 2025
# Resources: Me and Matthew wroe the code, ChatGPT helped with compilation erros, and checking for
# redundant or uselss parts of the code. It also helepd greatly with syntax and compilation errors.
# OpenAI (2025) *ChatGPT* (Version 5) (Generative AI Model).
# https://www.openai.com/chatgpt/
#---------------------------------------------------------#

import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

from src.io_image import load_image, save_image
from src.filters import (
    box_blur, sharpen, adjust_brightness, invert,
    rgb_to_gray, gray_to_rgb, otsu_threshold, apply_threshold,
)

FILETYPES = [
    ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
    ("All files", "*.*"),
]

def ask_op(root):
    """
    GUI-only operation chooser. Returns:
      "blur" | "sharpen" | "bright" | "invert" | "otsu" | "done" | None (cancel)
    """
    ops = [
        "1) Blur",
        "2) Sharpen",
        "3) Brightness",
        "4) Invert",
        "5) Otsu (B/W)",
        "6) Finish & Save",
    ]
    choice = simpledialog.askstring("Operation", "\n".join(ops), parent=root)
    if not choice:
        return None
    return {
        "1": "blur",
        "2": "sharpen",
        "3": "bright",
        "4": "invert",
        "5": "otsu",
        "6": "done",
    }.get(choice.strip(), "invalid")

def main():
    root = tk.Tk()
    root.withdraw()
    try:
        # keep dialogs on top 
        root.attributes("-topmost", True)
        root.update()
    except Exception:
        pass

    # Pick input
    in_path = filedialog.askopenfilename(title="Select an image", filetypes=FILETYPES, parent=root)
    if not in_path:
        messagebox.showinfo("No file", "No file selected. Exiting.", parent=root)
        return
    if not os.path.exists(in_path):
        messagebox.showerror("Error", f"File not found:\n{in_path}", parent=root)
        return

    try:
        img = load_image(in_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image:\n{e}", parent=root)
        return

    # Loop: apply edits until user chooses finish and save
    while True:
        op = ask_op(root)
        if op is None:
            # user closed the dialog, then confirm finish
            if messagebox.askyesno("Finish?", "No operation selected.\nWould you like to finish and save now?", parent=root):
                break
            else:
                continue
        if op == "done":
            break
        if op == "invalid":
            messagebox.showwarning("Invalid", "Please enter a number from 1–6.", parent=root)
            continue

        try:
            if op == "blur":
                k_str = simpledialog.askstring("Blur kernel", "Kernel size (3 or 5):",
                                               initialvalue="3", parent=root)
                try:
                    k = int(k_str) if k_str else 3
                except Exception:
                    k = 3
                k = 5 if k == 5 else 3
                img = box_blur(img, k=k)

            elif op == "sharpen":
                img = sharpen(img)

            elif op == "bright":
                delta_str = simpledialog.askstring("Brightness",
                                                   "Change amount (e.g. 0.2 or -0.2):",
                                                   initialvalue="0.15", parent=root)
                try:
                    delta = float(delta_str) if delta_str else 0.15
                except Exception:
                    delta = 0.15
                img = adjust_brightness(img, delta=delta)

            elif op == "invert":
                root.update_idletasks()
                img = invert(img)

            elif op == "otsu":
                gray = rgb_to_gray(img)
                t = otsu_threshold(gray)
                bw = apply_threshold(gray, t)
                img = gray_to_rgb(bw)
                messagebox.showinfo("Otsu threshold", f"Threshold value: {t:.3f}", parent=root)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while applying the filter:\n{e}", parent=root)
            continue

    # Save final
    base, _ = os.path.splitext(in_path)
    suggested = base + "_result.jpg"
    out_path = filedialog.asksaveasfilename(
        title="Save final image as...",
        defaultextension=".jpg",
        initialfile=os.path.basename(suggested),
        filetypes=FILETYPES,
        parent=root,
    )
    if not out_path:
        messagebox.showinfo("Canceled", "Save canceled.", parent=root)
        return

    try:
        save_image(out_path, img)
        messagebox.showinfo("Done", f"All edits applied.\nSaved:\n{out_path}", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save image:\n{e}", parent=root)

if __name__ == "__main__":
    main()
