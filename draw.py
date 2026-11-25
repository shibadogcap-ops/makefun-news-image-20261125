"""Deterministic 2D drawing primitives and PNG writer (stdlib only)."""

import struct
import zlib

INK = (24, 24, 28)
PAPER = (246, 242, 233)
ACCENT = (164, 32, 40)
GREY = (110, 108, 100)
LIGHT = (226, 220, 205)
BLUE = (36, 64, 120)
GOLD = (176, 132, 40)
GREEN = (44, 96, 60)
SKY = (168, 196, 224)


class Canvas:
    """RGB pixel canvas stored as a flat bytearray (r, g, b per pixel)."""

    def __init__(self, width, height, bg):
        self.width = width
        self.height = height
        r, g, b = bg
        px = bytes((r, g, b))
        self.data = bytearray(px * (width * height))

    def _index(self, x, y):
        # Returns the byte offset for (x, y), or None when out of bounds.
        if 0 <= x < self.width and 0 <= y < self.height:
            return (y * self.width + x) * 3
        return None

    def px(self, x, y, color):
        i = self._index(x, y)
        if i is not None:
            self.data[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0 = max(x, 0)
        y0 = max(y, 0)
        x1 = min(x + w, self.width)
        y1 = min(y + h, self.height)
        for yy in range(y0, y1):
            base = yy * self.width * 3
            for xx in range(x0, x1):
                i = base + xx * 3
                self.data[i:i + 3] = bytes(color)

    def frame(self, x, y, w, h, color, t=1):
        # Outline drawn inward from the rectangle edges.
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color):
        # Bresenham; both endpoints inclusive.
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def thick_line(self, x0, y0, x1, y1, color, t):
        # Bresenham points thickened into filled squares of side t.
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        half = t // 2
        while True:
            x0 -= half
            y0 -= half
            self.rect(x0, y0, t, t, color)
            x0 += half
            y0 += half
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color):
        # Filled circle via squared-distance test over the bounding box.
        r2 = r * r
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r2:
                    self.px(x, y, color)

    def ring(self, cx, cy, r, color, t=1):
        # Annulus: pixels whose distance sits within [r-t, r] (squared test).
        inner2 = max(r - t, 0) ** 2
        outer2 = r * r
        span = r + 1
        for y in range(cy - span, cy + span + 1):
            for x in range(cx - span, cx + span + 1):
                d2 = (x - cx) * (x - cx) + (y - cy) * (y - cy)
                if inner2 <= d2 <= outer2:
                    self.px(x, y, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        # Filled triangle via edge-function tests over its bounding box.
        min_x = max(min(x0, x1, x2), 0)
        max_x = min(max(x0, x1, x2) + 1, self.width)
        min_y = max(min(y0, y1, y2), 0)
        max_y = min(max(y0, y1, y2) + 1, self.height)
        # Edge functions: sign of cross product for each edge.
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                d1 = (x - x0) * (y1 - y0) - (x1 - x0) * (y - y0)
                d2 = (x - x1) * (y2 - y1) - (x2 - x1) * (y - y1)
                d3 = (x - x2) * (y0 - y2) - (x0 - x2) * (y - y2)
                has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
                has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
                if not (has_neg and has_pos):
                    self.px(x, y, color)


def _chunk(kind, payload):
    return (struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))


def save_png(canvas, path):
    """Write canvas to a PNG file (8-bit RGB, one IDAT, filter 0 rows)."""
    width, height = canvas.width, canvas.height
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw += canvas.data[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(_chunk(b"IHDR", ihdr))
        f.write(_chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(_chunk(b"IEND", b""))
