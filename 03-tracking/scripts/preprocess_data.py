
import os
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
import pickle
import urllib.request

def download_data(url, filename):
    """Downloads data from a URL and saves it to a file."""
    print(f"Downloading {url} to {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        raise

def preprocess_data(data_path, output_path):
    """Loads, preprocesses, and saves the taxi dataset."""
    # Create directories if they don't exist
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    # Download and load the data
    jan_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-01.parquet"
    feb_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2023-02.parquet"

    download_data(jan_url, os.path.join(data_path, "jan.parquet"))
    download_data(feb_url, os.path.join(data_path, "feb.parquet"))

    df_jan = pd.read_parquet(os.path.join(data_path, "jan.parquet"))
    df_feb = pd.read_parquet(os.path.join(data_path, "feb.parquet"))

    # For simplicity, we'll just use the January and February data for training and validation
    df_train = df_jan
    df_val = df_feb

    # Preprocessing steps
    categorical = ['PULocationID', 'DOLocationID']
    numerical = ['trip_distance']

    df_train['duration'] = df_train.lpep_dropoff_datetime - df_train.lpep_pickup_datetime
    df_train.duration = df_train.duration.apply(lambda td: td.total_seconds() / 60)
    df_train = df_train[(df_train.duration >= 1) & (df_train.duration <= 60)]

    df_val['duration'] = df_val.lpep_dropoff_datetime - df_val.lpep_pickup_datetime
    df_val.duration = df_val.duration.apply(lambda td: td.total_seconds() / 60)
    df_val = df_val[(df_val.duration >= 1) & (df_val.duration <= 60)]

    df_train[categorical] = df_train[categorical].astype(str)
    df_val[categorical] = df_val[categorical].astype(str)

    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    val_dicts = df_val[categorical + numerical].to_dict(orient='records')

    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    X_val = dv.transform(val_dicts)

    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    # Save the preprocessed data
    with open(os.path.join(output_path, "X_train.pkl"), "wb") as f:
        pickle.dump(X_train, f)
    with open(os.path.join(output_path, "y_train.pkl"), "wb") as f:
        pickle.dump(y_train, f)
    with open(os.path.join(output_path, "X_val.pkl"), "wb") as f:
        pickle.dump(X_val, f)
    with open(os.path.join(output_path, "y_val.pkl"), "wb") as f:
        pickle.dump(y_val, f)
    with open(os.path.join(output_path, "dv.pkl"), "wb") as f:
        pickle.dump(dv, f)

if __name__ == '__main__':
    data_path = "data"
    output_path = "data/processed"
    preprocess_data(data_path, output_path)
