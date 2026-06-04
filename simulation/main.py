
import tensorflow as tf
import distortions as ds
import numpy as np
import cv2

def main():
    mnist = tf.keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    re_size_img=(200,200)
    new_list=[cv2.resize(img,re_size_img,interpolation=cv2.INTER_AREA) for img in train_images[:10000]]
    train_resize= np.array(new_list)
    ds.classifier_to_folders(train_resize)


"""
    # Example on one image how  distorted image look like.
    example_index = 0
    plt.imshow(train_images[example_index], cmap='gray')
    plt.title(f"Label: {train_labels[example_index]}")
    plt.show()
    blur_img= ds.gaussian_m (train_images[example_index])
    plt.imshow(blur_img, cmap='gray')
    plt.show()

    # classifier to original and distorted

"""



if __name__ == '__main__':
    main()

