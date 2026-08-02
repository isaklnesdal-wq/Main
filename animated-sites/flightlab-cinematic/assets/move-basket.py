#!/usr/bin/env python3
"""Move the basket left and further back inside the hero photo.

In the supplied photo the basket stands 36% in from the left, dead centre
of where the floating disc sits, so the disc hides it. At desktop
proportions object-fit: cover is width-limited, so CSS panning cannot help.

This edits the photograph instead: paint the basket out, then paste it
back smaller, further left, and higher up the ground plane. The rest of
the frame is the untouched original — no blurred filler.

Two details matter:

  * The paint-out area is deliberately larger than the basket. A feathered
    mask is transparent at its edges, so a box drawn tight to the basket
    leaves its rim and pole showing through as a ghost. Enlarging the box
    puts the feather on plain forest and keeps the opaque core over the
    whole basket.

  * The basket is cut with a margin of surrounding forest, so the pasted
    patch blends forest-into-forest rather than showing a hard rectangle.

Fill comes from the sunlit floor to the basket's left, mirrored — same
light direction, so it matches. A faint haze is mixed into the moved
basket so it reads as distance rather than merely shrunk.

Usage:  python3 move-basket.py
"""
from PIL import Image, ImageEnhance
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'hero-bg-source.webp')
DST = os.path.join(HERE, 'hero-bg-moved.webp')

HOLE = (275, 200, 615, 770)   # painted out; larger than the basket on purpose
FILL = (0, 200, 315, 770)     # clean sunlit floor to its left
BOX = (300, 235, 590, 740)    # basket plus a margin of forest
FEATHER_HOLE, FEATHER_BASKET = 35, 34
SCALE = 0.62                  # 38% smaller => further away
GROUND_Y = 718                # where the pole meets the moss
BASKET_CX = 445               # basket centre in the original
DX, DY = -180, -70            # left, and up the ground plane


def feather(w, h, f):
    """Alpha mask: opaque core, linear ramp to 0 over f px at every edge."""
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.minimum(np.minimum(xx, w - 1 - xx),
                   np.minimum(yy, h - 1 - yy)).astype(np.float32)
    return Image.fromarray((np.clip(d / f, 0, 1) * 255).astype(np.uint8), 'L')


def main():
    src = Image.open(SRC).convert('RGB')
    basket = src.crop(BOX)          # grab before painting over it
    out = src.copy()

    hw, hh = HOLE[2] - HOLE[0], HOLE[3] - HOLE[1]
    patch = (src.crop(FILL)
                .transpose(Image.FLIP_LEFT_RIGHT)
                .resize((hw, hh), Image.LANCZOS))
    out.paste(patch, (HOLE[0], HOLE[1]), feather(hw, hh, FEATHER_HOLE))

    bw, bh = BOX[2] - BOX[0], BOX[3] - BOX[1]
    nw, nh = int(bw * SCALE), int(bh * SCALE)
    small = basket.resize((nw, nh), Image.LANCZOS)
    small = ImageEnhance.Contrast(small).enhance(0.93)
    small = Image.blend(small, Image.new('RGB', (nw, nh), (214, 222, 198)), 0.08)

    # keep the pole's ground contact on the ground plane, then offset
    x = BASKET_CX + DX - int((BASKET_CX - BOX[0]) * SCALE)
    y = GROUND_Y + DY - int((GROUND_Y - BOX[1]) * SCALE)
    out.paste(small, (x, y), feather(nw, nh, FEATHER_BASKET))

    out.save(DST, 'WEBP', quality=90, method=6)
    w = src.size[0]
    print('wrote %s %d bytes' % (DST, os.path.getsize(DST)))
    print('basket centre %.1f%% -> %.1f%% of width, %d%% smaller'
          % (BASKET_CX / w * 100, (BASKET_CX + DX) / w * 100, (1 - SCALE) * 100))


if __name__ == '__main__':
    main()
