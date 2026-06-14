import hashlib
import json
import os
import re
from datetime import datetime

import pandas as pd
import requests
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor


RAW_FOLDER = "/app/raw_files"
CLEAN_FOLDER = "/app/clean_data"
BEST_MODEL_PATH = "/app/clean_data/best_model.pickle"
MODEL_METADATA_PATH = "/app/clean_data/model_metadata.json"
SECURITY_AUDIT_PATH = "/app/clean_data/security_audit.json"
CITY_REGEX = re.compile(r"^[A-Za-zÀ-ÿ .']{1,50}$")


def get_safe_cities():
    cities = Variable.get("cities", deserialize_json=True)

    if not isinstance(cities, list) or len(cities) == 0:
        raise ValueError("Variable Airflow cities invalide")

    clean_cities = []

    for city in cities:
        if not isinstance(city, str):
            raise ValueError("Chaque ville doit etre une chaine")

        city = city.strip().lower()

        if not CITY_REGEX.match(city):
            raise ValueError(f"Nom de ville invalide: {city}")

        clean_cities.append(city)

    return clean_cities


def get_api_key():
    api_key = Variable.get("api_key", default_var=None)

    if api_key is None or len(api_key.strip()) == 0:
        raise ValueError("Variable Airflow api_key manquante")

    return api_key.strip()


def validate_weather_json(data):
    if not isinstance(data, dict):
        raise ValueError("Reponse API invalide")

    if "main" not in data:
        raise ValueError("Champ main manquant")

    if "temp" not in data["main"]:
        raise ValueError("Champ temperature manquant")

    if "pressure" not in data["main"]:
        raise ValueError("Champ pression manquant")

    if "name" not in data:
        raise ValueError("Champ ville manquant")


def transform_data_into_csv(n_files=None, filename="data.csv"):
    files = [
        f for f in os.listdir(RAW_FOLDER)
        if f.endswith(".json") and f != "null_file.json"
    ]

    files = sorted(files, reverse=True)

    if n_files:
        files = files[:n_files]

    rows = []

    for f in files:
        path = os.path.join(RAW_FOLDER, f)

        with open(path, "r", encoding="utf8") as file:
            data_temp = json.load(file)

        if not isinstance(data_temp, list):
            data_temp = [data_temp]

        for data_city in data_temp:
            try:
                validate_weather_json(data_city)

                rows.append(
                    {
                        "temperature": data_city["main"]["temp"],
                        "city": data_city["name"],
                        "pression": data_city["main"]["pressure"],
                        "date": f.replace(".json", "")
                    }
                )
            except Exception as exc:
                print("Ligne ignoree:", exc)

    df = pd.DataFrame(rows, columns=["temperature", "city", "pression", "date"])

    output_path = os.path.join(CLEAN_FOLDER, filename)
    df.to_csv(output_path, index=False)

    print("Fichier cree:", output_path)
    print(df.head(10))

    if df.empty:
        raise ValueError(f"{filename} est vide")

    return output_path


def prepare_data(path_to_data="/app/clean_data/fulldata.csv"):
    df = pd.read_csv(path_to_data)

    if df.empty:
        raise ValueError("fulldata.csv est vide")

    df = df.sort_values(["city", "date"], ascending=True)

    dfs = []

    for city in df["city"].unique():
        df_temp = df[df["city"] == city].copy()

        df_temp.loc[:, "target"] = df_temp["temperature"].shift(-1)

        for i in range(1, 10):
            df_temp.loc[:, f"temp_m_{i}"] = df_temp["temperature"].shift(i)

        df_temp = df_temp.dropna()
        dfs.append(df_temp)

    if len(dfs) > 0:
        df_final = pd.concat(dfs, axis=0, ignore_index=True)
    else:
        df_final = pd.DataFrame()

    if df_final.empty:
        print("Pas encore assez d historique, fallback simple")
        df_final = df.copy()
        df_final.loc[:, "target"] = df_final["temperature"]
    else:
        df_final = df_final.drop(["date"], axis=1)

    df_final = pd.get_dummies(df_final)

    features = df_final.drop(["target"], axis=1)
    target = df_final["target"]

    if len(features) < 3:
        raise ValueError("Pas assez de lignes pour entrainer les modeles")

    return features, target


def compute_model_score(model, X, y):
    cv = min(3, len(X))

    cross_validation = cross_val_score(
        model,
        X,
        y,
        cv=cv,
        scoring="neg_mean_squared_error"
    )

    model_score = cross_validation.mean()

    return model_score


def train_and_save_model(model, X, y, path_to_model):
    model.fit(X, y)
    dump(model, path_to_model)
    print(str(model), "saved at", path_to_model)

