#!/usr/bin/env python
# coding: utf-8

# ##### Copyright 2018 The TensorFlow Authors.

# In[1]:


#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# In[2]:


#@title MIT License
#
# Copyright (c) 2017 François Chollet
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


# # Basic classification: Classify images of clothing

# <table class="tfo-notebook-buttons" align="left">
#   <td>
#     <a target="_blank" href="https://www.tensorflow.org/tutorials/keras/classification"><img src="https://www.tensorflow.org/images/tf_logo_32px.png" />View on TensorFlow.org</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/keras/classification.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://github.com/tensorflow/docs/blob/master/site/en/tutorials/keras/classification.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
#   </td>
#   <td>
#     <a href="https://storage.googleapis.com/tensorflow_docs/docs/site/en/tutorials/keras/classification.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download notebook</a>
#   </td>
# </table>

# This guide trains a neural network model to classify images of clothing, like sneakers and shirts. It's okay if you don't understand all the details; this is a fast-paced overview of a complete TensorFlow program with the details explained as you go.
# 
# This guide uses [tf.keras](https://www.tensorflow.org/guide/keras), a high-level API to build and train models in TensorFlow.

# In[3]:


# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)


# ## Import the Fashion MNIST dataset

# This guide uses the [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) dataset which contains 70,000 grayscale images in 10 categories. The images show individual articles of clothing at low resolution (28 by 28 pixels), as seen here:
# 
# <table>
#   <tr><td>
#     <img src="https://tensorflow.org/images/fashion-mnist-sprite.png"
#          alt="Fashion MNIST sprite"  width="600">
#   </td></tr>
#   <tr><td align="center">
#     <b>Figure 1.</b> <a href="https://github.com/zalandoresearch/fashion-mnist">Fashion-MNIST samples</a> (by Zalando, MIT License).<br/>&nbsp;
#   </td></tr>
# </table>
# 
# Fashion MNIST is intended as a drop-in replacement for the classic [MNIST](http://yann.lecun.com/exdb/mnist/) dataset—often used as the "Hello, World" of machine learning programs for computer vision. The MNIST dataset contains images of handwritten digits (0, 1, 2, etc.) in a format identical to that of the articles of clothing you'll use here.
# 
# This guide uses Fashion MNIST for variety, and because it's a slightly more challenging problem than regular MNIST. Both datasets are relatively small and are used to verify that an algorithm works as expected. They're good starting points to test and debug code.
# 
# Here, 60,000 images are used to train the network and 10,000 images to evaluate how accurately the network learned to classify images. You can access the Fashion MNIST directly from TensorFlow. Import and load the Fashion MNIST data directly from TensorFlow:

# In[4]:


fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


# Loading the dataset returns four NumPy arrays:
# 
# * The `train_images` and `train_labels` arrays are the *training set*—the data the model uses to learn.
# * The model is tested against the *test set*, the `test_images`, and `test_labels` arrays.
# 
# The images are 28x28 NumPy arrays, with pixel values ranging from 0 to 255. The *labels* are an array of integers, ranging from 0 to 9. These correspond to the *class* of clothing the image represents:
# 
# <table>
#   <tr>
#     <th>Label</th>
#     <th>Class</th>
#   </tr>
#   <tr>
#     <td>0</td>
#     <td>T-shirt/top</td>
#   </tr>
#   <tr>
#     <td>1</td>
#     <td>Trouser</td>
#   </tr>
#     <tr>
#     <td>2</td>
#     <td>Pullover</td>
#   </tr>
#     <tr>
#     <td>3</td>
#     <td>Dress</td>
#   </tr>
#     <tr>
#     <td>4</td>
#     <td>Coat</td>
#   </tr>
#     <tr>
#     <td>5</td>
#     <td>Sandal</td>
#   </tr>
#     <tr>
#     <td>6</td>
#     <td>Shirt</td>
#   </tr>
#     <tr>
#     <td>7</td>
#     <td>Sneaker</td>
#   </tr>
#     <tr>
#     <td>8</td>
#     <td>Bag</td>
#   </tr>
#     <tr>
#     <td>9</td>
#     <td>Ankle boot</td>
#   </tr>
# </table>
# 
# Each image is mapped to a single label. Since the *class names* are not included with the dataset, store them here to use later when plotting the images:

# In[5]:


class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


# ## Explore the data
# 
# Let's explore the format of the dataset before training the model. The following shows there are 60,000 images in the training set, with each image represented as 28 x 28 pixels:

# In[6]:


train_images.shape


# Likewise, there are 60,000 labels in the training set:

# In[7]:


len(train_labels)


# Each label is an integer between 0 and 9:

# In[8]:


train_labels


# There are 10,000 images in the test set. Again, each image is represented as 28 x 28 pixels:

# In[9]:


test_images.shape


# And the test set contains 10,000 images labels:

# In[10]:


len(test_labels)


# ## Preprocess the data
# 
# The data must be preprocessed before training the network. If you inspect the first image in the training set, you will see that the pixel values fall in the range of 0 to 255:

# In[11]:


plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()


# Scale these values to a range of 0 to 1 before feeding them to the neural network model. To do so, divide the values by 255. It's important that the *training set* and the *testing set* be preprocessed in the same way:

# In[12]:


train_images = train_images / 255.0

test_images = test_images / 255.0


# To verify that the data is in the correct format and that you're ready to build and train the network, let's display the first 25 images from the *training set* and display the class name below each image.

# In[13]:


plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()


