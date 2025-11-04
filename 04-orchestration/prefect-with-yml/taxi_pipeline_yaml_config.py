#!/usr/bin/env python
# coding: utf-8

"""
🚕 NYC Taxi Duration Prediction - YAML Config Version
Pipeline con configuración YAML y artifacts estructurados entre tasks
"""

import os
import pickle
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass

import yaml
import pandas as pd
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import root_mean_squared_error

import mlflow
from prefect import task, flow, get_run_logger
from prefect.artifacts import create_table_artifact, create_markdown_artifact

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuración del pipeline cargada desde YAML"""
    mlflow_uri: str
    experiment_name: str
    data_url_pattern: str
    min_duration: float
    max_duration: float
    categorical_features: list
    numerical_features: list
    model_params: dict
    num_boost_round: int
    early_stopping_rounds: int
    models_dir: str
    preprocessor_filename: str
    retries: int
    retry_delay_seconds: int
    
    @classmethod
    def from_yaml(cls, config_path: str = "config.yaml"):
        """Cargar configuración desde archivo YAML"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return cls(
            mlflow_uri=config['mlflow']['tracking_uri'],
            experiment_name=config['mlflow']['experiment_name'],
            data_url_pattern=f"{config['data']['base_url']}/{config['data']['file_pattern']}",
            min_duration=config['data']['min_duration'],
            max_duration=config['data']['max_duration'],
            categorical_features=config['data']['categorical_features'],
            numerical_features=config['data']['numerical_features'],
            model_params=config['model']['params'],
            num_boost_round=config['model']['num_boost_round'],
            early_stopping_rounds=config['model']['early_stopping_rounds'],
            models_dir=config['output']['models_dir'],
            preprocessor_filename=config['output']['preprocessor_filename'],
            retries=config['prefect']['retries'],
            retry_delay_seconds=config['prefect']['retry_delay_seconds']
        )


def setup_mlflow(config: PipelineConfig):
    """Setup MLflow con configuración desde YAML"""
    try:
        mlflow.set_tracking_uri(config.mlflow_uri)
        mlflow.search_experiments()
        logger.info(f"✅ Connected to MLflow at: {config.mlflow_uri}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to connect: {e}")
        logger.info("Falling back to local SQLite database")
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
    
    try:
        mlflow.set_experiment(config.experiment_name)
        logger.info(f"✅ Experiment set: {config.experiment_name}")
    except Exception as e:
        logger.error(f"❌ Failed to set MLflow experiment: {e}")
        raise


@dataclass
class DataLoadResult:
    """Resultado de la carga de datos - se pasa entre tasks"""
    dataframe: pd.DataFrame
    year: int
    month: int
    num_records: int
    avg_duration: float
    unique_locations: int


@task(
    name="📥 YAML-Config: Load Taxi Data",
    description="[YAML Version] Load NYC taxi data from parquet files",
    tags=["yaml-config", "data", "extract"]
)
def yaml_load_taxi_data(year: int, month: int, config: PipelineConfig) -> DataLoadResult:
    """
    Carga datos de NYC taxi para un año y mes específico.
    Retorna un objeto DataLoadResult que se pasa a la siguiente task.
    """
    logger = get_run_logger()
    
    url = config.data_url_pattern.format(year=year, month=month)
    logger.info(f"📂 Loading data from: {url}")
    
    try:
        df = pd.read_parquet(url)
        logger.info(f"✅ Successfully loaded {len(df)} records")
    except Exception as e:
        logger.error(f"❌ Failed to load data from {url}: {e}")
        raise

    # Feature engineering
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    # Filter outliers usando config
    df = df[(df.duration >= config.min_duration) & (df.duration <= config.max_duration)]
    logger.info(f"🔍 Filtered to {len(df)} records (duration: {config.min_duration}-{config.max_duration} min)")

    # Categorical features desde config
    df[config.categorical_features] = df[config.categorical_features].astype(str)
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    # Calcular estadísticas
    num_records = len(df)
    avg_duration = df['duration'].mean()
    unique_locations = df['PU_DO'].nunique()

    # Crear artifact con resumen
    summary_data = [
        ["📊 Metric", "Value"],
        ["Total Records", f"{num_records:,}"],
        ["Average Duration", f"{avg_duration:.2f} min"],
        ["Min Duration", f"{df['duration'].min():.2f} min"],
        ["Max Duration", f"{df['duration'].max():.2f} min"],
        ["Unique PU_DO", f"{unique_locations:,}"],
        ["Period", f"{year}-{month:02d}"],
        ["🏷️ Version", "YAML Config"]
    ]

    create_table_artifact(
        key=f"yaml-data-summary-{year}-{month:02d}",
        table=summary_data,
        description=f"📊 [YAML Config] Data summary for {year}-{month:02d}"
    )

    # Retornar objeto estructurado
    return DataLoadResult(
        dataframe=df,
        year=year,
        month=month,
        num_records=num_records,
        avg_duration=avg_duration,
        unique_locations=unique_locations
    )


