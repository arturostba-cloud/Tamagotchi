import os
from PIL import Image

def image_to_mono_vlsb_bytes(image):
    width, height = image.size
    pixels = image.load()

    data = []

    for page in range((height + 7) // 8):      # each group of 8 rows
        for x in range(width):                 # left to right
            byte = 0

            for bit in range(8):
                y = page * 8 + bit
                if y >= height:
                    continue

                if pixels[x, y] != 0:          # black pixel
                    byte |= (1 << bit)

            data.append(byte)

    return data


def convert_images(paths):
    sprites = []

    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]

        img = Image.open(path).convert("1")
        width, height = img.size

        data = image_to_mono_vlsb_bytes(img)

        sprites.append({
            "name": name,
            "width": width,
            "height": height,
            "data": data
        })

    # ---- Print bytearrays first ----
    for sprite in sprites:
        print(f"{sprite['name']} = bytearray([")

        for i, byte in enumerate(sprite["data"]):
            if i % 12 == 0:
                print("    ", end="")
            print(f"0x{byte:02x}, ", end="")
            if (i + 1) % 12 == 0:
                print()

        print("\n])\n")

    # ---- Print framebuffer definitions ----
    for sprite in sprites:
        print(
            f"{sprite['name']}_fb = framebuf.FrameBuffer("
            f"{sprite['name']}, {sprite['width']}, {sprite['height']}, framebuf.MONO_VLSB)"
        )


def collect_paths(path):
    paths = []

    if os.path.isfile(path):
        return [path]

    for root, dirs, files in os.walk(path):
        for file in sorted(files):
            if file.lower().endswith((".png", ".bmp", ".jpg")):
                paths.append(os.path.join(root, file))

    return paths


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("python img_to_bytearray.py image.png")
        print("python img_to_bytearray.py folder/")
        exit()

    paths = collect_paths(sys.argv[1])
    convert_images(paths)