def get_file_sha256(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def check_file_exists_and_not_empty(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier manquant: {path}")

    if os.path.getsize(path) == 0:
        raise ValueError(f"Fichier vide: {path}")

    return {
        "path": path,
        "size_bytes": os.path.getsize(path)
    }


def write_json_report(path, data):
    with open(path, "w", encoding="utf8") as file:
        json.dump(data, file, indent=2)

    print("Rapport cree:", path)



def score_model(model_name, model, path_to_data):
    X, y = prepare_data(path_to_data)
    score = compute_model_score(model, X, y)

    print("model:", model_name)
    print("score:", score)

    return {
        "model_name": model_name,
        "score": score
    }


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1
}


with DAG(
    dag_id="weather_secmlops_dag",
    description="Weather pipeline with minimal SecMLOps controls",
    schedule_interval="* * * * *",
    default_args=default_args,
    catchup=False,
    tags=["datascientest", "exam", "airflow", "secmlops"],
    doc_md="""
# Weather SecMLOps DAG

This DAG collects weather data from OpenWeatherMap, stores raw JSON files,
transforms them into CSV files, trains regression models and saves the best model.

Security controls added for the exam version:

* API key stored in an Airflow Variable
* cities validated before API calls
* timeout on API requests
* HTTP status checked
* JSON schema checked before transformation
* empty CSV files rejected
"""
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    @task
    def fetch_weather_data():
        os.makedirs(RAW_FOLDER, exist_ok=True)

        cities = get_safe_cities()
        api_key = get_api_key()

        weather_data = []

        for city in cities:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city,
                    "appid": api_key,
                    "units": "metric"
                },
                timeout=10
            )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Erreur API pour {city}: {response.status_code} {response.text}"
                )

            data = response.json()
            validate_weather_json(data)
            weather_data.append(data)

        now = datetime.utcnow().strftime("%Y_%m_%d_%H_%M")
        output_file = os.path.join(RAW_FOLDER, f"{now}.json")

        with open(output_file, "w", encoding="utf8") as file:
            json.dump(weather_data, file)

        print("Fichier raw cree:", output_file)
        print("Nombre de villes:", len(weather_data))

        return output_file

    @task
    def transform_recent_data():
        return transform_data_into_csv(n_files=20, filename="data.csv")

    @task
    def transform_full_data():
        return transform_data_into_csv(filename="fulldata.csv")

    @task
    def train_linear_regression(path_to_data):
        return score_model(
            "LinearRegression",
            LinearRegression(),
            path_to_data
        )

    @task
    def train_decision_tree(path_to_data):
        return score_model(
            "DecisionTreeRegressor",
            DecisionTreeRegressor(random_state=42),
            path_to_data
        )

    @task
    def train_random_forest(path_to_data):
        return score_model(
            "RandomForestRegressor",
            RandomForestRegressor(n_estimators=50, random_state=42),
            path_to_data
        )

    @task
    def select_and_save_best_model(scores, path_to_data):
        best_score = max(scores, key=lambda item: item["score"])
        best_model_name = best_score["model_name"]

        print("Scores:", scores)
        print("Best model:", best_model_name)

        if best_model_name == "LinearRegression":
            model = LinearRegression()
        elif best_model_name == "DecisionTreeRegressor":
            model = DecisionTreeRegressor(random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=50, random_state=42)

        X, y = prepare_data(path_to_data)
        train_and_save_model(model, X, y, BEST_MODEL_PATH)

        model_hash = get_file_sha256(BEST_MODEL_PATH)

        metadata = {
            "best_model_name": best_model_name,
            "best_model_score": best_score["score"],
            "model_path": BEST_MODEL_PATH,
            "model_sha256": model_hash,
            "training_rows": len(X),
            "training_features": list(X.columns),
            "generated_at_utc": datetime.utcnow().isoformat()
        }

        write_json_report(MODEL_METADATA_PATH, metadata)

        return BEST_MODEL_PATH

    @task
    def security_audit(model_path):
        checks = {
            "data_csv": check_file_exists_and_not_empty("/app/clean_data/data.csv"),
            "fulldata_csv": check_file_exists_and_not_empty("/app/clean_data/fulldata.csv"),
            "model": check_file_exists_and_not_empty(model_path),
            "model_metadata": check_file_exists_and_not_empty(MODEL_METADATA_PATH),
            "model_sha256": get_file_sha256(model_path),
            "checked_at_utc": datetime.utcnow().isoformat(),
            "status": "passed"
        }

        write_json_report(SECURITY_AUDIT_PATH, checks)

        return SECURITY_AUDIT_PATH

    raw_file = fetch_weather_data()
    recent_csv = transform_recent_data()
    full_csv = transform_full_data()

    with TaskGroup("model_training") as model_training:
        score_lr = train_linear_regression(full_csv)
        score_dt = train_decision_tree(full_csv)
        score_rf = train_random_forest(full_csv)

    best_model = select_and_save_best_model(
        [score_lr, score_dt, score_rf],
        full_csv
    )

    audit_report = security_audit(best_model)

    start >> raw_file >> [recent_csv, full_csv]
    full_csv >> model_training >> best_model >> audit_report >> end
