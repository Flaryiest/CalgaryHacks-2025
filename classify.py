import cv2
import numpy as np
import json

# Define biome color ranges in HSV
biomes = {
    "ocean": [(90, 50, 50), (130, 255, 255)],   # Blue tones
    "sand": [(15, 50, 100), (35, 255, 255)],    # Yellow/Tan tones
    "grass": [(35, 50, 50), (85, 255, 255)],    # Green tones
    "ice": [(0, 0, 200), (180, 50, 255)]        # White/light blue
}

def classify_biomes(image_path, output_json="biome_coordinates.json"):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    biome_coords = {biome: [] for biome in biomes}

    for biome, (lower, upper) in biomes.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        coords = np.column_stack(np.where(mask > 0))
        biome_coords[biome] = [[int(x), int(y)] for y, x in coords]  # Convert to (x, y) format

    # Save to JSON
    with open(output_json, "w") as f:
        json.dump(biome_coords, f, indent=2)

    print(f"Biome coordinates saved to {output_json}")

# Example usage
image_path = "assets\\map.png"  # Change this to your image file
classify_biomes(image_path)
