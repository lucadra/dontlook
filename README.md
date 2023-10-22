# DontLook: Automated Face Censorship Tool

DontLook is a Python-based command line tool designed to automatically detect and censor faces in a collection of images. 

|Original Image| Censored with dontlook |
|--|--|
| [![frassica7.jpg](https://i.postimg.cc/c175fQ9M/frassica7.jpg)](https://postimg.cc/9zMphqjr) | [![frassica7.jpg](https://i.postimg.cc/JhJQMLSc/frassica7.jpg)](https://postimg.cc/qtJKx9Jz) |


## Prerequisites
The tool requires Python to run. If you don't have Python installed, you can download and install it from [Python's official website](https://www.python.org/downloads/).

## Installation
Run the following command to install DontLook from the GitHub repository:

    pip3 install git+https://github.com/lucadra/dontlook.git

## Usage

 1. Put all the images you want to censor in a folder
   [![Screenshot-2023-10-21-at-19-39-00.jpg](https://i.postimg.cc/SNv5Km1w/Screenshot-2023-10-21-at-19-39-00.jpg)](https://postimg.cc/HVb3Z1g2)
 2. Open a terminal window at that folder:
[![Screenshot-2023-10-21-at-19-44-26.jpg](https://i.postimg.cc/8CVZFcRn/Screenshot-2023-10-21-at-19-44-26.jpg)](https://postimg.cc/xXtvh0FK)
 3. Run the "dontlook" command from the terminal
 [![Screenshot-2023-10-21-at-19-41-16.png](https://i.postimg.cc/6phMvwMW/Screenshot-2023-10-21-at-19-41-16.png)](https://postimg.cc/SnJL0003)
 4. Censored images will be saved to a folder named "censored" inside the folder you ran the command at 
 [![Screenshot-2023-10-21-at-19-52-44.png](https://i.postimg.cc/rsPkcxtH/Screenshot-2023-10-21-at-19-52-44.png)](https://postimg.cc/7J0cnC91)

## How It Works
DontLook employs the YOLOv8 model for face detection. Upon detecting a face, the tool applies a median blur to the face region, ensuring anonymity.

## License
DontLook is licensed under the GPL 3.0 License. For more information, refer to the LICENSE file.

## Contributing
Contributions, issues, and feature requests are welcome. For significant changes, kindly open an issue first to discuss your proposed modifications.

## Acknowledgements
Face detection with YOLO is powered by the [Ultralytics YOLO implementation](https://github.com/ultralytics/ultralytics)
