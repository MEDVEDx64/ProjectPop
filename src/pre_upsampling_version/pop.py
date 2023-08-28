import sqlite3
import numpy
import os

from keras.layers import Input, Conv2D
from keras.models import Model, load_model
from imageio.v3 import imread, imwrite
from random import shuffle
from sys import argv

POP_MODEL = 'pop.h5'
POP_DB = 'pop.db'
DATASET = 'dataset'

def load_img(path):
    return numpy.array([(imread(path)/255).astype(numpy.float32)])

def save_img(path, arr):
    imwrite(path, ((numpy.clip(arr, 0.0, 1.0))*255).astype(numpy.uint8))

def load(y, n):
    p = 'x'
    if y:
        p = 'y'

    path = os.path.join(DATASET, p, n)
    return load_img(path)

def train(model):
    n = 0
    print('Listing and shuffling...')
    files = os.listdir(os.path.join(DATASET, 'y'))
    shuffle(files)
    fln = len(files)

    with sqlite3.connect(POP_DB) as con:
        (n,) = con.cursor().execute('SELECT COUNT(*) FROM checked').fetchone()

        for f in files:
            try:
                n += 1

                res = con.cursor().execute('SELECT n FROM checked WHERE n = ?', (f,))
                if res.fetchone():
                    continue

                print(str(n) + ' / ' + str(fln))

                try:
                    model.fit(load(False, f), load(True, f))
                except KeyboardInterrupt:
                    raise
                except:
                    print('Training error at sample #' + str(n))
                    #raise
                    continue
            
                con.cursor().execute('INSERT INTO checked VALUES(?)', (f,))
                model.save(POP_MODEL)

            except KeyboardInterrupt:
                print('HALT!')
                try:
                    model.save(POP_MODEL)
                except KeyboardInterrupt:
                    pass

                break

def create_model():
    input_img = Input(shape=(1080, 1920, 3), dtype=numpy.float32)

    x = Conv2D(128, (3, 3), activation='relu', padding='same')(input_img)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    x = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    model = Model(input_img, x)
    model.compile(optimizer='adam', loss='mse')

    return model

def create():
    model = None
    if os.path.exists(POP_MODEL):
        model = load_model(POP_MODEL)
        print('Existing model loaded')
    else:
        model = create_model()
    model.summary()

    if not os.path.exists(POP_DB):
        with sqlite3.connect(POP_DB) as con:
            con.cursor().execute('CREATE TABLE checked(n varchar NOT NULL PRIMARY KEY)')

    train(model)

def predict():
    model = load_model(POP_MODEL)
    files = os.listdir('in')
    fln = len(files)
    n = 0

    for f in files:
        n += 1
        print(str(n) + ' / ' + str(fln))
        save_img(os.path.join('out', f), model.predict(load_img(os.path.join('in', f))))

def main():
    if len(argv) < 2:
        print('subcommands are: train, predict')
        return
    
    if argv[1] == 'train':
        create()
    elif argv[1] == 'predict':
        predict()
    else:
        print('???')

if __name__ == '__main__':
    main()
