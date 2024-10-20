# orchestration/scripts/data_preprocessing.py
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path


def preprocess_data():
    data_dir = Path('/opt/orchestration/data')
    data_file = data_dir / 'iris.csv'
    df = pd.read_csv(data_file)

    # Split the dataset
    X = df.drop('variety', axis=1)
    y = df['variety']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save the splits
    X_train.to_csv(data_dir / 'X_train.csv', index=False)
    X_test.to_csv(data_dir / 'X_test.csv', index=False)
    y_train.to_csv(data_dir / 'y_train.csv', index=False)
    y_test.to_csv(data_dir / 'y_test.csv', index=False)
    print("Data preprocessing completed.")
