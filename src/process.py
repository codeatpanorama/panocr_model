import os
from PIL import Image
import shutil
import zipfile


data_dirctory = './Data'

target_path = '/2'


def rename(sub_path):
    counter = 1
    # Iterate over all files in the directory
    for filename in os.listdir(data_dirctory+sub_path):
    # Check if the file is a PNG image
        if filename.endswith('.png') or filename.endswith('.jpg') :
            # Rename the PNG file
            old_path = os.path.join(data_dirctory+sub_path, filename)
            new_path = os.path.join(data_dirctory+target_path, f"{counter}.tif")

            png_image = Image.open(old_path)

            grayscale_image = png_image.convert('L')
            grayscale_image.save(new_path, 'TIFF')
            grayscale_image.close()

            # Construct the corresponding TXT file name
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_old_path = os.path.join(data_dirctory+sub_path, txt_filename)
            txt_new_path = os.path.join(data_dirctory+target_path, f"{counter}.gt.txt")
            shutil.copy2(txt_old_path, txt_new_path)

            # Increment the counter
            counter += 1


def convert_png_to_tiff(png_files, output_dir):
    for png_file in png_files:
        # Get the name of the image file without the extension
        image_name = os.path.splitext(os.path.basename(png_file))[0]
        
        # Open the PNG file
        png_image = Image.open(png_file)
        
        # Convert the image to TIFF format
        tiff_file = f"{image_name}.tiff"
        tiff_file_path = os.path.join(output_dir, tiff_file)
        png_image.save(tiff_file_path, 'TIFF')
        
        # Close the PNG file
        png_image.close()
        
        print(f"Converted {png_file} to {tiff_file}")


def get_png_files(dir):
    png_files = []
    for file in os.listdir(dir):
        if file.endswith('.png'):
            png_files.append(os.path.join(dir, file))
    return png_files



def copy_txt_files(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Iterate over files in the source directory
    for file_name in os.listdir(source_dir):
        # Check if the file is a text file
        if file_name.endswith('.txt'):
            # Get the full path of the source file
            source_file = os.path.join(source_dir, file_name)
            
            # Copy the file to the destination directory
            shutil.copy2(source_file, destination_dir)
            print(f"Copied {file_name} to {destination_dir}")


def create_zip(directory, zip_file):
    # Create a new ZIP file
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Iterate over files in the directory
        for root, _, files in os.walk(directory):
            for file in files:
                # Get the full path of the file
                file_path = os.path.join(root, file)
                
                # Add the file to the ZIP archive
                zipf.write(file_path, os.path.relpath(file_path, directory))
    
    print(f"Successfully created {zip_file}")

# Example usage
directory = data_dirctory + target_path
zip_file = './Data/Version2.zip'
create_zip(directory, zip_file)


#png_files = get_png_files(data_dirctory)
#convert_png_to_tiff(png_files, data_dirctory+"/1")
#copy_txt_files(data_dirctory, data_dirctory+"/1")

#rename('/mj')