import numpy as np
from PIL import Image
import argparse

# === Encryption & Decryption using XOR method ===
def xor_image(image_path, key, output_path):
    # Open image and convert to array
    img = Image.open(image_path)
    arr = np.array(img)

    # Convert key to bytes
    key_bytes = [ord(char) for char in key]
    key_len = len(key_bytes)

    # Apply XOR operation to each pixel
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(arr.shape[2]):
                arr[i, j, k] = arr[i, j, k] ^ key_bytes[(i + j + k) % key_len]

    # Save encrypted/decrypted image
    result = Image.fromarray(arr)
    result.save(output_path)
    print(f"✅ Image saved as: {output_path}")

# === Encryption & Decryption using Shuffle method ===
def shuffle_image(image_path, key, output_path, decrypt=False):
    img = Image.open(image_path)
    arr = np.array(img)
    flat = arr.reshape(-1, 3)

    np.random.seed(sum([ord(c) for c in key]))

    if decrypt:
        # Recreate shuffle order
        idx = np.arange(flat.shape[0])
        np.random.shuffle(idx)
        unshuffle = np.argsort(idx)
        flat = flat[unshuffle]
    else:
        np.random.shuffle(flat)

    shuffled = flat.reshape(arr.shape)
    Image.fromarray(shuffled).save(output_path)
    print(f"✅ Image saved as: {output_path}")

# === Main Function ===
def main():
    parser = argparse.ArgumentParser(description="Simple Image Encryption Tool using Pixel Manipulation")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Choose operation")
    parser.add_argument("input", help="Input image file path")
    parser.add_argument("output", help="Output image file path")
    parser.add_argument("--method", choices=["xor", "shuffle"], default="xor", help="Encryption method")
    parser.add_argument("--key", required=True, help="Secret key for encryption/decryption")

    args = parser.parse_args()

    if args.method == "xor":
        xor_image(args.input, args.key, args.output)
    elif args.method == "shuffle":
        shuffle_image(args.input, args.key, args.output, decrypt=(args.operation == "decrypt"))

if __name__ == "__main__":
    main()
