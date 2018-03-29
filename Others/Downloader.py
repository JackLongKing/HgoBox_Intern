import json
import os
import multiprocessing
from urllib import request
from PIL import Image
from io import BytesIO
import tqdm

# OUT_DIR = '..\\data\\train'
# JSON_FILE_PATH = '..\\data\\train.json'
# IS_TRAIN_SET = True

# OUT_DIR = '..\\data\\validation'
# JSON_FILE_PATH = '..\\data\\validation.json'
# IS_TRAIN_SET = True

OUT_DIR = '..\\data\\test'
JSON_FILE_PATH = '..\\data\\test.json'
IS_TRAIN_SET = False

CLASS_NUMBER = 128
IMAGE_SIZE = (299, 299)


def download_image(key_url):
    out_dir = OUT_DIR
    if IS_TRAIN_SET:
        (key, url, folder) = key_url
        filename = os.path.join(out_dir, str(folder).zfill(3), '{}.jpg'.format(key))
    else:
        (key, url) = key_url
        filename = os.path.join(out_dir, '{}.jpg'.format(key))

    if os.path.exists(filename):
        print('Image {} already exists. Skipping download.'.format(filename))
        return 0

    try:
        response = request.urlopen(url)
        image_data = response.read()
    except:
        print('Warning: Could not download image {} from {}'.format(key, url))
        return 1

    try:
        pil_image = Image.open(BytesIO(image_data))
    except:
        print('Warning: Failed to parse image {}'.format(key))
        return 1

    try:
        pil_image_rgb = pil_image.convert('RGB')
    except:
        print('Warning: Failed to convert image {} to RGB'.format(key))
        return 1

    try:
        pil_image_rgb = pil_image_rgb.resize(IMAGE_SIZE)
        pil_image_rgb.save(filename, format='JPEG', quality=90)
    except:
        print('Warning: Failed to save image {}'.format(filename))
        return 1

    return 0


def loader():
    os.chdir(os.getcwd())
    json_file = open(JSON_FILE_PATH, 'r')
    data_dic = json.load(json_file)
    data_list = [[] for _ in range(len(data_dic['images']))]

    for i in data_dic['images']:
        data_list[i['image_id']-1].append(i['image_id'])
        data_list[i['image_id']-1].append(i['url'][0])

    if IS_TRAIN_SET:
        for i in range(CLASS_NUMBER):
            if not os.path.exists(os.path.join(OUT_DIR, str(i).zfill(3))):
                os.mkdir(os.path.join(OUT_DIR, str(i).zfill(3)))

        for i in data_dic['annotations']:
            data_list[i['image_id']-1].append(i['label_id']-1)

    pool = multiprocessing.Pool(processes=200)
    failures = sum(tqdm.tqdm(pool.imap_unordered(download_image, data_list), total=len(data_list)))
    print('Total number of download failures:', failures)
    pool.close()
    pool.terminate()


if __name__ == '__main__':
    loader()
