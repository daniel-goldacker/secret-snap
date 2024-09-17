import os
from PIL import Image

def str_to_bin(message):
    """Converts a message to its binary representation."""
    return ''.join(format(ord(char), '08b') for char in message)

def bin_to_str(bin_data):
    """Converts binary data to a string."""
    return ''.join(chr(int(bin_data[i:i + 8], 2)) for i in range(0, len(bin_data), 8))

def encode_message_in_image(image_path, message, output_image_name, instance_folder):
    """Encodes a message inside an image and saves to /instance."""
    img = Image.open(image_path)
    encoded_img = img.copy()
    width, height = img.size
    message += "===="  # End marker
    bin_message = str_to_bin(message)

    if len(bin_message) > width * height * 3:
        raise ValueError("Message is too long to fit in the image.")

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(encoded_img.getpixel((x, y)))
            for i in range(3):  # Modify the LSB of each color channel (R, G, B)
                if data_index < len(bin_message):
                    pixel[i] = pixel[i] & ~1 | int(bin_message[data_index])
                    data_index += 1
            encoded_img.putpixel((x, y), tuple(pixel))
            if data_index >= len(bin_message):
                break
        if data_index >= len(bin_message):
            break

    output_image_path = os.path.join(instance_folder, output_image_name)
    encoded_img.save(output_image_path)
    
    return output_image_path

def decode_message_from_image(image_path):
    """Decodes a secret message from an image."""
    img = Image.open(image_path)
    width, height = img.size
    bin_message = ""

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                bin_message += str(pixel[i] & 1)

    decoded_message = bin_to_str(bin_message)
    decoded_message = decoded_message.split("====")[0]  # Remove end marker
    return decoded_message
