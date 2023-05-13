def predict(f):
    if(int(f[0]) == 0):
        return int(0)
    else:
        return int(1)




# # Import required libraries
# import os
# import cv2
# import numpy as np
# from sklearn.model_selection import train_test_split
# from keras.models import Sequential
# from keras.utils import to_categorical
# from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# def test():
#     # Define path to the dataset directory
#     data_dir = "/path/to/dataset"

#     # Define class labels
#     classes = ["accident", "no_accident"]

#     # Define image size and channels
#     img_size = (1920, 1080)
#     channels = 3

#     # Initialize empty lists to store images and labels
#     data = []
#     labels = []

#     # Loop over each class label
#     for class_label in classes:
#         # Define path to class directory
#         class_dir = os.path.join(data_dir, class_label)

#         # Loop over each image file in the class directory
#         for img_file in os.listdir(class_dir):
#             # Read image file and resize to desired size
#             img = cv2.imread(os.path.join(class_dir, img_file))
#             img = cv2.resize(img, img_size)

#             # Append image and label to the data and labels lists
#             data.append(img)
#             labels.append(class_label)

#     # Convert data and labels to numpy arrays
#     data = np.array(data)
#     labels = np.array(labels)

#     # Split data into training and testing sets
#     train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=42)


#     # Define input shape and number of classes
#     input_shape = (img_size[0], img_size[1], channels)
#     num_classes = len(classes)

#     # Build CNN model
#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Conv2D(128, (3, 3), activation='relu'))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Flatten())
#     model.add(Dense(512, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(num_classes, activation='softmax'))

#     # Compile the model
#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#     # Convert labels to one-hot encoded vectors
#     train_labels_onehot = to_categorical(train_labels, num_classes)
#     test_labels_onehot = to_categorical(test_labels, num_classes)

#     # Train the model
#     history = model.fit(train_data, train_labels_onehot, epochs=10, batch_size=32, validation_data=(test_data, test_labels_onehot))
#     # Evaluate the model on the testing set
#     test_loss, test_acc = model.evaluate(test_data, test_labels_onehot)
#     print("Test loss:", test_loss)
#     print("Test accuracy:", test_acc)

#     # Load an example image
#     example_img = cv2.imread("/path/to/example/image")
#     example_img = cv2.resize(example_img, img_size)

#     # Make a prediction on the example image
#     pred = model.predict(np.array([example_img]))
#     pred_class = classes[np.argmax(pred)]
