from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    model_id: str
    data_path: Path
    artifacts_path: Path