@dataclass
class FeatureResult:
    """Resultado de feature engineering - se pasa entre tasks"""
    X: any  # Sparse matrix
    y: any  # Target array
    dv: DictVectorizer
    num_features: int
    num_samples: int


@task(
    name="🔧 YAML-Config: Engineer Features",
    description="[YAML Version] Create feature matrix using DictVectorizer",
    tags=["yaml-config", "features", "transform"]
)
def yaml_engineer_features(
    data_result: DataLoadResult,
    config: PipelineConfig,
    dv: Optional[DictVectorizer] = None
) -> FeatureResult:
    """
    Crea matriz de features desde DataLoadResult.
    Recibe el resultado de yaml_load_taxi_data como input.
    """
    logger = get_run_logger()
    
    df = data_result.dataframe
    
    # Features desde config
    categorical = ['PU_DO']
    numerical = config.numerical_features
    
    # Verificar columnas
    missing_cols = [col for col in categorical + numerical if col not in df.columns]
    if missing_cols:
        raise ValueError(f"❌ Missing required columns: {missing_cols}")
    
    dicts = df[categorical + numerical].to_dict(orient='records')
    logger.info(f"📝 Created {len(dicts):,} feature dictionaries")

    # Fit o transform
    if dv is None:
        dv = DictVectorizer(sparse=True)
        X = dv.fit_transform(dicts)
        logger.info(f"✅ Fitted DictVectorizer with {X.shape[1]:,} features")
        
        # Crear artifact solo cuando se hace fit
        feature_info = [
            ["📊 Metric", "Value"],
            ["Total Features", f"{X.shape[1]:,}"],
            ["Categorical Features", len(categorical)],
            ["Numerical Features", len(numerical)],
            ["Samples", f"{X.shape[0]:,}"],
            ["Sparsity", f"{(1 - X.nnz / (X.shape[0] * X.shape[1])) * 100:.2f}%"],
            ["🏷️ Version", "YAML Config"]
        ]

        create_table_artifact(
            key=f"yaml-feature-info-{data_result.year}-{data_result.month:02d}",
            table=feature_info,
            description=f"🔧 [YAML Config] Features for {data_result.year}-{data_result.month:02d}"
        )
    else:
        X = dv.transform(dicts)
        logger.info(f"✅ Transformed features: {X.shape[1]:,} features")

    # Target
    y = df['duration'].values

    return FeatureResult(
        X=X,
        y=y,
        dv=dv,
        num_features=X.shape[1],
        num_samples=X.shape[0]
    )


@dataclass
class ModelResult:
    """Resultado del entrenamiento - se pasa al flow principal"""
    run_id: str
    rmse: float
    num_boost_rounds: int
    best_iteration: int


