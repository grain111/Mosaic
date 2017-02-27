import glob, os, math, sys
from PIL import Image

def calc_dist(a,b):
    """ This function calculates distance betwen two points in space. "a" and "b" are tuples."""
    if isinstance(a, int):
        dist = math.sqrt((b - a)**2)
    elif len(a) == len(b):
        if len(a) == 3:
            dist = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2)
        if len(a) == 2:
            dist = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    else:
        return None

    return dist

def load_source(filename, SCL, MODE):
    """ This function loads the source images and down scales it. """
    print("Started loading source image.")
    path = "data\\" + filename
    image_path = glob.glob(path)[0]
    im = Image.open(image_path)
    if MODE == "GS":
        im = im.convert(mode="L")
    print("Finished loading source image.")
    return im.resize((int(im.width/SCL), int(im.height/SCL)))

def get_list_of_paths():
    print("Getting list of paths.")
    return glob.glob("data\photos\*.jpg")

def clear_data():
    print("Started erasing existing data.")
    list_of_paths = glob.glob("data\photos\*.jpg")
    if len(list_of_paths) != 0:
        for path in list_of_paths:
            os.remove(path)
    print("Finished erasing existing data.")

def handle_data(folder_name, SIZE, MODE):
    """ This function loads, crops, downscales and converts input data. """

    clear_data()
    print("Started data handeling.")
    path = "data\photos\\" + folder_name + "\*.jpg"
    list_of_paths = glob.glob(path)
    n = 0
    for path in list_of_paths:
        photo = Image.open(path)
        min_dim = min(photo.width, photo.height)

        lft = int((photo.width/2)-(min_dim/2))
        rgt = int((photo.width/2)+(min_dim/2))
        up = int((photo.height/2)-(min_dim/2))
        down = int((photo.height/2)+(min_dim/2))

        photo = photo.crop((lft, up, rgt, down))
        photo = photo.resize((SIZE,SIZE))
        if MODE == "GS":
            photo = photo.convert(mode="L")
        photo.save("data\\photos\\photo" + str(n) + ".jpg", "JPEG")
        n += 1
    print("Finished data handeling.")

def get_data_color(list_of_paths):

    print("Started data processing.")
    photo_color = []

    for path in list_of_paths:
        photo = Image.open(path)

        reds = 0
        greens = 0
        blues = 0

        for x in range(0, photo.width):
            for y in range(0, photo.height):
                RGB = photo.getpixel((x,y))
                reds += RGB[0]
                greens += RGB[1]
                blues += RGB[2]

        no_pix = photo.width * photo.height
        red = int(reds / no_pix)
        green = int(greens / no_pix)
        blue = int(blues / no_pix)
        photo_color.append((red, green, blue))

    print("Finished data processing.")
    return photo_color

def get_data_brightness(list_of_paths):

    print("Started data processing.")
    photo_brit = []

    for path in list_of_paths:
        photo = Image.open(path)
        brit = 0
        for x in range(0, photo.width):
            for y in range(0, photo.height):
                brit += photo.getpixel((x,y))

        no_pix = photo.width * photo.height
        a_brit = int(brit / no_pix)
        photo_brit.append(a_brit)

    return photo_brit

def get_source_pixel_data(im):
    data = []
    for x in range(0, im.width):
        for y in range(0, im.height):
            RGB = im.getpixel((x,y))
            data.append(RGB)

    print("Finished data processing.")
    return data

def match_data(data, source_data, list_of_paths, MODE):

    print("Started matching data.")
    matched_photos = []
    copy_list = list_of_paths
    copy_data = data

    for source_pixel in source_data:
        distance = []
        for photo in copy_data:
            distance.append(calc_dist(source_pixel, photo))
        index = distance.index(min(distance))
        matched_photos.append(copy_list[index])

        if MODE == "U":
            copy_list.pop(index)
            copy_data.pop(index)

    print("Finished matching data.")
    return matched_photos

def assemble_image(im, matched_data, SIZE, MODE):

    print("Started data assemble.")
    if MODE == "GS":
        out = Image.new("L", (im.width*SIZE, im.height*SIZE))
    if MODE == "COLOR":
        out = Image.new("RGB", (im.width*SIZE, im.height*SIZE))

    n = 0
    for x in range(0, im.width):
        for y in range(0, im.height):
            photo = Image.open(matched_data[n])
            out.paste(photo, (SIZE*x,SIZE*y))
            n += 1

    print("Finished data assemble.")
    return out

def main():
    SCL = 70
    SIZE = 300
    MODE = "GS" # GS -> Greyscale, COLOR -> color
    MODE2 = "U" # U -> no same photos R-> phots may repeat

    im = load_source("kasia.jpg", SCL, MODE)
    handle_data("RAW", SIZE, MODE)
    list_of_paths = get_list_of_paths()

    if MODE2 == "U":
        if len(list_of_paths) - (im.width * im.height) < 0:
            print("ERROR: Not enough photos!")
            sys.exit()

    if MODE == "GS":
        data = get_data_brightness(list_of_paths)
    if MODE == "COLOR":
        data = get_data_color(list_of_paths)

    source_data = get_source_pixel_data(im)
    matched_data = match_data(data, source_data, list_of_paths, MODE2)
    output_image = assemble_image(im, matched_data, SIZE, MODE)

    output_image.save("output.jpg")

    print("DONE!")

main()
