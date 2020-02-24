
# Model training
## Data preprocess
pervious files are saved in `Data_preprocess`folder. But we choose another technics thus they are useless now.

## Model training
In this part, transfer learning is used

### basic models
Xception, MobileNetV2, VGG19, InceptionV3, InceptionResNetV2 are used. All are pre-trained by 'ImageNet' and are loaded from [Keras Application](https://keras.io/applications/) in `training_part/util.py` 

### Load data
`DataImageGenerator.flow_from_directory` from [Keras Image Preprocess](https://keras.io/preprocessing/image/) are used to load data

### Train

run `python modelTraining.py` or run it from IDE. Please edit data path before running. Default is `Cat VGG19`, be free to edit. 

The `modelTraining.py` will output accuracy & loss with `.cvs` and model file with `.h5` and loss & accuracy plot with `.png` to `models` folder

### Model structure:

```
.
├── README
├── Reference
├── coding
│   ├── Data_preprocess
│   │   ├── EmotionList.txt
│   │   ├── count_img.py
│   │   ├── crawler_image.py
│   │   ├── extract_to_csv.py
│   │   └── read_csv.py
│   └── training_part
│       ├── const.py
│       ├── modelTraining.py
│       └── util.py
├── faceDetectors
└── models

```
 	
