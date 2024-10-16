import requests

def test_mlflow():
    try:
        response = requests.get("http://localhost:5000")
        if response.status_code == 200:
            print("Mlflow server is running successfully.")
        else:
            print(f"Failed to reach Mlflow server. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to Mlflow server: {e}")

if __name__ == "__main__":
    test_mlflow()
