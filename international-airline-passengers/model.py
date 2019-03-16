import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
from keras import models, layers
import seaborn as sns
from international_airline_passengers.tester import Trainer

class Machine:
    def __init__(self):
        self.data = DataSet()
        shape = self.data.X.shape[1:]
        self.model = self.rnn_model(shape)

    def run(self, epochs=400): # 학습텀 epoch 400 회 훈련
        d = self.data
        X_train, X_test, y_train, y_test = \
            d.X_train, d.X_test, d.y_train, d.y_test
        X, y = d.X, d.y
        m = self.model
        h = m.fit(X_train, y_train, epochs= epochs, validation_data=[X_test, y_test], verbose=0)
        trainer = Trainer()
        trainer.plot_loss(h)
        plt.title("History of training")
        #plt.show()
        yp = m.predict(X_test)
        print('Loss: ', m.evaluate(X_test, y_test))

        plt.plot(yp, label='Original ')
        plt.plot(y_test, label='Prediction')
        plt.legend(loc=0)
        plt.title('Validation Result')
        plt.show()

        yp = m.predict(X_test).reshape(-1)
        print('loss: ', m.evaluate(X_test, y_test))
        print(yp.shape, y_test)

        df = pd.DataFrame()
        df['Sample'] = list(range(len(y_test))) * 2
        df['Normalized #Passengers'] = np.concatenate([y_test, yp], axis=0)
        df['Type'] = ['Original'] * len(y_test) + ['Prediction'] * len(yp)

        plt.figure(figsize=(7, 5))
        sns.barplot(x="Sample",
                    y="Normalized #Passengers",
                    hue="Type",
                    data=df)
        plt.ylabel("Nomalized #Passengers")
        plt.show()

        yp = m.predict(X)

        plt.plot(yp, label='Original')
        plt.plot(y, label='Prediction')
        plt.legend(loc=0)
        plt.title('All Results')
        plt.show()

    @staticmethod
    def rnn_model(shape):
        m_x = layers.Input(shape=shape)
        m_h = layers.LSTM(10)(m_x)
        m_y = layers.Dense(1)(m_h)
        m = models.Model(m_x, m_y)

        m.compile('adam', 'mean_squared_error')
        m.summary()
        return m



class DataSet:
    def __init__(self, fname='data/international-airline-passengers.csv', D=12):
        data_dn = self.load_data(fname=fname)
        X, y = self.get_Xy(data_dn, D=D)
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=42)

        self.X, self.y = X, y
        self.X_train, self.X_test, self.y_train, self.y_test = X_train, X_test, y_train, y_test

    @staticmethod
    def load_data(fname):
        dataset = pd.read_csv(fname, usecols=[1], engine='python', skipfooter=3)
        data = dataset.values.reshape(-1)

        plt.plot(data)
        plt.xlabel('Time')
        plt.ylabel('#Passengers')
        plt.title('1. Original Data')
        plt.show()

        # data normalize
        data_dn = (data - np.mean(data)) / np.std(data) / 5

        plt.plot(data_dn)
        plt.xlabel('Time')
        plt.ylabel("Normalize #Passengers")
        plt.title("2. Normalize Data")
        plt.show()
        return data_dn

    @staticmethod
    def get_Xy(data, D=12):
        X_l = [] #알파벳 l
        y_l = []
        N = len(data)
        assert N > D, "N should be larger than D, where N is len(data)" #로그. 디버깅용
        for ii in range(N - D - 1):
            X_l.append(data[ii:ii + D])
            y_l.append(data[ii + D])
        X = np.array(X_l)
        X = X.reshape(X.shape[0], X.shape[1], 1)
        y = np.array(y_l)
        print(X.shape, y.shape)
        return X, y



