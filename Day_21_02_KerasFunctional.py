# Day_21_02_KerasFunctional.py
import tensorflow as tf
from sklearn import model_selection, preprocessing
import numpy as np

# 문제 1
# and 연산에 대한 데이터를 생성해서 결과를 예측하세요.

def regression_and():

    data = [[0, 0, 0],
            [0, 1, 0],
            [1, 0, 0],
            [1, 1, 1]]
    data = np.float32(data)

    x = data[:, :-1]
    y = data[:, -1:]

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))

    model.compile(optimizer='sgd',
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])  #

    model.fit(x, y, epochs=10000, verbose=2)

    print('acc:', model.evaluate(x, y))

    preds = model.predict(x)
    print(preds)


def regression_xor():
    data = [[0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]]
    data = np.float32(data)

    x = data[:, :-1]
    y = data[:, -1:]

    model = tf.keras.Sequential()
    model.add(tf.keras.Input([2]))
    model.add(tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))
    model.add(tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))

    model.compile(optimizer=tf.keras.optimizers.Adam(0.1),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])  #

    model.fit(x, y, epochs=100, verbose=2)

    print('acc:', model.evaluate(x, y))

    preds = model.predict(x)
    print(preds)

# 기본버전
def regression_xor_functional_1():
    data = [[0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]]
    data = np.float32(data)

    x = data[:, :-1]
    y = data[:, -1:]

    # model = tf.keras.Sequential()
    # model.add(tf.keras.Input([2]))
    # model.add(tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))
    # model.add(tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))

    # 1번
    # input   = tf.keras.Input([2])
    # dense1  = tf.keras.layers.Dense(units=2, activation=tf.keras.activations.sigmoid)
    # output1 = dense1.__call__(input)
    # dense2  = tf.keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid)
    # output2 = dense2.__call__(output1)
    # model = tf.keras.Model(input, output2)

    # 2번
    # input   = tf.keras.Input([2])
    # dense1  = tf.keras.layers.Dense(2, activation=tf.keras.activations.sigmoid)
    # output1 = dense1(input) # __call__ 삭제해도 파이선에서 클래스합수를 불러오는 기능을 활용
    # dense2  = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)
    # output2 = dense2(output1)
    # model = tf.keras.Model(input, output2)

    # 3번
    input = tf.keras.Input([2])
    output1 = tf.keras.layers.Dense(2, activation=tf.keras.activations.sigmoid)(input)
    output2 = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(output1)
    model = tf.keras.Model(input, output2)

    model.compile(optimizer=tf.keras.optimizers.Adam(0.1),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])  #

    model.fit(x, y, epochs=1000, verbose=2)

    print('acc:', model.evaluate(x, y))

    preds = model.predict(x)
    print(preds)

# 멀티 입력 버전
def regression_xor_functional_2():
    data = [[0, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]]
    data = np.float32(data)

    x1 = data[:, :1]
    x2 = data[:, 1:2]
    y  = data[:, 2:]

    input_left = tf.keras.Input([1])
    output_left = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(input_left)

    input_right = tf.keras.Input([1])
    output_right = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(input_right)

    output = tf.keras.layers.concatenate([output_left, output_right], axis=1)
    output_bind = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(output)


    model = tf.keras.Model([input_left, input_right], output_bind)

    model.compile(optimizer=tf.keras.optimizers.Adam(0.1),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])  #

    model.fit([x1,x2], y, epochs=1000, verbose=2)

    print('acc:', model.evaluate([x1,x2], y))

    preds = model.predict([x1,x2])
    print(preds)

# 멀치 입출력 버전
def regression_xor_functional_3():
    data = [[0, 0, 0, 0],
            [0, 1, 1, 0],
            [1, 0, 1, 0],
            [1, 1, 0, 1]]
    data = np.float32(data)

    x1 = data[:, :1]
    x2 = data[:, 1:2]
    y1  = data[:, 2:3]
    y2  = data[:, 3:]

    input_left = tf.keras.Input([1])
    output_left = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(input_left)

    input_right = tf.keras.Input([1])
    output_right = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(input_right)

    output = tf.keras.layers.concatenate([output_left, output_right], axis=1)

    output_left = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(output)
    output_right = tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid)(output)

    model = tf.keras.Model([input_left, input_right], [output_left, output_right])

    model.compile(optimizer=tf.keras.optimizers.Adam(0.1),
                  loss=tf.keras.losses.binary_crossentropy,
                  metrics=['acc'])  #

    model.fit([x1,x2], [y1,y2], epochs=1000, verbose=2)
    print(model.evaluate([x1, x2], [y1, y2], verbose = 0))

    # print('acc:', model.evaluate([x1,x2], [y1,y2]))
    #
    # preds = model.predict([x1,x2])
    # print(preds)

# regression_end()
# regression_xor()
# regression_xor_functional_1()
# regression_xor_functional_2()
regression_xor_functional_3()