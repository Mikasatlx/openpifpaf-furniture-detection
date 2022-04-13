# openpifpaf_furniture
A plugin of OpenPifPaf for furniture pose detection and classification

#### Abstract

> Real-time Multi-Object Furniture Pose Detection and Classification
>
> We present a multi-object pose detection and classification method of home furniture in cluttered and occluded indoor environments.
> We generalize OpenPifPaf, a field-based method that jointly detects and forms spatio-temporal keypoint associations of a specific object, with the capacity of jointly performing detection and classification of multiple objects in a bottom-up, box-free and real-time manner. We demonstrate that our proposed method outperforms state-of-the-art furniture key-
point detection methods on two publicly available datasets (Keypoint-5 and Pascal3D+).
> We further implement a synthetic dataset to evaluate the performance when target objects have occluded viewpoints or limited resolutions. Results also show that our synthetic dataset boosts the performance of detecting real-world instances. All source codes are shared.

![Example](docs/example.png)

### Table of Contents

- [Installation](#installation)
- [Dataset](#dataset)
- [Pretrained models](#pretrained-models)
- [Interfaces](#interfaces)
- [Training](#training)
- [Prediction](#prediction)
- [Evaluation](#evaluation)
- [Project structure](#project-structure)

## Installation

We encourage to setup a virtual environment in your work space.
```
# Create a virtual environment in work_space.
mkdir work_space
cd ws_space
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
```

Clone this repository in your work space.
```
# To clone the repository in work_space using HTTPS
git clone https://github.com/Mikasatlx/openpifpaf-furniture-detection.git
cd openpifpaf-furniture-detection
```

Dependencies can be found in the `requirements.txt` file.
```
# To install dependencies
pip3 install -r requirements.txt
```

The decoder is implemented as a C++ extension. Build it before using.
```
# To buile the C++ extension
pip3 install -e .
```

This OpenPifPaf plugin is equipped with additional capacity of object classification. The required keypoint labels are also in COCO format. If you want to train or evaluate a model on your local machine, unfortunately the coco.py in the pycocotool package which is automatically installed in the virtual environment can not support loading labels with different categories. Replace it with the one provided in this repository. 
(We only change the operator "&=" in line 195 to "|=" in order to support loading labels with different categories.)

```
cp coco.py ../venv/lib/python3.6/site-packages/pycocotools/
```

Note that this step is not necessary if you train or evaluate a model on the EPFL SCITAS cluster.

This project has been tested with Python 3.6, PyTorch 1.9.0, CUDA 10.2 and OpenPifPaf 0.13.0.


## Dataset

This project uses dataset [Keypoint5](http://3dinterpreter.csail.mit.edu/), [Pascal3D+](https://cvgl.stanford.edu/projects/pascal3d.html) and our proposed synthetic dataset for training and evaluation. Addtional work has been done to transfrom the original labels into the required COCO format, and combine them together in order to train a model for real-world applications (e.g., mobile furniture indoor localization). Download the [furniture dataset]() with COCO-style labels through this link, and put it in the openpifpaf-furniture-detection folder: 


## Pretrained models

Please download the [pretrained models]() from this link.

## Interfaces

This project is implemented as an [OpenPifPaf](https://github.com/openpifpaf/openpifpaf) plugin module.
As such, it benefits from all the core capabilities offered by OpenPifPaf, and only implements the additional functions it needs.

All the commands can be run through OpenPifPaf's interface using subparsers.
Help can be obtained for any of them with option `--help`.
More information can be found in [OpenPifPaf documentation](https://openpifpaf.github.io/intro.html).


## Training

Training is done using subparser `openpifpaf.train`.

Example of training on the furniture dataset can be run with the command:
```
python3 -m openpifpaf.train \
  --dataset furniture \
  --basenet shufflenetv2k30 \
  --furniture-train-annotations ./data-realuse/annotations/realuse_train.json \
  --furniture-val-annotation ./data-realuse/annotations/realuse_val.json \
  --furniture-train-image-dir ./data-realuse/images/train \
  --furniture-val-image-dir ./data-realuse/images/val \
  --furniture-square-edge 423 \
  --momentum 0.95 \
  --b-scale 3 \
  --clip-grad-value 5 \
  --epochs 150 \
  --lr-decay 130 140 \
  --lr-decay-epochs 10 \
  --lr-warm-up-epochs 10 \
  --weight-decay 1e-5 \
  --loader-workers 16 \
  --furniture-upsample 2 \
  --furniture-extended-scale \
  --furniture-orientation-invariant 0.1 \
  --batch-size 16
```
Arguments should be modified appropriately if needed.

More information about the options can be obtained with the command:
```
python3 -m openpifpaf.train --help
```

## Prediction

Result of a single image is predicted by using subparser `openpifpaf.predict`.

Example of predicting a image using the given checkpoint can be run with the command:

```
python3 -m openpifpaf.predict docs/test_images/pascal3d/demo2.jpg \
  --checkpoint <path/to/checkpoint.pt> \
  -o docs/test_images_result/demo \
  --force-complete-pose-furniture \ (not necessary)
  --instance-threshold-furniture 0.15 \
  --seed-threshold-furniture 0.2 \
  --line-width 8 \
  --font-size 0 
```

![Prediction](docs/test_images_result/demo.png)

Arguments should be modified appropriately if needed.

To visualize all the composite fields of the 5th keypoint, add the following parameters in the command above:

```
--debug-indices cif_furniture:5 caf_furniture:5 
--save-all docs/test_images_result/debug_example
```

More information about the options can be obtained with the command:
```
python3 -m openpifpaf.eval --help
```

## Evaluation

Evaluation of a checkpoint is done using subparser `openpifpaf.eval`.

Evaluation on JAAD with all attributes can be run with the command:
```
python3 -m openpifpaf.eval \
  --output <path/to/outputs> \
  --dataset jaad \
  --jaad-root-dir <path/to/jaad/folder/> \
  --jaad-subset default \
  --jaad-testing-set test \
  --checkpoint <path/to/checkpoint.pt> \
  --batch-size 1 \
  --jaad-head-upsample 2 \
  --jaad-pedestrian-attributes all \
  --head-consolidation filter_and_extend \
  --decoder instancedecoder:0 \
  --decoder-s-threshold 0.2 \
  --decoder-optics-min-cluster-size 10 \
  --decoder-optics-epsilon 5.0 \
  --decoder-optics-cluster-threshold 0.5
```
Arguments should be modified appropriately if needed.

Using option `--write-predictions`, a json file with predictions can be written as an additional output.

Using option `--show-final-image`, images with predictions displayed on them can be written in the folder given by option `--save-all <path/to/image/folder/>`.
To also display ground truth annotations, add option `--show-final-ground-truth`.

More information about the options can be obtained with the command:
```
python3 -m openpifpaf.eval --help
```


## Project structure

The code is organized as follows:
```
openpifpaf_detection_attributes/
├── datasets/
│   ├── jaad/
│   ├── (+ common files for datasets)
│   └── (add new datasets here)
└── models/
    ├── mtlfields/
    ├── (+ common files for models)
    └── (add new models here)
```


## License

This project is built upon [OpenPifPaf](https://openpifpaf.github.io/intro.html) and shares the AGPL Licence.

This software is also available for commercial licensing via the EPFL Technology Transfer
Office (https://tto.epfl.ch/, info.tto@epfl.ch).


## Citation

If you use this project in your research, please cite the corresponding paper:
```text
@article{mordan2021detecting,
  title={Detecting 32 Pedestrian Attributes for Autonomous Vehicles},
  author={Mordan, Taylor and Cord, Matthieu and P{\'e}rez, Patrick and Alahi, Alexandre},
  journal={IEEE Transactions on Intelligent Transportation Systems (T-ITS)},
  year={2021},
  doi={10.1109/TITS.2021.3107587}
}
```


## Acknowledgements

We would like to thank Valeo for funding our work, and Sven Kreiss for the OpenPifPaf Plugin architecture.
