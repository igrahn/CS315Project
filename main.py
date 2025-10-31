#
# Libraries to use, subject to change
import argparse
from src.ppm_io import read_ppm, write_ppm, rgb_to_gray, gray_to_rgb
from src.filters import box_blur, sharpen, sobel_edges, otsu_threshold, apply_threshold

def parse_args():
  p = argparse.ArgumentParser(description=""

def main():

    parser = argparse.ArgumentParser(description="Basic Image Processing Tool (blur, sharpen, sobel, otsu)")
    parser.add_argument("--op", required=True)
    parser.add_argument("--in", dest="inp", required=True)
    parser.add_argument("--out", dest="outp", required=True)
    parser.add_argument("--k", type=int, default=3)
  
    args = parser.parse_args()

  img = read_ppm(args.inp)

  if args.op == "blur":
    out = box_blur(img, k=args.k)
    
  elif args.op == "sharpen":
    out = sharpen(img)
    
  elif args.op == "sobel":
    #
    #
    #
  elif args.op == "otsu":
    #
    #
    #
  else:
    raise ValueError("error!")
 
