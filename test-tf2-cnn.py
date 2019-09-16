#===========================================================================================================================================================
#    Program Name:    test-tf2-cnn.py
#    Executed in :    /home/DeepLearning
#                     python test-tf2-cnn.py
#    Date Created:    14 September 2019
#
#    https://www.tensorflow.org/beta/tutorials/images/intro_to_cnns
#

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

from tensorflow.keras import datasets, layers, models

(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0


#  CREATE THE CONVOLUTIONAL BASE

#  As input, a CNN takes tensors of shape (image_height, image_width, color_channels), ignoring the batch size. If you are new to color 
#  channels, MNIST has one (because the images are grayscale), whereas a color image has three (R,G,B). In this example, we will  
#  configure our CNN to process inputs of shape (28, 28, 1), which is the format of MNIST images. We do this by passing the argument 
#  input_shape to our first layer.

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.summary()

#  
# To complete our model, we will feed the last output tensor from the convolutional base (of shape (3, 3, 64)) into one or more Dense # # layers to perform classification. Dense layers take vectors as input (which are 1D), while the current output is a 3D tensor. First, # we will flatten (or unroll) the 3D output to 1D, then add one or more Dense layers on top. MNIST has 10 output classes, so we use a # # final Dense layer with 10 outputs and a softmax activation.
#

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)

#  Evaluate the model

test_loss, test_acc = model.evaluate(test_images, test_labels)

print(test_acc)
