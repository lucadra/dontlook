#!/usr/bin/env python

from ultralytics import YOLO
import cv2
import wget
import os
import numpy as np
import tqdm 
import torch

MODEL_URL = 'https://github.com/akanametov/yolov8-face/releases/download/v0.0.0/yolov8n-face.pt'


def define_device() -> str:
    if torch.cuda.is_available():
        return"cuda"
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        return "mps"
    else:
        return "cpu"
    

def main():
    yolo_model_name = 'yolov8n-face.pt'
    yolo_model_path = os.path.join(os.path.expanduser('~'), yolo_model_name)

    if not os.path.isfile(yolo_model_path):
        print(f"Dowloading model from {MODEL_URL} to {yolo_model_path}...")
        wget.download(MODEL_URL, yolo_model_path)

    model = YOLO(yolo_model_path)

    images = [file for file in os.listdir() if file.endswith(('jpg', 'jpeg', 'png'))]

    if not os.path.isdir('censored'):
        os.mkdir('censored')

    device = define_device()

    if device == "cpu":
        model.model.to(device)
        model.model.eval()
        dummy_input = torch.randn(1, 3, 640, 640, device=device)
        torch.onnx.export(model.model, dummy_input, "yolov8n-face.onnx", verbose=True, opset_version=11)
        model = torch.onnx.load("yolov8n-face.onnx")


    for image in tqdm.tqdm(images, desc='Censoring images...', unit='image'):
        result = model(source=image, stream=True, show=False, save=False, save_txt=False, verbose=False, device=device)

        img = cv2.imread(image)
        image_height, image_width, _ = img.shape

        smaller_dimension = min(image_height, image_width)
        kernel_size = int(smaller_dimension / 5)
        
        if kernel_size % 2 == 0:
            kernel_size += 1

        blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

        for box in list(result)[0].boxes: 
            bounding_box = box.xyxyn.tolist()[0]

            norm_x0 = bounding_box[0] * image_width
            norm_y0 = bounding_box[1] * image_height
            norm_x1 = bounding_box[2] * image_width
            norm_y1 = bounding_box[3] * image_height

            mask = np.zeros_like(img, dtype=np.uint8)

            mask = cv2.rectangle(mask, (int(norm_x0), int(norm_y0)), (int(norm_x1), int(norm_y1)), (255, 255, 255), -1)
            out = np.where(mask==(0, 0, 0), img, blurred_img)
            img = out

        out_path = os.path.join('censored', image)
        cv2.imwrite(out_path, out)