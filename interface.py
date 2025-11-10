import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageEnhance
import os

def upload_image():
    # Let user select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.ppm *.gif")]
    )
    if not file_path:
        print("No file selected.")
        return

    # Load and display image info
    img = Image.open(file_path)
    print(f"Loaded image: {file_path}")
    print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")

    # Convert to PPM
    ppm_path = os.path.splitext(file_path)[0] + ".ppm"
    img.save(ppm_path)
    print(f"Image converted and saved as PPM: {ppm_path}")

    # Ask user which transformation to apply
    print("\nChoose an operation:")
    print("1. Convert to grayscale")
    print("2. Invert colors")
    print("3. Increase brightness")
    print("4. Decrease brightness")
    print("5. Rotate 90°")
    print("6. Flip horizontally")
    choice = input("Enter number (1–6): ")

    # Perform the selected operation
    if choice == "1":
        img = ImageOps.grayscale(img)
    elif choice == "2":
        img = ImageOps.invert(img.convert("RGB"))
    elif choice == "3":
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.5)
    elif choice == "4":
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.6)
    elif choice == "5":
        img = img.rotate(90, expand=True)
    elif choice == "6":
        img = ImageOps.mirror(img)
    else:
        print("Invalid choice. No operation applied.")

    # Save altered image as PPM
    altered_path = os.path.splitext(file_path)[0] + "_altered.ppm"
    img.save(altered_path)
    print(f"Altered image saved as: {altered_path}")

    # Optional: show image
    img.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window
    upload_image()
