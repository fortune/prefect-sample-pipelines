"""Prefect による ML パイプラインのサンプル

OpenML からデータを取得し、分類モデルを作成し、評価する。
"""

import pandas as pd
from prefect import flow, task
from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


# -------------------------
# データ取得（OpenML）
# -------------------------
@task(retries=3)
def load_data(dataset_name, version):
    print(f"📥 Fetching dataset from OpenML: {dataset_name} (version {version})")
    dataset = fetch_openml(name=dataset_name, version=version, as_frame=True)
    X = dataset.data
    y = dataset.target
    print(f"✅ Dataset shape: {X.shape}")
    return X, y


# -------------------------
# 前処理（数値変換 & 分割）
# -------------------------
@task
def preprocess_data(X, y, test_size=0.3):
    # カテゴリ変数を数値に変換（OneHot or LabelEncodingでもOK）
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    # ラベルがカテゴリ型の場合、文字列から整数に変換
    if y.dtype == 'category' or y.dtype == 'object':
        y = pd.factorize(y)[0]

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=test_size, random_state=42
    )
    print(f"🧹 Preprocessed: X_train={X_train.shape}, X_test={X_test.shape}")
    return X_train, X_test, y_train, y_test


# -------------------------
# モデル訓練
# -------------------------
@task
def train_model(X_train, y_train):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    print("✅ Model trained")
    return clf


# -------------------------
# モデル評価
# -------------------------
@task
def evaluate_model(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    print("📊 Classification Report:")
    print(df_report)
    return df_report


# -------------------------
# Flow定義
# -------------------------
@flow(name="ML Classification Pipeline with OpenML", log_prints=True)
def classification_pipeline(dataset_name, version):
    X, y = load_data(dataset_name, version)
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    clf = train_model(X_train, y_train)
    evaluate_model(clf, X_test, y_test)


# -------------------------
# エントリーポイント
# -------------------------
if __name__ == "__main__":
    classification_pipeline(dataset_name="adult", version=2)
