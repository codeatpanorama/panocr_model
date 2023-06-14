import pytesseract
from PIL import Image
import os

# Set the path to the directory containing PNG files
png_dir = '.Data/marathi_handwritten_text'

# Create a directory for the output text files
output_dir = '.Data/marathi_handwritten_text'
os.makedirs(output_dir, exist_ok=True)

# Iterate over each PNG file in the directory
for filename in os.listdir(png_dir):
    if filename.endswith('.png'):
        # Construct the full path to the PNG file
        png_path = os.path.join(png_dir, filename)

        # Open the PNG image
        image = Image.open(png_path)

        # Extract text from the image using pytesseract
        text = pytesseract.image_to_string(image)

        # Construct the output file path
        output_file = os.path.join(output_dir, filename.replace('.png', '.gt.txt'))

        # Write the text to the output file
        with open(output_file, 'w') as file:
            file.write(text)

        # Close the image
        image.close()
