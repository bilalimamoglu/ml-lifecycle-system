# orchestration/scripts/data_generation.py
import pandas as pd
from sklearn.datasets import load_iris
from pathlib import Path


def generate_data():
    # Load the Iris dataset
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['variety'] = pd.Categorical.from_codes(iris.target, iris.target_names)

    # Save the dataset to the /data directory
    data_dir = Path('/opt/orchestration/data')
    data_dir.mkdir(parents=True, exist_ok=True)
    data_file = data_dir / 'iris.csv'
    df.to_csv(data_file, index=False)
    print(f"Iris dataset saved to {data_file}")
