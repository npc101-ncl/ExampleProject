import os
import pandas as pd
import matplotlib.pyplot as plt

working_directory = os.path.abspath('')  # create a base directory to work from
CSVPaths = {"S":os.path.join(working_directory, 'S.csv'),
            "SI":os.path.join(working_directory, 'SI.csv'),
            "SI1":os.path.join(working_directory, 'SI1.csv'),
            "SI2":os.path.join(working_directory, 'SI2.csv')}

for myTitle ,myPath in CSVPaths.items():
    myData = pd.read_csv(myPath)
    myLines = plt.plot(myData.iloc[:, 0], myData.iloc[:, 1:])
    plt.title(myTitle)
    plt.legend(iter(myLines), list(myData.columns)[1:])
    plt.show()