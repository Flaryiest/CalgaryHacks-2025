from PIL import Image, ImageDraw
import numpy as np

image_path = "Factory.png"
img = Image.open(image_path).convert("RGBA")
width, height = img.size
smoke_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(smoke_layer)
smoke_color = (150, 150, 150, 200)
smoke_positions = [
    (width // 2 - 10, height // 5),
    (width // 2, height // 6),
    (width // 2 + 10, height // 7),
    (width // 2 - 5, height // 4),
]

for x, y in smoke_positions:
    draw.rectangle([x, y, x + 6, y + 6], fill=smoke_color)
img = Image.alpha_composite(img, smoke_layer)
img.save("factory_with_smoke.png")
img.show()
