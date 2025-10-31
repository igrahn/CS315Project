import cv2
import os

def readInput():
    image = input("Enter the path to your image file: ").strip()
   
    if not os.path.isfile(image):
        print("Error: File does not exist.")
        return None

    extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    if not image.lower().endswith(extensions):
        print("Error: Unsupported file format.")
        return None

    return image

def resizeImage(new_width, new_height, image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Could not read image file.")
            return
        resized = cv2.resize(img, (new_width, new_height))
        cv2.imwrite("resized_output.png", resized)
        print("Image resized and saved as resized_output.png")
    except Exception as e:
        print(f"Error resizing image: {e}")

def main():
    image_path = readInput()
    if image_path:
        new_width = int(input("Enter new width: "))
        new_height = int(input("Enter new height: "))
        resizeImage(new_width, new_height, image_path)

if __name__ == "__main__":
    main()
