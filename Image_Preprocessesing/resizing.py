import os
from PIL import Image

def resize_images_in_directory(directory, target_size=(256,256)):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpeg', '.jpg', '.png')):
            img_path = os.path.join(directory, filename)
            try:
                with Image.open(img_path) as img:
                    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                    img_resized.save(img_path)
                    print(f"Resized and saved {filename} at {img_path}")
            except Exception as e:
                print(f"Error resizing {filename}: {e}")

def resize_all_categories(base_directory, target_size=(256, 256)):
    categories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    for category in categories:
        directory = os.path.join(base_directory, category)
        print(f"Resizing images in {directory} to {target_size}...")
        resize_images_in_directory(directory, target_size)
        print(f"Completed resizing images in {category}.")

base_directory = "/Users/mohammedalqadda/Autonomous_Gardening_Robot_for_Home_Care/Machine Learning/trainable"
resize_all_categories(base_directory, target_size=(256,256))

