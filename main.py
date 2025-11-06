#
# Libraries to use, subject to change
import argparse
from src.ppm_io import read_ppm, write_ppm, rgb_to_gray, gray_to_rgb
from src.filters import box_blur, sharpen, adjust_brightness, otsu_threshold, apply_threshold, invert

def main():
  parser = argparse.ArgumentParser(description="Basic Image Processing Tool (blur, sharpen, brightness, otsu, invert)")
  
  parser.add_argument("--op", required=True, choices=["blur", "sharpen", "brightness", "otsu", "invert"])
  parser.add_argument("--in", dest="inp", required=True)
  parser.add_argument("--out", dest="outp", required=True)
  parser.add_argument("--k", type=int, default=3)
  parser.add_argument("--delta", type=float, default=0.15)
  
  args = parser.parse_args()

  img = load_image(args.inp)

  if args.op == "blur":
    k = 5 if args.k == 5 else 3
    out = box_blur(img, k=k)
    
  elif args.op == "sharpen":
    out = sharpen(img)

  elif args.op == "brightness":
    out = adjust_brightness(img, delta=args.delta)
    
  elif args.op == "invert":
    out = invert(img)
    
  elif args.op == "otsu":
    
    gray = rgb_to_gray(img)
    t = otsu_threshold(gray)
    binary = apply_threshold(gray, t)
    out = gray_to_rgb(binary)
    print(f"Otsu threshold value: {t:.3f}")
    
  else:
    print("Invalid! Please choose from one of the 4 options.")


  save_image(args.outp, out)
  print(f"Saved output as {args.outp}")
    
if __name__ == "__main__":
    main()
 
