from PIL import Image
import os

# Load the image
def get_list_of_images_path(image_folder):
    list_of_image = []
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        if os.path.isfile(file_path):  # Ensures it's a file, not a directory
            list_of_image.append(file_path)
    return list_of_image

def get_list_of_images_data(images_path: list):
    images = []
    for image_path in images_path:
        image = Image.open(image_path)
        images.append(image)
    return images

def get_list_of_images_resized(images: list, new_size: tuple):
    images_resized = []
    images_datas = []
    for image_data in images:
        image = image_data.resize(new_size, Image.LANCZOS)
        # Convert to RGBA and remove transparent background (if any)
        image = image.convert("RGBA")
        datas = image.getdata()
        images_resized.append(image)
        images_datas.append(datas)
    return images_resized, images_datas

def clean_image(image_data):
    # Define a new image data list with transparent background removed
    new_data = []
    for item in image_data:
        # If the pixel is transparent, replace it with a fully transparent pixel
        if item[3] == 0:
            new_data.append((255, 255, 255, 0))  # Transparent white
        else:
            new_data.append(item)
    return new_data

def change_image_data(images_resized: list, images_data: list):
    images_new = []
    for i in range(len(images_resized)):
        image_resized = images_resized[i]
        image_data = images_data[i]

        new_data = clean_image(image_data)
        image_resized.putdata(new_data)
        images_new.append(image_resized)
    return images_new

def save_images(images : list, images_path : list, output_path : str, format : str):
    for i in range(len(images_path)): 
        image = images[i]
        input_image_path = images_path[i]
        image_file_name = os.path.basename(input_image_path)
        output_image_directory = output_path
        output_image_path = os.path.join(output_image_directory, image_file_name)
        print(f"output file : {output_image_path}")
        image.save(output_image_path, format)

def resize_image(input_image_folder = f"{os.getcwd()}/resources/input_images", new_size = (1240, 1240), format="PNG", output_image_folder = f"{os.getcwd()}/resources/output_images"):
    images_path = get_list_of_images_path(image_folder=input_image_folder)
    images = get_list_of_images_data(images_path=images_path)
    images_resized, images_data = get_list_of_images_resized(images=images, new_size=new_size)
    images_new = change_image_data(images_resized, images_data)
    save_images(images=images_new, images_path=images_path, output_path=output_image_folder, format=format)

resize_image()