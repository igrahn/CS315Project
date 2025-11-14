#---------------------------------------------------------#
# File: filters.py
# Author: Ian Grahn and Matthew Barbarisi
# Purpose: File for handling filter references
# Version: 1.6 Nov 12 2025
# Resources: Me and Matthew wroe the code, ChatGPT helped with compilation erros, and checking for
# redundant or uselss parts of the code. It also helepd greatly with syntax and compilation errors.
# OpenAI (2025) *ChatGPT* (Version 5) (Generative AI Model).
# https://www.openai.com/chatgpt/
#---------------------------------------------------------#


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x

# edge handling, chosen over zero padding so that borders dont darken on blur/sharpen
def _get_rgb(img, i, j):
    """Repeat nearest border pixel if (i, j) is outside the image."""
    h = len(img)
    w = len(img[0])

    if i < 0:
        i = 0
    if j < 0:
        j = 0
    if i >= h:
        i = h - 1
    if j >= w:
        j = w - 1

    return img[i][j]


# Convolution (RGB)
def convolve_rgb(img, ker):
    """Apply a kxk kernel to each RGB channel separately."""
    k = len(ker)
    r = k // 2

    h = len(img)
    w = len(img[0])

    out = [[(0.0, 0.0, 0.0)] * w for _ in range(h)]

    for i in range(h):
        for j in range(w):
            sr = 0.0
            sg = 0.0
            sb = 0.0

            for a in range(-r, r + 1):
                for b in range(-r, r + 1):
                    r0, g0, b0 = _get_rgb(img, i + a, j + b)
                    wgt = ker[a + r][b + r]
                    sr += r0 * wgt
                    sg += g0 * wgt
                    sb += b0 * wgt

            out[i][j] = (_clamp01(sr), _clamp01(sg), _clamp01(sb))

    return out



# Filters
#intentionally constrained to 3:5
def box_kernel(k: int):
    """Uniform kxk kernel where all entries are 1/(k*k)."""
    weight = 1.0 / (k * k)
    return [[weight] * k for _ in range(k)]


def box_blur(img, k: int = 3):
    """Box blur with k=3 or 5."""
    k = 5 if k == 5 else 3
    return convolve_rgb(img, box_kernel(k))


def sharpen(img):
    """Simple sharpening kernel."""
    ker = [
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ]
    return convolve_rgb(img, ker)


def adjust_brightness(img, delta: float = 0.15):
    """Add 'delta' to each channel and clamp to [0,1]."""
    out = []
    for row in img:
        new_row = []
        for (r, g, b) in row:
            new_row.append((_clamp01(r + delta), _clamp01(g + delta), _clamp01(b + delta)))
        out.append(new_row)
    return out


def invert(img):
    """Invert colors: (r,g,b) -> (1-r, 1-g, 1-b)."""
    out = []
    for row in img:
        new_row = []
        for (r, g, b) in row:
            new_row.append((1.0 - r, 1.0 - g, 1.0 - b))
        out.append(new_row)
    return out


# Grayscale and OTSU

def rgb_to_gray(img):
    """Convert RGB floats to grayscale floats in [0,1] (luminosity method)."""
    h = len(img)
    w = len(img[0])

    gray = [[0.0] * w for _ in range(h)]

    for i in range(h):
        for j in range(w):
            r, g, b = img[i][j]
            gray[i][j] = 0.299 * r + 0.587 * g + 0.114 * b

    return gray


def gray_to_rgb(gray):
    """Expand grayscale floats to RGB triples."""
    h = len(gray)
    w = len(gray[0])

    out = []
    for i in range(h):
        row = []
        for j in range(w):
            v = gray[i][j]
            row.append((v, v, v))
        out.append(row)

    return out


def histogram(gray):
    """Return a list[256] with counts of grayscale intensities."""
    hist = [0] * 256
    h = len(gray)
    w = len(gray[0])

    for i in range(h):
        for j in range(w):
            b = int(gray[i][j] * 255 + 0.5)
            if b < 0:
                b = 0
            if b > 255:
                b = 255
            hist[b] += 1

    return hist

#overall O(N)
def otsu_threshold(gray):
    """Compute Otsu's threshold as a float in [0,1]."""
    hist = histogram(gray)
    total = sum(hist)

    if total == 0:
        return 0.5

    p = [x / total for x in hist]

    omega = [0.0] * 256
    mu = [0.0] * 256

    cw = 0.0
    cm = 0.0
    for i in range(256):
        cw += p[i]
        cm += p[i] * i
        omega[i] = cw
        mu[i] = cm

    mu_t = mu[-1]
    best_t = 0
    best_sigma = -1.0

    
#    mu_t = mu[-1]
#    best_t = 0
#    best_sigma = -1.0

    for t in range(256):
        w0 = omega[t]
        w1 = 1.0 - w0

        if w0 <= 1e-12 or w1 <= 1e-12:
            continue

        mu0 = mu[t] / w0
        mu1 = (mu_t - mu[t]) / w1
        sigma_b2 = w0 * w1 * (mu0 - mu1) ** 2

        if sigma_b2 > best_sigma:
            best_sigma = sigma_b2
            best_t = t

    return best_t / 255.0

# apply threshold
def apply_threshold(gray, t: float):
    """Return a binary image (0.0 or 1.0) based on threshold t in [0,1]."""
    h = len(gray)
    w = len(gray[0])

    out = []
    for i in range(h):
        row = []
        for j in range(w):
            row.append(1.0 if gray[i][j] >= t else 0.0)
        out.append(row)

    return out