@task(
    name="🤖 YAML-Config: Train XGBoost Model",
    description="[YAML Version] Train XGBoost model with MLflow tracking",
    tags=["yaml-config", "model", "train", "xgboost"]
)
def yaml_train_xgboost_model(
    train_features: FeatureResult,
    val_features: FeatureResult,
    config: PipelineConfig
) -> ModelResult:
    """
    Entrena modelo XGBoost.
    Recibe FeatureResult de train y validation como inputs.
    """
    logger = get_run_logger()
    
    # Crear directorio de modelos
    models_folder = Path(config.models_dir)
    models_folder.mkdir(exist_ok=True)
    
    logger.info(f"🎯 Training with {train_features.num_samples:,} samples, {train_features.num_features:,} features")

    with mlflow.start_run() as run:
        # Preparar datos
        train = xgb.DMatrix(train_features.X, label=train_features.y)
        valid = xgb.DMatrix(val_features.X, label=val_features.y)

        # Parámetros desde config
        params = config.model_params
        mlflow.log_params(params)
        
        # Log configuración adicional
        mlflow.log_param("num_boost_round", config.num_boost_round)
        mlflow.log_param("early_stopping_rounds", config.early_stopping_rounds)
        mlflow.log_param("pipeline_version", "yaml-config")

        # Entrenar
        logger.info("🚀 Starting training...")
        booster = xgb.train(
            params=params,
            dtrain=train,
            num_boost_round=config.num_boost_round,
            evals=[(valid, 'validation')],
            early_stopping_rounds=config.early_stopping_rounds
        )

        # Evaluar
        y_pred = booster.predict(valid)
        rmse = root_mean_squared_error(val_features.y, y_pred)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("train_samples", train_features.num_samples)
        mlflow.log_metric("val_samples", val_features.num_samples)
        mlflow.log_metric("num_features", train_features.num_features)
        
        logger.info(f"📊 RMSE: {rmse:.4f}")

        # Guardar preprocessor
        preprocessor_path = models_folder / config.preprocessor_filename
        with open(preprocessor_path, "wb") as f_out:
            pickle.dump(train_features.dv, f_out)
        
        try:
            mlflow.log_artifact(str(preprocessor_path), artifact_path="preprocessor")
            mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")
            logger.info("✅ Successfully logged model and preprocessor to MLflow")
        except Exception as e:
            logger.warning(f"⚠️ Failed to log to MLflow: {e}")

        # Crear artifact de performance
        performance_data = [
            ["📊 Metric", "Value"],
            ["RMSE", f"{rmse:.4f}"],
            ["Best Iteration", booster.best_iteration],
            ["Train Samples", f"{train_features.num_samples:,}"],
            ["Val Samples", f"{val_features.num_samples:,}"],
            ["Features", f"{train_features.num_features:,}"],
            ["Learning Rate", params['learning_rate']],
            ["Max Depth", params['max_depth']],
            ["MLflow Run ID", run.info.run_id[:8] + "..."],
            ["🏷️ Version", "YAML Config"]
        ]

        create_table_artifact(
            key="yaml-model-performance",
            table=performance_data,
            description=f"🎯 [YAML Config] Model performance - RMSE: {rmse:.4f}"
        )

        # Markdown detallado
        markdown_content = f"""
# 🤖 Model Training Summary (YAML Config Version)

## 📊 Performance Metrics
- **RMSE**: {rmse:.4f} minutes
- **Best Iteration**: {booster.best_iteration}/{config.num_boost_round}
- **MLflow Run ID**: `{run.info.run_id}`
- **Pipeline Version**: YAML Config

## 📈 Data Statistics
- **Training Samples**: {train_features.num_samples:,}
- **Validation Samples**: {val_features.num_samples:,}
- **Total Features**: {train_features.num_features:,}

## ⚙️ Hyperparameters (from config.yaml)
| Parameter | Value |
|-----------|-------|
| Learning Rate | {params['learning_rate']} |
| Max Depth | {params['max_depth']} |
| Min Child Weight | {params['min_child_weight']} |
| Reg Alpha | {params['reg_alpha']} |
| Reg Lambda | {params['reg_lambda']} |
| Objective | {params['objective']} |

## 🎯 Training Configuration
- **Boost Rounds**: {config.num_boost_round}
- **Early Stopping**: {config.early_stopping_rounds} rounds
- **Config File**: `config.yaml`

## 📁 Artifacts Saved
- ✅ Model: `mlartifacts/.../models_mlflow/`
- ✅ Preprocessor: `{preprocessor_path}`
- ✅ MLflow Experiment: `{config.experiment_name}`
        """

        create_markdown_artifact(
            key="yaml-training-summary",
            markdown=markdown_content,
            description="📝 [YAML Config] Detailed training summary"
        )

        return ModelResult(
            run_id=run.info.run_id,
            rmse=rmse,
            num_boost_rounds=config.num_boost_round,
            best_iteration=booster.best_iteration
        )


