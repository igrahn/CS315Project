import cv2

def load_image(path):
  img = cv2.imread(path)
  if img is None:
    raise FileNotFoundError(f"Could not open {path}")
  h, w = img.shape[:2]
  data = []
  for i in range(h):
    row = []
    for j in range(w):
      b, g, r = img[i, j]
      row.append((r/255.0, g/255.0, b/255.0))
    data.append(row)
  return data

def save_image(path, data):
  import numpy as np
  h = len(data)
  w = len(data[0]) if h else 0
  img = np.zeros((h, w, 3), dtype="uint8")
  for i in range(h):
    for j in range(w):
      r, g, b = data[i][j]
      img[i, j, 0] = int(max(0.0, min(1.0, b)) * 255 + 0.5)
      img[i, j, 1] = int(max(0.0, min(1.0, g)) * 255 + 0.5)
      img[i, j, 2] = int(max(0.0, min(1.0, r)) * 255 + 0.5)
  cv2.imwrite(path, img)
