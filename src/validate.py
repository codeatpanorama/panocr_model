import os

png_dir = "./Data/marathi_handwritten_text/tif-300-dpi"

count = 0
for png_file in os.listdir(png_dir):
    if png_file.endswith(".tif"):
        gt_file = os.path.join(png_dir, png_file.replace(".tif", ".gt.txt"))
        if not os.path.exists(gt_file):
            print(f"Missing .gt.txt file for {png_file}")
            count = count +1
        
print(f'completed successfully.{count}')