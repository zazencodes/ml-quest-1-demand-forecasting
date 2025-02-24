import json


def merge_course_hashes(course_map_path, hash_map_path, output_path):
    """
    Merge course map JSON with hash IDs from hash map JSON.

    Args:
        course_map_path (str): Path to course map JSON file
        hash_map_path (str): Path to hash map JSON file
        output_path (str): Path to save merged JSON file
    """
    # Load both JSON files
    print(f"Reading {course_map_path}")
    with open(course_map_path, "r") as f:
        course_map = json.load(f)

    print(f"Reading {hash_map_path}")
    with open(hash_map_path, "r") as f:
        hash_map = json.load(f)

    def add_hash_to_topic(topic, topic_group_id, topic_subgroup_id):
        """Add hash ID to a topic based on its path"""
        # Construct the path that matches the hash map format
        topic_path = f"{topic_group_id}/{topic_subgroup_id}/{topic['id']}"

        # Add the hash ID if it exists in the hash map
        if topic_path in hash_map:
            topic["lesson_hash_id"] = hash_map[topic_path]
        return topic

    # Iterate through the course structure
    for topic_group in course_map["course"]["topicGroups"]:
        topic_group_id = topic_group["id"]

        for subgroup in topic_group["topicSubGroups"]:
            subgroup_id = subgroup["id"]

            # Update each topic with its hash ID
            subgroup["topics"] = [
                add_hash_to_topic(topic, topic_group_id, subgroup_id)
                for topic in subgroup["topics"]
            ]

    # Save the updated course map
    print(f"Writing {output_path}")
    with open(output_path, "w") as f:
        json.dump(course_map, f, indent=2)


if __name__ == "__main__":
    merge_course_hashes(
        "ml_quest_1_demand_forecasting.json",
        "lesson_hashes.json",
        "ml_quest_1_demand_forecasting_updated.json",
    )
