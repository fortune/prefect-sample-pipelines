# Prefect Sample Pipelines

Python 製のワークフロー管理ツール [Prefect](https://www.prefect.io/) を使ってパイプラインのサンプルをいくつか作成してみる。

## Preequisites

- [Prefect SDK](https://docs.prefect.io/v3/get-started/install) はインストール済み
- [Prefect Cloud アカウント](https://app.prefect.cloud/) と API キー（Self-hosted な Prefect サーバを使うならなくてもいい）

## Work pool 作成

```sh
prefect work-pool create --type process sample-pipelines
```

を実行して Prefect サーバに `sample-pipelines` という名前の **Work pool** を作成。Work pool のタイプは `--type process` にしたが、適宜好きなものに変えること（[other work pool types](https://docs.prefect.io/v3/deploy/infrastructure-concepts/work-pools#work-pool-types)）。

タイプを `--type process` にした場合は、ワークフローを実行するサーバ上で Work pool を Polling する **Worker** プロセスを次のように起動しておく。

```sh
prefect worker start --pool sample-pipelines
```

## 単純なパイプライン

- [simple_ml.py](./simple_ml.py)
- [simple_ml_create_deployment.py](./simple_ml_create_deployment.py)

[OpemML](https://openml.org/) からデータセットをロードし、分類モデルを訓練して評価するだけの機械学習パイプラインを定義するスクリプトと、作成済みの `sample-pipelines` Work pool へ **Deployment** リソースを登録するためのスクリプト。

```sh
python simple_ml_create_deployment.py
```

を実行すれば **Deployment** リソースが登録される。
