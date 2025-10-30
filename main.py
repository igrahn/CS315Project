#
# Libraries to use, subject to change
import argparse
from src.ppm_io import read_ppm, write_ppm, rgb_to_gray, gray_to_rgb
from src.filters import box_blur, sharpen, sobel_edges, otsu_threshold, apply_threshold

def main():

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
 
