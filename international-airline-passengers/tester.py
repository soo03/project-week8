import numpy as np
import matplotlib.pyplot as plt
import os

class Trainer:
    def __init__(self):
        pass

    @staticmethod
    def save_history_history(fname, history_history, fold=''):
        np.save(os.path.join(fold, fname), history_history)

    @staticmethod
    def load_history_history(fname, fold=''):
        history_history = np.load(os.path.join(fold, fname)).item(0)
        return history_history

    @staticmethod
    def plot_acc(history, title=None):
        if not isinstance(history, dict):
            history = history.history

        plt.plot(history['acc'])
        plt.plot(history['val_acc'])
        if title is not None:
            plt.title(title)
        plt.ylabel('Accuracy') #정확도
        plt.xlabel('Epoch') #회전
        plt.legend(['Training Data', 'Validation Data'], loc=0)
        #plt.show()

    @staticmethod
    def plot_loss(history, title=None):
        if not isinstance(history, dict):
            history = history.history
        plt.plot(history['loss'])
        plt.plot(history['val_loss'])
        if title is not None:
            plt.title(title)
        plt.ylabel('Loss')  # 정확도
        plt.xlabel('Epoch')  # 회전
        plt.legend(['Training Data', 'Validation Data'], loc=0)
        # plt.show()

    def plot_history(self,history):
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 2, 1)
        self.plot_acc(history)
        plt.subplot(1, 2, 2)
        self.plot_loss(history)

    def plot_loss_acc(self,history):
        self.plot_loss(history, '(a) Loss trajectory')
        plt.show()
        self.plot_acc(history, '(b) Accuracy trajectory')
        plt.show()

    def plot_acc_loss(self, history):
        self.plot_acc(history, '(a) Accuracy trajectory')
        plt.show()
        self.plot_loss(history, '(b) Loss trajectory')
        plt.show()











