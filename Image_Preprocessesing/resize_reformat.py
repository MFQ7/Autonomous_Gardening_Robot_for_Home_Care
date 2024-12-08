from PIL import Image, ImageOps
import os
import pillow_heif

pillow_heif.register_heif_opener()

def jpg_to_jpeg(old_path, output_path, base_filename, start_index=1, resize_to=(256, 256)):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    files = [f for f in os.listdir(old_path) if f.lower().endswith(('.jpg', '.heic'))]
    index = start_index

    for file in files:
        try:
            file_path = os.path.join(old_path, file)
            image = Image.open(file_path)
            if resize_to:
                image = ImageOps.fit(image, resize_to, Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            new_filename = f"{base_filename}_{index}.jpeg"
            full_output_path = os.path.join(output_path, new_filename)
            image.save(full_output_path, "JPEG")
            print(f"Converted and saved {file} as {new_filename}")
            index += 1
        except Exception as e:
            print(f"Failed to process {file}: {str(e)}")

def convert_all_folders(base_directory, output_directory, categories):
    for category in categories:
        old_dir = os.path.join(base_directory, category)
        output_dir = os.path.join(output_directory, category.replace(' ', '_'))
        base_filename = category.replace(' ', '_')

        if not os.path.exists(old_dir):
            print(f"Category folder '{category}' not found. Skipping.")
            continue
        jpg_to_jpeg(old_dir, output_dir, base_filename)
base_directory = "/Users/mohammedalqadda/Autonomous_Gardening_Robot_for_Home_Care/Machine Learning/temp/"
output_directory = "/Users/mohammedalqadda/Autonomous_Gardening_Robot_for_Home_Care/Machine Learning/test"
categories = ["Guldawari"]
convert_all_folders(base_directory, output_directory, categories)