# Labwork 2

## Task

Configure and run image classification system based on convolutional neural networks.

## Theory and App architecture

Full disclosure, some code is reused from the
[old project](https://github.com/sunDalik/vk-bot/blob/master/img2msg/__init__.py), which I contributed to.
It is VK bot that uses image recognition to classify images sent to the group chat and react to them
accordingly.

So, basic foundation (for example `Xception` model with `imagenet` weights) is determined by this code,
since I decided to reuse some parts of it because of deadline pressure.

Lets start with model itself. In this project I use [`Xception`](https://keras.io/api/applications/xception/) model.
According to [Keras docs](https://keras.io/api/applications/) this model shows best results for both top-1 and top-5
accuracy. I used Xception with weights pretrained on [`imagenet`](https://www.image-net.org/about.php) dataset.

Next important question is what dataset we are using to validate this model. Lab task specified that we need to use
any 50 images. I was too lazy to manually construct dataset and more importantly label it. So I decided to use
official `imagenet` [ILSVRC dataset](https://www.kaggle.com/c/imagenet-object-localization-challenge/data)
(all 167Gb of it).

This dataset contains of 3 subsets: test, train and validation. In this work I used latter one, since test does
not contain labels, and we cannot use training dataset for obvious reasons, since we are using `imagenet` weights.
Validation dataset contains of 50000 images. We are using whole dataset, making data count 1000 bigger than one
recommended to be used in this labwork.

Let's discuss the way validation subset is mapped. Images itself are living in the `ILSVRC/Data/CLS-LOC/val`
directory. The labes for them is in the `ILSVRC/Annotations/CLS-LOC/val`. Labels is stored in the `.xml` files
with name matching the name of the image. Sample format:

```xml
<annotation>
  <folder>val</folder>
  <filename>ILSVRC2012_val_00026567</filename>
  <source>
    <database>ILSVRC_2012</database>
  </source>
  <size>
    <width>500</width>
    <height>375</height>
    <depth>3</depth>
  </size>
  <segmented>0</segmented>
  <object>
    <name>n02256656</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>163</xmin>
      <ymin>200</ymin>
      <xmax>246</xmax>
      <ymax>269</ymax>
    </bndbox>
  </object>
  <object>
    <name>n02256656</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
      <xmin>147</xmin>
      <ymin>43</ymin>
      <xmax>409</xmax>
      <ymax>329</ymax>
    </bndbox>
  </object>
</annotation
```

Objects on the picture is stored in the `object->name`. What we see here is `ILSVRC2012_ID`. How do we find mappings to
human readable categories? Well, the forums mentioned some `map_clsloc.txt` file. After googling I found this file in some
[git gist](https://gist.github.com/aaronpolhamus/964a4411c0906315deb9f4a3723aac57) and it seemed to work perfectly for all
1000 classes we used in Xception.

Now lets discuss the app architecture itself. After initializing `Xception` model we define main functions.

* `parse_classes` : this function does simple thing. It loads `map_clsloc.txt` mentioned above and creates the dictionary
  with `ILSVRC2012_ID` as key and human readable class name as value.
* `get_class_for_image` : this function takes the image name, finds corresponding `.xml` with labels, parses it and returns
dict with `ILSVRC2012_ID` as key and corresponding value from `map_clsloc` as value.
* `get_predictions` : this function is where the magic happens. Firstly, we load image and resize it to 299x299, since it is
size that `Xception` needs. Than we feed it to the Xception and get top-5 predictions with probabilities. Returns list of
tuples `(ILSVRC2012_ID, class_name, probability)`.
* `process_image` : main function. Takes image name as argument, calls `get_class_for_image` to get expected classes of
objects in picture, calls `get_predictions` to get predicted classes for image, and then compares expected `ILSVRC2012_ID`'s
to predicted ones to calculate whether we got right top-1 and top-5. Returns tuple `(is_top1, is_top5)`.
* Main script is pretty straigtforward. We iterate over 50000 input images and call `process_image` on every one of them.
Then we count all images and top1 and top5 success counts to calculate percentages.

## Conserns and limitations

1. We use CPU implementation and not GPU one since I have AMD GPU, and Tensorflow does not support it as for now. See
`.ipynb` for details.
2. Elephant in the room. During the run I used code with my stupid mistake:

![image](https://github.com/johnny-keker/computer-vision/assets/39794543/6acd9e52-0ef9-4c2c-9809-fe7ab8979435)

However, luckily for us, it only affects the calculation of probability percentages, and thanks to extensive logging I
was able to get results anyway, yay!:

![image](https://github.com/johnny-keker/computer-vision/assets/39794543/0920897a-541e-45fa-a3ec-36cc42533d4b)

3. I had to use `python 2.7` since this labwork is based on my previous work, and I couldn't get it to work with python 3,
looks like they broken tensorflow backend for keras there, or at least significally changed it. And deadline are coming,
so no cool features like f-strings and type annotations for us, sorry:(

## Results

The run took ~1h on Ryzen 9 5900X.

* `top 1` : 38762, ~77.52%
* `top 5` : 46876, ~93.75%

This results is really close to [Keras docs](https://keras.io/api/applications/), so looks like they are valid.

## Conclusions

In this labwork I configured and used image recognition neural network on large datased and compared results
to documentation. You can see the whole logs [here](https://raw.githubusercontent.com/johnny-keker/computer-vision/master/lab2/artifacts/output.log).

References is mentioned in the readme text as clickable liks.
