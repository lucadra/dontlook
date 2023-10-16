from setuptools import setup, find_packages

setup(
    name="dontlook",
    version="0.1",
    packages=find_packages(),
        package_data={
        "dontlook": ["yolov8n-face.onnx"]
    },
    install_requires=[
        "numpy==1.26.0",
        "opencv_python==4.8.1.78",
        "tqdm==4.66.1",
        "ultralytics==8.0.196",
        "wget==3.2",
        "omegaconf==2.3.0",
        "typing-extensions==4.8.0"
    ],
    entry_points={
        'console_scripts': [
            'dontlook=dontlook.__main__:main',
        ],
    },
)
