import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import joblib

data_dir = "/Users/huanglh/Downloads/Tests-1/101/"
model_file = "/tmp/fall_detection_model.pkl"

# K-Nearest Neighbors
# loop through all files in the data_dir
data_frames = []
for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        # only process files with .txt extension
        if file.endswith(".txt"):
            file_path = os.path.join(subdir, file)
            # read in the data file and create a Pandas DataFrame
            data = pd.read_csv(file_path, sep='\t', header=0,
                               names=["Acc_X", "Acc_Y", "Acc_Z", "Mag_X", "Mag_Y", "Mag_Z", "fall"])
            data_frames.append(data)

# concatenate all the DataFrames into a single DataFrame
all_data = pd.concat(data_frames)

# split the data into input features and target variable
X = all_data.iloc[:, :-1]
y = all_data.iloc[:, -1]

# create a KNN classifier with k=5
knn_model = KNeighborsClassifier(n_neighbors=5)

# train the model on the data
knn_model.fit(X, y)

# obtain the predicted labels for the training data
y_pred_train = knn_model.predict(X)

# compute the accuracy score of the model on the training data
accuracy_train = accuracy_score(y, y_pred_train)

# print the accuracy score
print(f"Training accuracy: {accuracy_train:.3f}")

# save the trained model to disk
joblib.dump(knn_model, model_file)
