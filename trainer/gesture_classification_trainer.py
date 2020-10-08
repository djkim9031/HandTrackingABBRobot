from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
import tensorflow as tf
from tensorflow.keras.callbacks import ReduceLROnPlateau,ModelCheckpoint,EarlyStopping
from tensorflow.keras.regularizers import l2

IMAGE_SIZE=224
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 0.0005
LR_DECAY = 0.0001
PATIENCE=30
CLASSIFIER_WEIGHTS_FILE="classification_inceptionv3.h5"
RESUME=False


def create_model():

    core = InceptionV3(input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3), include_top=False, weights="imagenet")
    for layer in core.layers:
      layer.trainable = True

    x = core.output
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(50,activation='relu')(x)
    x = tf.keras.layers.Dense(4,activation='softmax')(x)
    model = tf.keras.Model(inputs=[core.input], outputs=[x])

    regularizer = l2(WEIGHT_DECAY / 2)
    for weight in model.trainable_weights:
        with tf.keras.backend.name_scope("weight_regularizer"):
            model.add_loss(lambda: regularizer(weight))
    return model

model = create_model()
model.summary()


from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAINING_DIR = 'Gesture_Dataset/training'
VALIDATION_DIR = 'Gesture_Dataset/validation'
train_datagen = ImageDataGenerator(
    rotation_range=30,
    zoom_range=[0.8, 1.0],
    horizontal_flip=True,
    brightness_range=[0.5,1.2],
    fill_mode='nearest',
    preprocessing_function=preprocess_input)
validation_datagen = ImageDataGenerator(
    zoom_range=[0.8, 1.0],
    horizontal_flip=True,
    brightness_range=[0.5,1.2],
    fill_mode='nearest',
    preprocessing_function=preprocess_input)

train_generator = train_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(IMAGE_SIZE,IMAGE_SIZE),
    batch_size=32,
    class_mode='categorical'
)
validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(IMAGE_SIZE,IMAGE_SIZE),
    batch_size=8,
    class_mode='categorical'
)
if RESUME:
  model.load_weights(CLASSIFIER_WEIGHTS_FILE)

#optimizer = tf.keras.optimizers.SGD(lr=LEARNING_RATE, decay=LR_DECAY, momentum=0.9, nesterov=False)
optimizer = tf.keras.optimizers.Nadam(lr=LEARNING_RATE, decay=LR_DECAY)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics='accuracy')
checkpoint = ModelCheckpoint("gesture_classification_InceptionV3.h5", monitor="val_loss", verbose=1,save_best_only=True,
                                 save_weights_only=True, mode="min")
reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.6, patience=10, min_lr=1e-7, verbose=1, mode="min")
stop = EarlyStopping(monitor="val_loss", patience=PATIENCE, mode="min")

history = model.fit(train_generator,epochs=200,verbose=1,callbacks=[checkpoint, reduce_lr,stop],validation_data=validation_generator)

