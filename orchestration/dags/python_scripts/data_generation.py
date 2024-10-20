import pandas as pd
from sklearn.datasets import load_iris
from pathlib import Path

def generate_data():
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['variety'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    # Update the data directory path
    data_dir = Path('/opt/airflow/data')
    data_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_dir / 'iris.csv', index=False)
    print(f"Iris dataset saved to {data_dir / 'iris.csv'}")