# ## Build the model
# 
# Building the neural network requires configuring the layers of the model, then compiling the model.

# ### Set up the layers
# 
# The basic building block of a neural network is the *layer*. Layers extract representations from the data fed into them. Hopefully, these representations are meaningful for the problem at hand.
# 
# Most of deep learning consists of chaining together simple layers. Most layers, such as `tf.keras.layers.Dense`, have parameters that are learned during training.

# In[14]:


model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10)
])


# The first layer in this network, `tf.keras.layers.Flatten`, transforms the format of the images from a two-dimensional array (of 28 by 28 pixels) to a one-dimensional array (of 28 * 28 = 784 pixels). Think of this layer as unstacking rows of pixels in the image and lining them up. This layer has no parameters to learn; it only reformats the data.
# 
# After the pixels are flattened, the network consists of a sequence of two `tf.keras.layers.Dense` layers. These are densely connected, or fully connected, neural layers. The first `Dense` layer has 128 nodes (or neurons). The second (and last) layer returns a logits array with length of 10. Each node contains a score that indicates the current image belongs to one of the 10 classes.
# 
# ### Compile the model
# 
# Before the model is ready for training, it needs a few more settings. These are added during the model's *compile* step:
# 
# * *Loss function* —This measures how accurate the model is during training. You want to minimize this function to "steer" the model in the right direction.
# * *Optimizer* —This is how the model is updated based on the data it sees and its loss function.
# * *Metrics* —Used to monitor the training and testing steps. The following example uses *accuracy*, the fraction of the images that are correctly classified.

# In[15]:


model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


# ## Train the model
# 
# Training the neural network model requires the following steps:
# 
# 1. Feed the training data to the model. In this example, the training data is in the `train_images` and `train_labels` arrays.
# 2. The model learns to associate images and labels.
# 3. You ask the model to make predictions about a test set—in this example, the `test_images` array.
# 4. Verify that the predictions match the labels from the `test_labels` array.
# 

# ### Feed the model
# 
# To start training,  call the `model.fit` method—so called because it "fits" the model to the training data:

# In[16]:


model.fit(train_images, train_labels, epochs=2)


# As the model trains, the loss and accuracy metrics are displayed. This model reaches an accuracy of about 0.91 (or 91%) on the training data.

# ### Evaluate accuracy
# 
# Next, compare how the model performs on the test dataset:

# In[17]:


test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)


# It turns out that the accuracy on the test dataset is a little less than the accuracy on the training dataset. This gap between training accuracy and test accuracy represents *overfitting*. Overfitting happens when a machine learning model performs worse on new, previously unseen inputs than it does on the training data. An overfitted model "memorizes" the noise and details in the training dataset to a point where it negatively impacts the performance of the model on the new data. For more information, see the following:
# *   [Demonstrate overfitting](https://www.tensorflow.org/tutorials/keras/overfit_and_underfit#demonstrate_overfitting)
# *   [Strategies to prevent overfitting](https://www.tensorflow.org/tutorials/keras/overfit_and_underfit#strategies_to_prevent_overfitting)

# ### Make predictions
# 
# With the model trained, you can use it to make predictions about some images.
# The model's linear outputs, [logits](https://developers.google.com/machine-learning/glossary#logits). Attach a softmax layer to convert the logits to probabilities, which are easier to interpret. 

# In[18]:


probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])


# In[19]:


predictions = probability_model.predict(test_images)


# Here, the model has predicted the label for each image in the testing set. Let's take a look at the first prediction:

# In[20]:


predictions[0]


# A prediction is an array of 10 numbers. They represent the model's "confidence" that the image corresponds to each of the 10 different articles of clothing. You can see which label has the highest confidence value:

# In[21]:


np.argmax(predictions[0])


# So, the model is most confident that this image is an ankle boot, or `class_names[9]`. Examining the test label shows that this classification is correct:

# In[22]:


test_labels[0]


# Graph this to look at the full set of 10 class predictions.

# In[23]:


def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array, true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array, true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')


# ### Verify predictions
# 
# With the model trained, you can use it to make predictions about some images.

# Let's look at the 0th image, predictions, and prediction array. Correct prediction labels are blue and incorrect prediction labels are red. The number gives the percentage (out of 100) for the predicted label.

# In[24]:


i = 0
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)
plt.show()


# In[25]:


i = 12
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)
plt.show()


# Let's plot several images with their predictions. Note that the model can be wrong even when very confident.

# In[26]:


# Plot the first X test images, their predicted labels, and the true labels.
# Color correct predictions in blue and incorrect predictions in red.
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions[i], test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()


# ## Use the trained model
# 
# Finally, use the trained model to make a prediction about a single image.

# In[27]:


# Grab an image from the test dataset.
img = test_images[1]

print(img.shape)


# `tf.keras` models are optimized to make predictions on a *batch*, or collection, of examples at once. Accordingly, even though you're using a single image, you need to add it to a list:

# In[28]:


# Add the image to a batch where it's the only member.
img = (np.expand_dims(img,0))

print(img.shape)


# Now predict the correct label for this image:

# In[29]:


predictions_single = probability_model.predict(img)

print(predictions_single)


# In[30]:


plot_value_array(1, predictions_single[0], test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)


# `keras.Model.predict` returns a list of lists—one list for each image in the batch of data. Grab the predictions for our (only) image in the batch:

# In[31]:


np.argmax(predictions_single[0])


# And the model predicts a label as expected.

# In[32]:


model.save('mymodel.h5')


# In[ ]:




