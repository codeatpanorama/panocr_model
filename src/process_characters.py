import os
from PIL import Image, ImageOps
import shutil
import zipfile


data_dirctory = './Data'

char_directory="/characters"
target_path = '/3'

def getMap():
    return {
        "character_1_ka": "क",
        "character_2_kha": "ख",
        "character_3_ga": "ग",
        "character_4_gha": "घ",
        "character_5_kna": "ङ",
        "character_6_cha": "च",
        "character_7_chha": "छ",
        "character_8_ja": "ज",
        "character_9_jha": "झ",
        "character_10_yna": "ञ",
        "character_11_taamatar": "ट",
        "character_12_thaa":"ठ",
        "character_13_daa": "ड",
        "character_14_dhaa": "ढ",
        "character_15_adna": "ण",
        "character_16_tabala": "त",
        "character_17_tha": "थ",
        "character_18_da": "द",
        "character_19_dha": "ध",
        "character_20_na": "न",
        "character_21_pa": "प",
        "character_22_pha": "फ",
        "character_23_ba": "ब",
        "character_24_bha": "भ",
        "character_25_ma": "म",
        "character_26_yaw": "य",
        "character_27_ra": "र",
        "character_28_la": "ल",
        "character_29_waw": "व",
        "character_30_motosaw": "श",
        "character_31_petchiryakha": "ष",
        "character_32_patalosaw": "स",
        "character_33_ha": "ह",
        "character_34_chhya": "क्ष",
        "character_35_tra": "त्र",
        "character_36_gya": "ज्ञ",

        "digit_0": "०",
        "digit_1": "१",
        "digit_2": "२",
        "digit_3": "३",
        "digit_4": "४",
        "digit_5": "५",
        "digit_6": "६",
        "digit_7": "७",
        "digit_8": "८",
        "digit_9": "९",
    }

def getDir():
    return  os.listdir(data_dirctory+char_directory) #if os.path.isdir(os.path.join(data_dirctory, name))]

def get_png_files(dir):
    png_files = []
    for file in os.listdir(dir):
        if file.endswith('.png'):
            png_files.append(os.path.join(dir, file))
    return png_files

def generateTiff():
    directories = getDir()
    map = getMap()
    counter = 1
    for directory in directories:
        print(f"dicrectory: {directory}")
        character_directory_path = data_dirctory+char_directory+"/"+directory
        files = get_png_files(character_directory_path)
        for file in files:
            print(f"file: {file}")
            if file.endswith('.png') or file.endswith('.jpg'):
                char = map[directory]
                old_path = os.path.join(file)
                new_path = os.path.join(data_dirctory+target_path, f"{char}-{counter}.tif")
                png_image = Image.open(old_path)

                inverted_image = ImageOps.invert(png_image)
                inverted_image.save(new_path, 'TIFF')
                tif_image = Image.open(new_path)
                tif_image.info['dpi'] =(300, 300)
                tif_image.save(new_path)


                new_path_file = os.path.join(data_dirctory+target_path, f"{char}-{counter}.gt.txt")
                file = open(new_path_file, 'w')
                # Write content to the file
                file.write(char)
                # Close the file
                file.close()
                counter = counter+1


#generateTiff()

def rename(sub_path, prefix):
    counter = 1
    # Iterate over all files in the directory
    for filename in os.listdir(data_dirctory+sub_path):
    # Check if the file is a PNG image
        if filename.endswith('.png') or filename.endswith('.jpg') :
            # Rename the PNG file
            old_path = os.path.join(data_dirctory+sub_path, filename)
            new_path = os.path.join(data_dirctory+target_path, f"{prefix}-{counter}.tif")
            png_image = Image.open(old_path)

            grayscale_image = png_image.convert('L')
            grayscale_image_info = grayscale_image.info.copy()
            grayscale_image_info['dpi'] = (300, 300)

            grayscale_image.save(new_path, 'TIFF')
            grayscale_image.close()

            # Construct the corresponding TXT file name
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_old_path = os.path.join(data_dirctory+sub_path, txt_filename)
            txt_new_path = os.path.join(data_dirctory+target_path, f"{prefix}-{counter}.gt.txt")
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


def get_tiff_dpi(tiff_file):
    image = Image.open(tiff_file)
    dpi = image.info.get('dpi')
    image.close()
    return dpi

'''
# Example usage
tiff_file = './Data/2/1.tif'
dpi = get_tiff_dpi(tiff_file)
if dpi:
    x_dpi, y_dpi = dpi
    print(f"DPI of {tiff_file}: X={x_dpi}, Y={y_dpi}")
else:
    print(f"No DPI information found in {tiff_file}")
'''

# Example usage
directory = data_dirctory + target_path
zip_file = './Data/Version3.zip'
create_zip(directory, zip_file)


#png_files = get_png_files(data_dirctory)
#convert_png_to_tiff(png_files, data_dirctory+"/1")
#copy_txt_files(data_dirctory, data_dirctory+"/1")

#rename('/mj', 'mj')