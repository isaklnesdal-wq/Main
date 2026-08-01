#!/usr/bin/env python3
"""Widen the hero backdrop photo so the basket sits further back and left.

The supplied photo (hero-bg-source.webp, 1229x864) has the basket 36% in
from the left. At desktop proportions the photo is width-limited by
object-fit: cover, so there is no room to pan — the basket lands directly
behind the floating disc and cannot be moved by CSS alone.

Enlarging the canvas fixes both complaints at once:

  * the basket's share of the frame drops from 36% to 25%, so panning the
    crop right now moves it clear of the disc;
  * the wider 1.75 aspect makes a 16:10 viewport crop on width instead of
    height, which scales the whole scene down 23% — the basket reads as
    further away.

The added area is the photo's own forest, mirrored and defocused. The blur
is what makes this work: it removes the mirror symmetry that would
otherwise be obvious, and reads as depth of field, which the photo already
has elsewhere. Roughly 30% of the width and a band at the top are
synthetic — acceptable behind a large foreground subject and under the
hero scrim, but it is not photography, so prefer a genuinely wider
original if one is available.

Pairs with the object-position values in index.html (85% desktop, 46%
mobile). Regenerating with different dimensions means retuning those.

Usage:  python3 widen-hero-bg.py
"""
from PIL import Image, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'hero-bg-source.webp')
DST = os.path.join(HERE, 'hero-bg-wide.webp')

TARGET_W, TARGET_H = 1750, 1000
OVX, OVY = 190, 90          # feathered overlaps, in px
BLUR_SIDE, BLUR_TOP = 9, 14


def ramp(w, h, length, axis):
    """Alpha mask fading in over `length` px along `axis`."""
    m = Image.new('L', (w, h), 255)
    p = m.load()
    if axis == 'x':
        for x in range(length):
            v = int(255 * x / length)
            for y in range(h):
                p[x, y] = v
    else:
        for y in range(h - length, h):
            v = int(255 * (h - y) / length)
            for x in range(w):
                p[x, y] = v
    return m


def main():
    src = Image.open(SRC).convert('RGB')
    w, h = src.size
    top = TARGET_H - h

    # widen to the right with mirrored, defocused forest
    ext_w = TARGET_W - (w - OVX)
    strip = (src.crop((560, 0, w, h))
                .transpose(Image.FLIP_LEFT_RIGHT)
                .resize((ext_w, h), Image.LANCZOS)
                .filter(ImageFilter.GaussianBlur(BLUR_SIDE)))
    wide = Image.new('RGB', (TARGET_W, h))
    wide.paste(src, (0, 0))
    wide.paste(strip, (w - OVX, 0), ramp(ext_w, h, OVX, 'x'))

    # add canopy above; it is soft glare up there already
    cap = (wide.crop((0, 0, TARGET_W, 300))
               .transpose(Image.FLIP_TOP_BOTTOM)
               .resize((TARGET_W, top + OVY), Image.LANCZOS)
               .filter(ImageFilter.GaussianBlur(BLUR_TOP)))
    out = Image.new('RGB', (TARGET_W, TARGET_H))
    out.paste(wide, (0, top))
    out.paste(cap, (0, 0), ramp(TARGET_W, top + OVY, OVY, 'y'))

    out.save(DST, 'WEBP', quality=88, method=6)
    print('wrote %s %s %d bytes' % (DST, out.size, os.path.getsize(DST)))
    print('basket x: %.1f%% -> %.1f%% of frame' % (440 / w * 100, 440 / TARGET_W * 100))


if __name__ == '__main__':
    main()
