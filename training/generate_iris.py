from sklearn.datasets import load_iris
import pandas as pd
from pathlib import Path

# Load the Iris dataset
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['variety'] = pd.Categorical.from_codes(iris.target, iris.target_names)

# Ensure the /data folder exists
data_dir = Path.cwd() / 'data'
data_dir.mkdir(exist_ok=True)

# Save the dataset to the /data directory
df.to_csv(data_dir / 'iris.csv', index=False)
print(f"Iris dataset saved to {data_dir / 'iris.csv'}")
