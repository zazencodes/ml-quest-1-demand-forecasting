import argparse

from model_train import train_models
from model_predict import generate_forecast

parser = argparse.ArgumentParser(description="Train models or generate predictions.")
parser.add_argument(
    "action",
    choices=["train", "predict"],
    help="Action to perform: 'train' to train models or 'predict' to generate predictions.",
)
args = parser.parse_args()

if args.action == "train":
    print("Call to meal_demand train")
    train_models()
elif args.action == "predict":
    print("Call to meal_demand predict")
    generate_forecast()
