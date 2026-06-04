# -*- coding: utf-8 -*-

# from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPooling2D, UpSampling2D


# tensorflow.python.keras.layers import BatchNormalization

from PIL import Image
import E_D_def
import tensorflow as tf
#from tensorflow.python.keras.layers import BatchNormalization
from keras.layers import BatchNormalization
from keras.losses import MeanSquaredError
from keras.layers import (Input, Dense, Flatten, Conv2D, MaxPooling2D, UpSampling2D)
from keras.models import Model
from numpy import save
from keras.callbacks import ModelCheckpoint
from numpy import loadtxt
from keras.models import load_model
from keras.layers import Conv2DTranspose
from keras import layers
from os import listdir  # print all files in path
from shutil import copyfile  # will copy file from source to dest
import random
from random import seed  # how to random
from random import random
import random
import os
from keras.engine.base_preprocessing_layer import PreprocessingLayer

# from tensorflow.python.keras.utils import load_img --> tensorflow.python.keras.utils.load_img
# from tensorflow.python.keras.preprocessing.image import img_to_array
from keras.callbacks import ModelCheckpoint
from keras.utils.vis_utils import plot_model


import cv2
import PIL  # manipulation on images in python
import numpy as np
import matplotlib.pyplot as plt


def print_hi(name):

    # define location of dataset SIMULATION
    #folder_x = r"C:\project final\Simulation_dist\image_blur" #C:\Users\ilaig\PycharmProjects\Simulation_of_distortions\image_blur"  # blur
    #folder_y = r"C:\project final\Simulation_dist\image_org" #"C:\Users\ilaig\PycharmProjects\Simulation_of_distortions\image_org"  # org

    ##################################
    folder_x=r"C:\Users\ilaiga.Owner\PycharmProjects\Images_mode_L\pythonProject\blur"
    folder_y=r"C:\Users\ilaiga.Owner\PycharmProjects\Images_mode_L\pythonProject\orginal"

    ###################################

    after_wiener_list = listdir(folder_x)
    original_list = listdir(folder_y)

    size_after = len(after_wiener_list)
    size_original = len(original_list)
    #size_original - size_after

    random.seed(1)
    random.shuffle(after_wiener_list)  # do shuffle on data

    # detemine the size of train and test and divide to folder
    """
    test_size = 0.05
    val_size = 0.05
    train_size = 0.95
    size = len(after_wiener_list)

    # split to validation, train and test #prefer round not int the train moudle the blur images

    test_pic = after_wiener_list[:int(test_size * size)]
    val_pic = after_wiener_list[int(test_size * size):int(2 * int(test_size * size))]
    train_pic = after_wiener_list[int(2 * int(test_size * size)):-1]
    """

    test_size = 0.2
    val_size = 0.1
    train_size = 0.7
    size = len(after_wiener_list)

    # Calculate the sizes based on proportions
    test_size = int(test_size * size)
    val_size = int(val_size * size)
    train_size = size - test_size - val_size

    # Split the dataset
    test_pic = after_wiener_list[:test_size]
    val_pic = after_wiener_list[test_size:test_size + val_size]
    train_pic = after_wiener_list[test_size + val_size:]
    #print (train_pic)
    # plt.show()
    x_photos, y_photos = list(), list()
    x_photo, y_photo = list(), list()

    # Model Construction
    epochs = 100 #15 work on single computer
    batch_size = 25 #10 work on single computer

    # //Model Construction

    input_img = Input(shape=(200, 200, 3))
    print((input_img.shape), 'input_img')


    # Model Construction

    # Encoder
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    block_1_output = BatchNormalization()(x)
    #block_1_output = tf.keras.layers.BatchNormalization()(x)
    print((block_1_output.shape), 'block_1_output')

    x = Conv2D(128, (3, 3), activation='relu', padding='same')(block_1_output)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    block_2_output = BatchNormalization()(x)
    #block_2_output = tf.keras.layers.BatchNormalization()(x)
    print((block_2_output.shape), 'block_2_output')

    x = Conv2D(256, (3, 3), activation='relu', padding='same')(block_2_output)
    x = Conv2D(256, (3, 3), activation='relu', padding='valid')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='valid')(x)
    block_3_output = BatchNormalization()(x)
    #block_3_output = tf.keras.layers.BatchNormalization()(x)
    print((block_3_output.shape), 'block_3_output')

    x = Conv2D(512, (3, 3), activation='relu', padding='same')(block_3_output)
    x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='same')(x)

    # x = tf.keras.layers.ZeroPadding2D(padding=(1, 1))(x) not mine
    block_4_output = BatchNormalization()(x)
    #block_4_output = tf.keras.layers.BatchNormalization()(x)
    print((block_4_output.shape), 'block_4_output')

    x = Conv2D(1024, (3, 3), activation='relu', padding='same')(block_4_output)
    x = Conv2D(1024, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    block_5_output = BatchNormalization()(x)
    #block_5_output = tf.keras.layers.BatchNormalization()(x)
    print((block_5_output.shape), 'block_5_output')
    encoded = BatchNormalization()(block_5_output)
    #encoded = tf.keras.layers.BatchNormalization()(block_5_output)
    print((encoded.shape), 'encoded')

    # Decoder + skip connection

    x = Conv2D(1024, (3, 3), activation='relu', padding='same')(encoded)
    x = Conv2D(1024, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = layers.add([x, block_5_output])
    x = UpSampling2D((2, 2))(x)
    block_6_output = BatchNormalization()(x)
    #block_6_output = tf.keras.layers.BatchNormalization()(x)
    print((block_6_output.shape), 'block_6_output')

    x = Conv2D(512, (3, 3), activation='relu', padding='same')(encoded)
    x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    #x = tf.keras.layers.ZeroPadding2D(padding=(2, 2))(x)
    block_7_output = layers.add([x, block_4_output])
    print((block_7_output.shape), 'block_7_output')

    x = Conv2D(256, (3, 3), activation='relu', padding='same')(block_7_output)
    # x = tf.keras.layers.ZeroPadding2D(padding=(1, 1))(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    block_8_output = layers.add([x, block_3_output])
    # x = Conv2D(64, (3, 3), activation='relu', padding='same')(block_8_output)
    # block_8_outputx = tf.keras.layers.ZeroPadding2D(padding=(1,1))(x)
    print((block_8_output.shape), 'block_8_output')

    x = Conv2D(128, (3, 3), activation='relu', padding='same')(block_8_output)
    x = tf.keras.layers.ZeroPadding2D(padding=(1, 1))(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='valid')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    block_9_output = layers.add([x, block_2_output])
    print((block_9_output.shape), 'block_9_output')

    x = Conv2D(64, (3, 3), activation='relu', padding='same')(block_9_output)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    block_10_output = layers.add([x, block_1_output])
    print((block_10_output.shape), 'block_10_output')

    x = Conv2D(32, (3, 3), activation='relu', padding='same')(block_10_output)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = BatchNormalization()(x)
    #x = tf.keras.layers.BatchNormalization()(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)
    print((decoded.shape), 'decoded')

    autoencoder = Model(input_img, decoded)

    #mse = tf.keras.losses.MeanSquaredError()
    mse = MeanSquaredError()

    autoencoder.compile(optimizer='adam', loss=mse, metrics=['accuracy'])
    #autoencoder.compile (optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),loss=mse, metrics=['accuracy'])
    autoencoder.summary()
    #plot_model(autoencoder, to_file='model.png', show_shapes=True)
    # define the file path where the model should be saved
    filepath = "model-{epoch:02d}.h5"
    # create a ModelCheckpoint callback to save the model after each epoch
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=False, save_weights_only=False,
                                 mode='auto', save_freq='epoch')

    #train_generator = E_D_def.generator(train_pic,batch_size, folder_x, folder_y)
    #validation_generator = E_D_def.generator(val_pic,batch_size, folder_x, folder_y)
    steps_per_epoch = len(train_pic) / batch_size


    autoencoder_fit_plot = autoencoder.fit(
        x= E_D_def.gen_train(train_pic, batch_size, folder_x, folder_y),
        y=None,
        epochs=epochs,
        callbacks=[checkpoint],
        steps_per_epoch=int(len(train_pic)) / batch_size,
        validation_data=E_D_def.gen_train(val_pic, batch_size, folder_x, folder_y),
        #steps_per_epoch=len(train_pic) / batch_size,
        #validation_steps=(len(val_pic)/ batch_size) * 2,
        validation_steps=int(len(train_pic)) / batch_size * 2,
    )


    #-- plot

    E_D_def.plot_acc(autoencoder_fit_plot)
    E_D_def.plot_loss(autoencoder_fit_plot)

# --------------------------------- works---------------------------------------------------

    #predict_model_prob= E_D_def.predic_some_epochs(25, test_pic,autoencoder_fit_plot)
    #print (predict_model_prob)
# -------------------------------------------------------------------------------------
    #predict model for batches

    predict_model_prob_list = E_D_def.predict_some_epochs(95, test_pic[:],folder_x)
    if predict_model_prob_list is not None:
        #report = classification_report(y_test, predict_model_prob_list)
        #print (report)
        print (predict_model_prob_list)


    #x_test_100 = test_pic[0:99]
    #x_test = autoencoder.predict(gen_predict(x_test_100))

"""
        # print after wiener pic
    for i in range(5):
        # define filename
        filename = folder_x + '\\' + after_wiener_list[i]
        image_x = cv2.imread(filename)
        # convert the image to NumPy array and ensure it's of type 'uint8'

        image_x = np.asarray(image_x).astype('uint8')
        # plt.imshow(image_x)
        # plt.show()

    # print original pic
    for i in range(5):
        # define filename
        filename = folder_y + '\\' + after_wiener_list[i]
        # load image
        image_y = cv2.imread(filename)
        image_y = np.asarray(image_y).astype('uint8')
        # plot
        # plt.imshow(image_y)
        # plt.show()

    # print Y pic- the blur
    for file in train_pic[0:50]:
        y_phot = folder_y + "/" + file
        y_photoo = cv2.imread(y_phot)
        y_photoo = cv2.resize(y_photoo, (100, 100))
        y_photo_n = np.pad(y_photoo, [(50, 50), (50, 50), (0, 0)])
        y_photo = np.asarray(y_photo_n).astype('uint8')
        y_photos.append(y_photo)

    for i in y_photos[:5]:
        img_y = np.asarray(i).astype('uint8')
        # plt.imshow(img_y)
        # plt.show()

    # print X pic
    for file in train_pic[0:50]:
        x_phot = folder_x + "/" + file
        x_photo = cv2.imread(x_phot)
        x_photo = np.asarray(x_photo).astype('uint8')
        # store
        x_photos.append(x_photo)

    for i in x_photos[:5]:
        img_x = np.asarray(i).astype('uint8')
        # plt.imshow(img_x)
        # plt.show()



"""


    # def gen_predict(list_to_predict):
    #         x_photos, x_photo = list(), list()
    #         for file in list_to_predict:
    #             x_phot = folder_x+"/"+file
    #             x_photo = cv2.imread(x_phot)
    #             x_photo = np.asarray(x_photo).astype('uint8')
    #             # convert to numpy array
    #  #           x_photo = img_to_array(x_photo).astype('float32')
    #             x_photo = x_photo/255
    #             # store
    #             x_photos.append(x_photo)
    #         X_batch = np.array(x_photos).astype('float32')
    #         yield X_batch

    # #predict for test
    # x_test_100 = test_pic[0:99]
    # x_test = autoencoder.predict(gen_predict(x_test_100))

    # for num in range(30):
    #     counter = num
    #     for i in x_test[counter:counter+1]:
    # #        img = PIL.Image.fromarray(i, 'RGB')
    # #        img.save('my.png')
    # #        img.show()
    # #        cv2.imshow('i',i)
    # #        cv2.waitKey(0)
    #         cv2.imwrite(str(num)+'i_x_test_predict_1024_cv2.tif', i[::,-1])
    #         plt.imshow(i)
    #         plt.savefig(str(num)+'i_x_test_predict_1024.tif')
    #         plt.show()
    #     #print after wiener pic
    #     for ii in x_test_100[counter:counter+1]:
    #         # define filename
    #         filename = folder_x + '\\' + ii
    #         image_x = cv2.imread(filename)
    # #        image_x = np.asarray(image_x).astype('uint8')
    #         plt.imshow(image_x)
    #         plt.savefig(str(num)+'ii_x_test_predict_1024.tif')
    #         plt.show()
    #     for iii in x_test_100[counter:counter+1]:
    #         # define filename
    #         filename = folder_y + '\\' + iii
    #         image_y = cv2.imread(filename)
    # #        image_x = np.asarray(image_x).astype('uint8')
    #         plt.imshow(image_y)
    #         plt.savefig(str(num)+'iii_x_test_predict_1024.tif')
    #         plt.show()
    #     counter += 1

    # # #predict for train
    # # x_train_100 = train_pic[0:99]
    # # x_train = autoencoder.predict(gen_predict(x_train_100))

    # # for num in range(10):
    # #     counter = num
    # #     for i in x_train[counter:counter+1]:
    # #         x_photo = np.asarray(i).astype('uint8')
    # #         plt.imshow(i)
    # #         plt.show()
    # #     #print after wiener pic
    # #     # for i in x_train_100[counter:counter+1]:
    # #     #     # define filename
    # #     #     filename = folder_x + '\\' + i
    # #     #     image_x = cv2.imread(filename)
    # #     #     image_x = np.asarray(image_x).astype('uint8')
    # #     #     plt.imshow(image_x)
    # #     #     plt.show()
    # #     for iii in x_train_100[counter:counter+1]:
    # #         # define filename
    # #         filename = folder_y + '\\' + iii
    # #         image_y = cv2.imread(filename)
    # # #        image_x = np.asarray(image_x).astype('uint8')
    # #         plt.imshow(image_y)
    # # #        plt.savefig(str(num)+'iii_x_test_predict_new.tif')
    # #         plt.show()
    # #     counter += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
