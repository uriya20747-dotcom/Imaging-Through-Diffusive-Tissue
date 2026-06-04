import numpy as np
import cv2
import keras
import os
from keras.models import load_model
import matplotlib.pyplot as plt


def gen_train(pic_list, batch_size, folder_x, folder_y):
    samples_per_epoch = len(pic_list) // 2  # Since we have pairs of blur and original images
    number_of_batches = samples_per_epoch // batch_size
    counter = 0
    while True:
        images_batch = pic_list[batch_size * counter:batch_size * (counter + 1)]
        x_photos, y_photos = [], []

        for file in images_batch:
            if "blur_image_" in file:
                # This is a blurred image
                index = file.split('_')[2].split('.')[0]
                blur_filename = f"blur_image_{index}.jpg"
                org_filename = f"image_{index}.jpg"

                # Read and process x_photo (blur image)
                x_photo_from_file = os.path.join(folder_x, blur_filename)
                x_photo = cv2.imread(x_photo_from_file)
                if x_photo is None:
                    print(f"Error: Unable to load image from {x_photo_from_file}")
                    continue
                x_photo = cv2.cvtColor(x_photo, cv2.COLOR_BGR2RGB)
                x_photo = x_photo.astype('float32') / 255.0
                x_photos.append(x_photo)

                # Read and process y_photo (original image)
                y_photo_from_file = os.path.join(folder_y, org_filename)
                y_photo = cv2.imread(y_photo_from_file)
                if y_photo is None:
                    print(f"Error: Unable to load image from {y_photo_from_file}")
                    continue
                y_photo = cv2.cvtColor(y_photo, cv2.COLOR_BGR2RGB)
                y_photo = y_photo.astype('float32') / 255.0
                y_photos.append(y_photo)

        X_batch = np.array(x_photos)
        y_batch = np.array(y_photos)

        counter += 1
        yield X_batch, y_batch

        if counter >= number_of_batches:
            counter = 0

def plot_acc(autoencoder_fit_plot):
    plt.plot(autoencoder_fit_plot.history['accuracy'])
    plt.plot(autoencoder_fit_plot.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()

def plot_loss (autoencoder_fit_plot):
    plt.plot(autoencoder_fit_plot.history['loss'])
    plt.plot(autoencoder_fit_plot.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.show()


def predict_some_epochs(num_epoch, test_images,folder_x): # you can see that autoencoder is the model
    # Assuming the model file is named "model-{}.h5" where {} is a placeholder for the epoch number
    model_file_path = f"model-{num_epoch}.h5"

    # Load the model from the specified file
    #my_auto_encoder.load_weights(model_file_path)

    list_prob = []
    for num_photo, image_path in enumerate(test_images):
        path_test = os.path.join(folder_x, image_path)
        model_to_predict= load_model(os.path.join(os.getcwd(),model_file_path))
        #model_to_predict=autoencoder
        image = cv2.imread(path_test)  # read
        #image_path = os.path.abspath(image_path)
        #image = cv2.imread(image_path)
        if image is None:
            print(f"image: {image} is not fined")


        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.0
        predictions = model_to_predict.predict(np.expand_dims(image, axis=0))

        # Format the save path with the correct image index
        current_path = os.getcwd()
        predict_path = os.path.join(current_path, "predict_images")
        # Create directories if they don't exist
        os.makedirs(predict_path, exist_ok=True)
        image_name= f"predict_res_{num_photo}.jpg"
        cv2.imwrite(os.path.join(predict_path, image_name), (predictions.squeeze() * 255).astype(np.uint8))
        # Assuming 'predictions' is an image-like array; adjust as needed
        #cv2.imwrite(save_path, (predictions.squeeze() * 255).astype(np.uint8))

        list_prob.append(predictions)

    return list_prob

