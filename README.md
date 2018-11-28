# Photogrammetry-based data synthesis for object-to-model deep learning

## About the project

The availability of large image data sets has been a crucial factor in the recent success of deep learning-based classification and detection methods. Yet, while data sets for everyday objects (e.g. ImageNet, Microsoft Coco) are widely available, data for specific use-cases (e.g. identifying packaged products in a warehouse) remains scarce. In such cases, the data sets have to be created from scratch. 

We present a novel framework for using photogrammetry-based data synthesis to create an end-to-end deep learning pipeline, beginning with real-world objects and culminating in a trained model.

Our method is based on the generation of training images from 3D models obtained by applying photogrammetry to photographs of real-world objects, generally using less than 40 images per object. Using 100k synthetic images, an InceptionV3 convolutional neural network (CNN) was trained, which achieved accuracy of 96\% on a separately acquired test set of real images. The image generation process supports automatic pixel annotation. This eliminates the prohibitively expensive manual annotation typically required for detection tasks. Based on this readily available data, a one-stage RetinaNet detector was trained on the synthetic, annotated images to produce a detector that can accurately localize and classify the specimen products in real-time.

## Components

This repository contains all the components required to implement the pipeline explained in the paper. It also includes two front-end implementations, a Flask Web Server and an iPhone App, allowing users to perform detection/classification using a trained model. 

- Rendering API 
- Training pipeline
- Evaluation
- Flask server
- iPhone App

**The short demo video can be found [here](https://vimeo.com/277194444)**

### Production Recognition (Classification)
![](/demo_images/classification.gif)

### Production Recognition (Detection)
![](/demo_images/detection.gif)

## Installation & Dependencies

### Activate correct CUDA version to link TF to GPU
create a file in your home directory called .bash_profile with content and save:

```
if [ -f /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh ]
then
   . /vol/cuda/8.0.61-cudnn.7.0.2/setup.sh
fi
```
(The above code is for Imperial Collge London Lab PC environment)


then log out and log in again or restart bash.

### Create Virtual Environment

The first step is to install *virtualenv*.

```pip install virtualenv```

The next is to initialise the virtual environment with 

```virtualenv -p python3 venv```

Get into the virtualenv

```source venv/bin/activate```

Install all the dependencies within the virtual environment.

```pip install -r requirements.txt```

### How to run each program

### Integrated Pipeline: main.py

provide paths to validation and test set, currently pointing to the example
folders provided with this repository.

provide the path to your blender installation in 
```bl_path = 'PATH/TO/BLENDER/INSTALLATION'```

Choose all parameters in main.py for rendering and neural network training,
save and run
```
$python main.py
```

### Rendering API

README can be found in  `/src/rendering`.

### Training and Evaluation

README can be found in  `/kerasmodels`.

### iPhone App

README can be found in  `/iPhone_app`.

### Flask

README can be found in  `/flask_webserver`.


## Project Team Members <a name="project-team-members"></a>

Should you have any questions regarding how to run the above, please contact one of the project team members.

* [kk3317](https://gitlab.doc.ic.ac.uk/kk3317) -
**Kiyohito Kunii** &lt;kk3317@imperial.ac.uk&gt;
* [mzw17](https://gitlab.doc.ic.ac.uk/mzw17) -
**Max Baylis** &lt;mzw17@imperial.ac.uk&gt;
* [mgb17](https://gitlab.doc.ic.ac.uk/mgb17) -
**Matthew Wong** &lt;mgb@imperial.ac.uk&gt;
* [who11](https://gitlab.doc.ic.ac.uk/who11) -
**Ong Wai Hong** &lt;who11@imperial.ac.uk&gt;
* [pk3014](https://gitlab.doc.ic.ac.uk/pk3014) -
**Pavel Kroupa** &lt;pk3014@imperial.ac.uk&gt;
* [sk5317](https://gitlab.doc.ic.ac.uk/sk5317) -
**Swen Koller** &lt;sk5317@imperial.ac.uk&gt;

