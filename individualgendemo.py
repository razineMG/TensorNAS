from tensornas.blocktemplates.blockarchitectures import classificationblockarchitectures
from tensorflow import keras

##### Training MNIST data
(
    (images_train, labels_train),
    (images_test, labels_test),
) = keras.datasets.mnist.load_data()
input_shape = images_train.shape
images_train = images_train.reshape(
    images_train.shape[0], images_train.shape[1], images_train.shape[2], 1
)
images_test = images_test.reshape(
    images_test.shape[0], images_test.shape[1], images_test.shape[2], 1
)
input_tensor_shape = (images_train.shape[1], images_train.shape[2], 1)
images_train = images_train.astype("float32")
images_test = images_test.astype("float32")
images_train /= 255
images_test /= 255
mnist_class_count = 10
#######

from tensornas.layers import Conv2D, Flatten, Dropout, Reshape
from tensornas.layers.Dense import HiddenDense, OutputDense
from tensornas.layers.MaxPool import MaxPool2D, MaxPool3D

# test = Conv2D.Layer(input_tensor_shape)
# print(test.get_name())
# test.print()
# test.mutate()
#
# test = Flatten.Layer(input_tensor_shape)
# print(test.get_name())
# test.print()
# test.mutate()
#
# test = Dropout.Layer(input_tensor_shape)
# print(test.get_name())
# test.print()
# test.mutate()
#
# test = HiddenDense.Layer(input_tensor_shape)
# print(test.get_name())
# test.print()
# test.mutate()
# test.print()
#
# test = OutputDense.Layer(input_tensor_shape, 10)
# print(test.get_name())
# test.print()
# test.mutate()
# test.print()
#
# test = Reshape.Layer(input_tensor_shape, [1, 784])
# print(test.get_name())
# test.print()
# test.mutate()
# test.print()
#
# test = MaxPool2D.Layer(input_tensor_shape)
# print(test.get_name())
# test.print()
# test.mutate()
# test.print()
#
# test = MaxPool3D.Layer(input_tensor_shape)
# print(test.get_name())
# test.print()
# test.mutate()
# test.print()


model = classificationblockarchitectures.ClassificationBlockArchitecture(
    input_tensor_shape, mnist_class_count
)

model.print()

model.evaluate(
    train_data=images_train,
    train_labels=labels_train,
    test_data=images_test,
    test_labels=labels_test,
    epochs=2,
    batch_size=100,
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)


# # idea, constrain previous layer, it stop multiple flatten being created sequentially
#
print("Done")
