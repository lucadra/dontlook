#!/usr/bin/env python
from ultralytics import YOLO
import cv2
import os
import tqdm 
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import pkg_resources

logging.disable(logging.CRITICAL)
MODEL_PATH = pkg_resources.resource_filename('dontlook', 'yolov8n-face.onnx')


def main():
    model = YOLO(MODEL_PATH)
    file_names = [file for file in os.listdir() if file.endswith(('jpg', 'jpeg', 'png'))]

    with ThreadPoolExecutor() as executor:
        images = list(executor.map(cv2.imread, file_names))

    results = model(images, task="detect", stream=True, show=False, save=False, save_txt=False, verbose=False, imgsz=160)

    data = zip(file_names, images, results)

    if not os.path.isdir('censored'):
        os.mkdir('censored')

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(censor_image, file_path, image, result) for file_path, image, result in data]
        for future in tqdm.tqdm(as_completed(futures), total=len(futures)):
            future.result()


def censor_image(file_name, img, result):
    out = img
    image_height, image_width, _ = img.shape

    smaller_dimension = min(image_height, image_width)
    kernel_size = int(smaller_dimension / 20)
        
    if kernel_size % 2 == 0:
        kernel_size += 1

    for box in result.boxes:
        bounding_box = box.xyxyn.tolist()[0]

        norm_x0 = int(bounding_box[0] * image_width)
        norm_y0 = int(bounding_box[1] * image_height)
        norm_x1 = int(bounding_box[2] * image_width)
        norm_y1 = int(bounding_box[3] * image_height)

        out[norm_y0:norm_y1, norm_x0:norm_x1] = cv2.medianBlur(img[norm_y0:norm_y1, norm_x0:norm_x1], kernel_size)
        img = out

    out_path = os.path.join('censored', file_name)
    cv2.imwrite(out_path, out)