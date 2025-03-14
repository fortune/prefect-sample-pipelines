from prefect import flow

# 実行対象の Flow がある場所を定義
SOURCE_REPO="https://github.com/fortune/prefect-sample-pipelines.git"

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        # Flow のエントリポイントを指定。Python スクリプトと関数を指定する。
        entrypoint="simple_ml.py:classification_pipeline", # Specific flow to run
    ).deploy(
        name="simple-ml-deployment", # この Deployment リソースの名前

        # Flow のエントリポイントとなる関数に渡すパラメータを定義
        parameters={
            "dataset_name": "adult",
            "version": 2
        },
        work_pool_name="sample-pipelines",  # この Deployment の登録先となるワークプールの名前
        cron="0 * * * *",  # Flow の実行スケジュールを指定（Run every hour）
    )