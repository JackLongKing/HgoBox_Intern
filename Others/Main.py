from keras.applications import Xception, MobileNet
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Reshape, Conv2D, Activation
from keras.models import Model, save_model, load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard, Callback
from keras.utils.generic_utils import CustomObjectScope
import keras
import os


MODEL_DIR = '..\\data\\model'
TRAIN_DIR = '..\\data\\train'
VAL_DIR = '..\\data\\validation'

CLASS_NUMBER = 128
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCH_CUT = 6
AUTO_SAVE_PER_EPOCH = 2

val_datagen = ImageDataGenerator(rescale=1/255)
train_datagen = ImageDataGenerator(rescale=1/255,
                                   rotation_range=30,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.1,
                                   zoom_range=0.1,
                                   channel_shift_range=10,
                                   horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(TRAIN_DIR, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE)
val_generator = val_datagen.flow_from_directory(VAL_DIR, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE)


class AutoSave(Callback):
    def __init__(self, model, N):
        self.model = model
        self.N = N

    def on_epoch_end(self, epoch, logs={}):
        if epoch % self.N == 0 and epoch != 0:
            save_model(model,  os.path.join(MODEL_DIR, 'model' + str(epoch) + '.h5'))
            print('saved model to ' + os.path.join(MODEL_DIR, 'model' + str(epoch) + '.h5'))


def define_model():
    # base_model = Xception(weights='imagenet', include_top=False)
    # x = base_model.output
    # x = GlobalAveragePooling2D()(x)
    # x = Dropout(0.5)(x)
    # x = Dense(1024, activation='relu')(x)
    # x = Dropout(0.5)(x)
    # prediction = Dense(CLASS_NUMBER, activation='softmax')(x)


    # base_model = MobileNet(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    # x = base_model.output
    # x = GlobalAveragePooling2D()(x)
    # x = Reshape((1, 1, 1024))(x)
    # x = Dropout(0.5)(x)
    # x = Conv2D(CLASS_NUMBER, (1, 1), padding='same')(x)
    # x = Activation('softmax')(x)
    # prediction = Reshape((CLASS_NUMBER,))(x)
    #
    # model = Model(inputs=base_model.input, outputs=prediction)

    base_model = MobileNet(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    x = base_model.input
    for i, layer in enumerate(base_model.layers[1:]):
        if (i+3) % 6 == 0:
            x = Dropout(0.2)(x)
        x = layer(x)

    x = GlobalAveragePooling2D()(x)
    x = Reshape((1, 1, 1024))(x)
    x = Dropout(0.5)(x)
    x = Conv2D(CLASS_NUMBER, (1, 1), padding='same')(x)
    x = Activation('softmax')(x)
    prediction = Reshape((CLASS_NUMBER,))(x)

    model = Model(inputs=base_model.input, outputs=prediction)

    # for i, layer in enumerate(model.layers):
    #     print(str(i) + ' ' + layer.name)
    #
    # for i, layer in enumerate(base_model.layers):
    #     print(str(i) + ' ' + layer.name)

    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


if input('define new model? (y/n) ') == 'y':
    model = define_model()
else:
    with CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,
                            'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):
        model = load_model(os.path.join(MODEL_DIR, 'model.h5'))

# print(model.summary())

tb_callback = TensorBoard(log_dir='..\\data\\graph')
as_callback = AutoSave(model, EPOCH_CUT//AUTO_SAVE_PER_EPOCH)

model.fit_generator(generator=train_generator, steps_per_epoch=len(train_generator)//EPOCH_CUT,
                    validation_data=val_generator, validation_steps=len(val_generator)//EPOCH_CUT,
                    epochs=20*EPOCH_CUT, verbose=1,
                    callbacks=[tb_callback, as_callback])
save_model(model, os.path.join(MODEL_DIR, 'model.h5'))

# print(model.evaluate_generator(val_generator, steps=len(val_generator)))
