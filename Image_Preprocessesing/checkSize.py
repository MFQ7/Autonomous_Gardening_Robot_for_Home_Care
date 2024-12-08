import os
from PIL import Image

def check_image_sizes_and_average(directory):
    widths = []
    heights = []
    same_size = True
    first_size = None

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpeg', '.jpg', '.png')):
            img_path = os.path.join(directory, filename)
            with Image.open(img_path) as img:
                size = img.size
                widths.append(size[0])
                heights.append(size[1])
                if first_size is None:
                    first_size = size
                elif first_size != size:
                    same_size = False


    average_width = sum(widths) / len(widths) if widths else 0
    average_height = sum(heights) / len(heights) if heights else 0
    average_size = (average_width, average_height)

    return same_size, average_size

def check_all_folders(base_directory):
    categories = ['Coleus_Blumei', 'Green_Pepper', 'Guldawari']
    results = {}
    for category in categories:
        directory = os.path.join(base_directory, category)
        same_size, average_size = check_image_sizes_and_average(directory)
        results[category] = {'Same Size': same_size, 'Average Size': average_size}
        print(f"{category}: Same Size - {same_size}, Average Size - {average_size}")
    return results

base_directory = "/Users/mohammedalqadda/Autonomous_Gardening_Robot_for_Home_Care/Machine Learning/validation"  # Update this path to where your 
check_all_folders(base_directory)
