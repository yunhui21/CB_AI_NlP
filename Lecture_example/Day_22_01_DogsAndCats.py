# Day_22_01_DogsAndCats.py
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import pickle


def show_history(history, version):
    epochs = np.arange(len(history['loss']))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, history['val_loss'], 'r', label='valid')
    plt.plot(epochs, history['loss'], 'g', label='train')
    plt.title('loss {}'.format(version))
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, history['val_acc'], 'r', label='valid')
    plt.plot(epochs, history['acc'], 'g', label='train')
    plt.title('accuracy {}'.format(version))
    plt.legend()

    plt.show()


def show_history_ema(history, version):
    def get_ema(points, factor=0.8):
        smoothed = [points[0]]
        for pt in points[1:]:
            prev = smoothed[-1]
            smoothed.append(prev * factor + pt * (1 - factor))
        return smoothed

    loss1 = get_ema(history['val_loss'])
    loss2 = get_ema(history['loss'])

    acc1 = get_ema(history['val_acc'])
    acc2 = get_ema(history['acc'])

    epochs = np.arange(len(history['loss']))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, loss1, 'r', label='valid')
    plt.plot(epochs, loss2, 'g', label='train')
    plt.title('loss {}'.format(version))
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, acc1, 'r', label='valid')
    plt.plot(epochs, acc2, 'g', label='train')
    plt.title('accuracy {}'.format(version))
    plt.legend()

    plt.show()


def get_model_name(version):
    filename = 'cats_and_dogs_small_{}.h5'.format(version)
    return os.path.join('models', filename)


def get_history_name(version):
    filename = 'cats_and_dogs_small_{}.history'.format(version)
    return os.path.join('models', filename)


def save_history(history, version):
    with open(get_history_name(version), 'wb') as f:
        pickle.dump(history.history, f)


def load_history(version):
    with open(get_history_name(version), 'rb') as f:
        history = pickle.load(f)
        # show_history(history, version)
        show_history_ema(history, version)


def load_model(version):
    model = tf.keras.models.load_model(get_model_name(version))
    model.summary()

    test_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)

    test_flow = test_gen.flow_from_directory('dogs-vs-cats/small/test',
                                             target_size=[150, 150],
                                             batch_size=1000,
                                             class_mode='binary')
    x, y = test_flow.next()
    # print(x.shape, y.shape)     # (1000, 150, 150, 3) (1000,)

    print('acc :', model.evaluate(x, y, verbose=0))

    # x, y = test_flow.next()
    # print(x.shape, y.shape)
    #
    # print('acc :', model.evaluate(x, y, verbose=0))


# 기본 모델
def model_1():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input([150, 150, 3]))

    model.add(tf.keras.layers.Conv2D(32, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))
    model.add(tf.keras.layers.Conv2D(64, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))
    model.add(tf.keras.layers.Conv2D(128, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))
    model.add(tf.keras.layers.Conv2D(128, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer=tf.keras.optimizers.RMSprop(0.0001),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])

    data_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)

    batch_size = 32
    train_flow = data_gen.flow_from_directory('dogs-vs-cats/small/train',
                                              target_size=[150, 150],
                                              batch_size=batch_size,
                                              class_mode='binary')
    valid_flow = data_gen.flow_from_directory('dogs-vs-cats/small/valid',
                                              target_size=[150, 150],
                                              batch_size=batch_size,
                                              class_mode='binary')
    history = model.fit_generator(train_flow,
                                  steps_per_epoch=2000 // batch_size,
                                  epochs=1,
                                  validation_data=valid_flow,
                                  validation_steps=batch_size,
                                  verbose=2)
    model.save(get_model_name(1))
    save_history(history, 1)


# 기본 모델 + 이미지 증식
def model_2():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input([150, 150, 3]))

    model.add(tf.keras.layers.Conv2D(32, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))
    model.add(tf.keras.layers.Conv2D(64, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))
    model.add(tf.keras.layers.Conv2D(128, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))
    model.add(tf.keras.layers.Conv2D(128, [3, 3], activation='relu'))
    model.add(tf.keras.layers.MaxPool2D([2, 2]))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))                     # 오버피팅 방지
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer=tf.keras.optimizers.RMSprop(0.0001),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])

    train_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255,
                                                                rotation_range=20,
                                                                width_shift_range=0.1,
                                                                height_shift_range=0.1,
                                                                shear_range=0.1,
                                                                zoom_range=0.1,
                                                                horizontal_flip=True)
    valid_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)

    batch_size = 32
    train_flow = train_gen.flow_from_directory('dogs-vs-cats/small/train',
                                               target_size=[150, 150],
                                               batch_size=batch_size,
                                               class_mode='binary')
    valid_flow = valid_gen.flow_from_directory('dogs-vs-cats/small/valid',
                                               target_size=[150, 150],
                                               batch_size=batch_size,
                                               class_mode='binary')
    history = model.fit_generator(train_flow,
                                  steps_per_epoch=2000 // batch_size,
                                  epochs=20,
                                  validation_data=valid_flow,
                                  validation_steps=batch_size,
                                  verbose=2)
    model.save(get_model_name(2))
    save_history(history, 2)