@flow(
    name="🚕 Taxi Duration ML Pipeline (YAML-Config)",
    description="[YAML Version] Config-driven ML pipeline with structured artifacts",
    flow_run_name="taxi-yaml-{year}-{month}"
)
def taxi_duration_yaml_pipeline(
    year: int,
    month: int,
    config_path: str = "config.yaml"
) -> ModelResult:
    """
    Flow principal que orquesta todas las tasks.
    Usa configuración desde YAML y pasa artifacts entre tasks.
    
    DIFERENCIAS CON LA VERSIÓN ORIGINAL:
    - ✅ Configuración desde YAML
    - ✅ Artifacts estructurados entre tasks
    - ✅ Nombres únicos para diferenciar en Prefect UI
    """
    logger = get_run_logger()
    
    # 1. Cargar configuración desde YAML
    logger.info(f"📋 Loading configuration from: {config_path}")
    config = PipelineConfig.from_yaml(config_path)
    
    # 2. Setup MLflow
    setup_mlflow(config)
    
    # 3. Cargar datos de entrenamiento
    logger.info(f"📥 Loading training data: {year}-{month:02d}")
    train_data = yaml_load_taxi_data(year=year, month=month, config=config)
    
    # 4. Calcular período de validación
    next_year = year if month < 12 else year + 1
    next_month = month + 1 if month < 12 else 1
    
    # 5. Cargar datos de validación
    logger.info(f"📥 Loading validation data: {next_year}-{next_month:02d}")
    val_data = yaml_load_taxi_data(year=next_year, month=next_month, config=config)
    
    # 6. Crear features de entrenamiento (fit DictVectorizer)
    logger.info("🔧 Creating training features...")
    train_features = yaml_engineer_features(
        data_result=train_data,
        config=config,
        dv=None  # Fit nuevo
    )
    
    # 7. Crear features de validación (transform con DV existente)
    logger.info("🔧 Creating validation features...")
    val_features = yaml_engineer_features(
        data_result=val_data,
        config=config,
        dv=train_features.dv  # Reutilizar DV del training
    )
    
    # 8. Entrenar modelo
    logger.info("🤖 Training model...")
    model_result = yaml_train_xgboost_model(
        train_features=train_features,
        val_features=val_features,
        config=config
    )
    
    # 9. Crear resumen final del pipeline
    pipeline_summary = f"""
# 🎉 YAML-Config Pipeline Execution Complete!

## 🏷️ Pipeline Version
**YAML Configuration-Driven Pipeline**

## 📊 Data Summary
| Period | Records | Avg Duration | Unique Locations |
|--------|---------|--------------|------------------|
| **Training** ({train_data.year}-{train_data.month:02d}) | {train_data.num_records:,} | {train_data.avg_duration:.2f} min | {train_data.unique_locations:,} |
| **Validation** ({val_data.year}-{val_data.month:02d}) | {val_data.num_records:,} | {val_data.avg_duration:.2f} min | {val_data.unique_locations:,} |

## 🎯 Model Performance
- **RMSE**: {model_result.rmse:.4f} minutes
- **Best Iteration**: {model_result.best_iteration}/{model_result.num_boost_rounds}

## 🔗 Results
- **MLflow Run ID**: `{model_result.run_id}`
- **MLflow URI**: `{config.mlflow_uri}`
- **Experiment**: `{config.experiment_name}`

## 📁 Configuration
- **Config File**: `{config_path}`
- **Models Directory**: `{config.models_dir}/`
- **Preprocessor**: `{config.preprocessor_filename}`

## ✨ Key Features
- ✅ Configuration from YAML file
- ✅ Structured artifacts between tasks
- ✅ Type-safe dataclasses
- ✅ Unique task names for Prefect UI

## 🚀 Next Steps
1. Review model performance in MLflow UI
2. Compare with previous runs
3. Consider model deployment if RMSE < 6.0 minutes

---
*Pipeline executed with YAML-config approach* 🎯
    """

    create_markdown_artifact(
        key="yaml-pipeline-summary",
        markdown=pipeline_summary,
        description="📋 [YAML Config] Complete pipeline execution summary"
    )
    
    logger.info(f"✅ YAML Pipeline completed! RMSE: {model_result.rmse:.4f}")
    
    return model_result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='🚕 NYC Taxi Duration Prediction with YAML Configuration'
    )
    parser.add_argument(
        '--year',
        type=int,
        default=2023,
        help='Year of training data (default: 2023)'
    )
    parser.add_argument(
        '--month',
        type=int,
        default=1,
        help='Month of training data (default: 1)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to config YAML file (default: config.yaml)'
    )
    args = parser.parse_args()

    try:
        print("\n" + "="*70)
        print("🚕 NYC Taxi Duration Prediction - YAML Config Pipeline")
        print("="*70)
        print(f"📋 Config File: {args.config}")
        print(f"📅 Training Period: {args.year}-{args.month:02d}")
        print(f"🏷️  Version: YAML Configuration-Driven")
        print("="*70 + "\n")
        
        # Ejecutar flow
        result = taxi_duration_yaml_pipeline(
            year=args.year,
            month=args.month,
            config_path=args.config
        )
        
        print("\n" + "="*70)
        print("✅ YAML-Config Pipeline Completed Successfully!")
        print("="*70)
        print(f"📊 RMSE: {result.rmse:.4f} minutes")
        print(f"🔗 MLflow Run ID: {result.run_id}")
        print(f"🎯 Best Iteration: {result.best_iteration}/{result.num_boost_rounds}")
        print(f"🏷️  Pipeline Version: YAML Config")
        print("="*70 + "\n")
        
        # Guardar run ID
        with open("yaml_pipeline_run_id.txt", "w") as f:
            f.write(result.run_id)
            
    except FileNotFoundError as e:
        print(f"\n❌ Error: Config file not found: {args.config}")
        print("💡 Make sure config.yaml exists in the current directory")
        raise
    except Exception as e:
        logger.error(f"❌ YAML Pipeline failed: {e}")
        raise

 # Recuerda que para ver el mlflow.db debes ejecutar el siguiente comando:
 
# uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5001