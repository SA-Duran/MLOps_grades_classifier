# train.py
import os
import sys
import json
import time
import argparse
import random
import logging
from dataclasses import dataclass
from typing import Dict, Any

import numpy as np

from src.exception import CustomException
from src.logger import logging as log  # your configured logger
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
# from src.utils import save_object  # if you need to persist extra artifacts


# ---- Reproducibility ---------------------------------------------------------
def set_seeds(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)


# ---- Config dataclass --------------------------------------------------------
@dataclass
class TrainConfig:
    artifacts_dir: str = "artifacts"
    preprocessor_path: str = os.path.join("artifacts", "preprocessor.pkl")
    model_path: str = os.path.join("artifacts", "model.pkl")
    metrics_path: str = os.path.join("artifacts", "metrics.json")
    seed: int = 42
    test_size: float = 0.2
    # add hyperparams here if you want to pass them down


# ---- Orchestrator ------------------------------------------------------------
class TrainPipeline:
    def __init__(self, cfg: TrainConfig):
        self.cfg = cfg
        os.makedirs(self.cfg.artifacts_dir, exist_ok=True)

        self.ingestion = DataIngestion()
        self.transform = DataTransformation()          # uses its own config for preprocessor path
        self.trainer = ModelTrainer()                  # ensure it can accept/emit paths & metrics

    def run(self) -> Dict[str, Any]:
        t0 = time.perf_counter()
        log.info("==== Training pipeline started ====")
        set_seeds(self.cfg.seed)

        # 1) Ingestion
        log.info("Step 1/3: Data ingestion")
        train_csv, test_csv, aux = self.ingestion.initiate_data_ingestion()
        log.info(f"Ingestion done. Train: {train_csv}, Test: {test_csv}")

        # 2) Transformation (fit on train, transform both)
        log.info("Step 2/3: Data transformation")
        train_arr, test_arr, preproc_path = self.transform.initiate_data_transformation(
            train_path=train_csv, test_path=test_csv
        )
        log.info(f"Preprocessor saved at: {preproc_path}")

        # 3) Training & evaluation
        log.info("Step 3/3: Model training & evaluation")
        metrics = self.trainer.initiate_model_trainer(train_arr, test_arr)
        # Expect `metrics` like {"rmse": ..., "mae": ..., "r2": ...}
        log.info(f"Training finished. Metrics: {metrics}")

        # Optionally persist metrics
        with open(self.cfg.metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        elapsed = time.perf_counter() - t0
        log.info(f"==== Pipeline finished in {elapsed:.1f}s ====")
        return {"metrics": metrics, "preprocessor": preproc_path, "elapsed_sec": elapsed}


# ---- CLI ---------------------------------------------------------------------
def build_argparser():
    p = argparse.ArgumentParser(description="Train pipeline")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--artifacts-dir", type=str, default="artifacts")
    p.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
    # add more args (e.g., hyperparams) as needed
    return p


def main():
    args = build_argparser().parse_args()
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    cfg = TrainConfig(artifacts_dir=args.artifacts_dir, seed=args.seed)

    try:
        pipeline = TrainPipeline(cfg)
        result = pipeline.run()
        # Pretty print to console
        print(json.dumps(result["metrics"], indent=2))
    except CustomException as e:
        log.error(f"CustomException: {e}")
        sys.exit(1)
    except Exception as e:
        log.exception("Unhandled exception during training")
        raise  # or sys.exit(2)


if __name__ == "__main__":
    main()