# 전이 학습(사전학습)
def model_3():
    def extract_features(conv_base, data_gen, directory, sample_count, batch_size):
        x = np.zeros([sample_count, 4, 4, 512])
        y = np.zeros([sample_count])

        flow = data_gen.flow_from_directory(directory,
                                            target_size=[150, 150],
                                            batch_size=batch_size,
                                            class_mode='binary')
        for ii, (xx, yy) in enumerate(flow):
            n1 = ii * batch_size
            n2 = n1 + batch_size

            if n2 > sample_count:
                # 사용할 떄 확인 필수
                # remainder = sample_count - n1
                # x[n1:] = conv_base.predict(xx[:remainder])
                # y[n1:] = yy[:remainder]
                break

            x[n1:n2] = conv_base.predict(xx)
            y[n1:n2] = yy

        return x.reshape(-1, 4 * 4 * 512), y

    # conv_base = tf.keras.applications.VGG16()
    conv_base = tf.keras.applications.VGG16(include_top=False, input_shape=[150, 150, 3])

    data_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
    batch_size = 32

    x_train, y_train = extract_features(conv_base, data_gen, 'dogs-vs-cats/small/train', 2000, batch_size)
    x_valid, y_valid = extract_features(conv_base, data_gen, 'dogs-vs-cats/small/valid', 1000, batch_size)
    x_test , y_test  = extract_features(conv_base, data_gen, 'dogs-vs-cats/small/test' , 1000, batch_size)

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(256, activation='relu', input_dim=4 * 4 * 512))
    model.add(tf.keras.layers.Dropout(0.5))                     # 오버피팅 방지
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer=tf.keras.optimizers.RMSprop(0.0001),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=10,
                        validation_data=[x_valid, y_valid],
                        verbose=2)
    # 기본 모델하고 달라서 저장해서 로딩할 수 없다
    # model.save(get_model_name(3))

    model.evaluate(x_test, y_test, verbose=0)
    save_history(history, 3)


# 기본 모델 + 이미지 증식 + 사전학습
def model_4():
    conv_base = tf.keras.applications.VGG16(include_top=False, input_shape=[150, 150, 3])
    conv_base.trainable = False

    # for layer in conv_base.layers:
    #     # print(layer.name)
    #     if 'block5' in layer.name:
    #         layer.trainable = True

    model = tf.keras.Sequential()
    model.add(conv_base)

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))                     # 오버피팅 방지
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer=tf.keras.optimizers.RMSprop(0.0001),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])

    train_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255,
                                                                rotation_range=20,
                                                                width_shift_range=0.1,
                                                                height_shift_range=0.1,
                                                                shear_range=0.1,
                                                                zoom_range=0.1,
                                                                horizontal_flip=True)
    valid_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)

    batch_size = 32
    train_flow = train_gen.flow_from_directory('dogs-vs-cats/small/train',
                                               target_size=[150, 150],
                                               batch_size=batch_size,
                                               class_mode='binary')
    valid_flow = valid_gen.flow_from_directory('dogs-vs-cats/small/valid',
                                               target_size=[150, 150],
                                               batch_size=batch_size,
                                               class_mode='binary')
    history = model.fit_generator(train_flow,
                                  steps_per_epoch=2000 // batch_size,
                                  epochs=1,
                                  validation_data=valid_flow,
                                  validation_steps=batch_size,
                                  verbose=2)
    model.save(get_model_name(4))
    save_history(history, 4)


start = time.time()

# model_1()
# model_2()
# model_3()
# model_4()

print('소요시간 : {:.2f}초'.format(time.time() - start))

# load_history(1)
# load_model(1)
# load_model(2)
# load_model(3)       # 호출 안함
# load_model(4)






