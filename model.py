from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def model(data_file):
    data = pd.read_csv(data_file)
    train, test = train_test_split(data, test_size=0.2)
    model = SGDClassifier()
    features_headers = ["macd", "psar"]
    train_features = np.array(train[features_headers].values)
    train_labels = np.array(train["label"].values)
    model.fit(train_features, train_labels)

    test_features = np.array(test[features_headers].values)
    test_labels = np.array(test["label"].values)
    train_predictions = model.predict(train_features)

    '''
    buy_macd = []
    buy_psar = []
    sell_macd = []
    sell_psar = []
    print 2
    for a in range(len(train_labels)):
        print a
        if train_labels[a] == 1:
            buy_macd.append(train_features[a, 1])
            buy_psar.append(train_features[a, 0])
        else:
            sell_macd.append(train_features[a, 1])
            sell_psar.append(train_features[a, 0])

    plt.show()
    '''
    '''
    # plot the line, the points, and the nearest vectors to the plane
    xx = np.linspace(-0.05, 0.05, 0.01)
    yy = np.linspace(-0.01, 0.01, 0.002)

    X1, X2 = np.meshgrid(xx, yy)
    Z = np.empty(X1.shape)
    for (i, j), val in np.ndenumerate(X1):
        x1 = val
        x2 = X2[i, j]
        p = clf.decision_function([[x1, x2]])
        Z[i, j] = p[0]
    levels = [-1.0, 0.0, 1.0]
    linestyles = ['dashed', 'solid', 'dashed']
    colors = 'k'
    plt.contour(X1, X2, Z, levels, colors=colors, linestyles=linestyles)
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired,
                edgecolor='black', s=20)

    plt.axis('tight')
    plt.show()
    '''
    print model.score(test_features, test_labels)


if __name__ == '__main__':
    model("metrics_data.csv")
