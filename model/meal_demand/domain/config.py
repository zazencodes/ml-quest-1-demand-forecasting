from dataclasses import dataclass
from pathlib import Path


@dataclass
class ModelHyperparams:
    learning_rate: float
    max_depth: int
    min_samples_split: int
    n_estimators: int
    subsample: float


@dataclass
class Config:
    data_path: Path
    artifacts_path: Path
    model_params: ModelHyperparams | None = None
