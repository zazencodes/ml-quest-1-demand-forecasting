import json
from pathlib import Path


def main():
    fp = Path("ml_quest_1_demand_forecasting.json")

    json_data = json.loads(fp.read_text())

    answer = input(
        "Loaded JSON from ml_quest_1_demand_forecasting.json. Will replace file now. (y/n)"
    )
    if answer != "y":
        return

    # Function to add video_file to each topic
    def add_video_file(data):
        for topic_group in data["course"]["topicGroups"]:
            for subgroup in topic_group["topicSubGroups"]:
                for topic in subgroup["topics"]:
                    topic["video_file"] = f"{topic['id']}.mp4"
                    topic["has_preview_video"] = False

    # Modify the JSON data
    add_video_file(json_data)

    fp.write_text(json.dumps(json_data, indent=2))

    print("Replaced file ml_quest_1_demand_forecasting.json")


if __name__ == "__main__":
    main()
