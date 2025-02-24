import hashlib
import json

# cd content && find . -name "*.md" | sort | pbcopy
LESSON_PATHS = """
./1-full-course/1-introduction/1-introduction-to-course.md
./1-full-course/1-introduction/2-understanding-dataset-problem.md
./1-full-course/2-data-exploration/1-loading-dataset.md
./1-full-course/2-data-exploration/2-handling-missing-data.md
./1-full-course/2-data-exploration/3-anomaly-outlier-detection.md
./1-full-course/2-data-exploration/4-temporal-coverage-analysis.md
./1-full-course/3-feature-engineering/1-goal-general-considerations.md
./1-full-course/3-feature-engineering/2-one-hot-encoding.md
./1-full-course/3-feature-engineering/3-custom-ordered-categorical.md
./1-full-course/3-feature-engineering/4-numeric-date-features.md
./1-full-course/3-feature-engineering/5-moving-average-lag-features.md
./1-full-course/3-feature-engineering/6-data-imputation-temporal-gaps.md
./1-full-course/4-modeling/1-modeling-introduction.md
./1-full-course/4-modeling/10-stack-of-models.md
./1-full-course/4-modeling/11-generating-forecast.md
./1-full-course/4-modeling/12-forecast-visualization.md
./1-full-course/4-modeling/13-forecast-database-upload.md
./1-full-course/4-modeling/2-simple-heuristics-model.md
./1-full-course/4-modeling/3-general-considerations.md
./1-full-course/4-modeling/4-hyperparameter-optimization.md
./1-full-course/4-modeling/5-gradient-boosted-regression.md
./1-full-course/4-modeling/6-train-test-split.md
./1-full-course/4-modeling/7-grid-search-continued.md
./1-full-course/4-modeling/8-grid-search-visualization.md
./1-full-course/4-modeling/9-training-final-model.md
./1-full-course/5-hands-on-implementation/1-implementation-introduction.md
./1-full-course/5-hands-on-implementation/2-ml-app-overview.md
./1-full-course/5-hands-on-implementation/3-docker-compose-overview.md
./1-full-course/5-hands-on-implementation/4-data-loading-cleanup.md
./1-full-course/5-hands-on-implementation/5-feature-encoding-module.md
./1-full-course/5-hands-on-implementation/6-numeric-features-module.md
./1-full-course/5-hands-on-implementation/7-model-training-module.md
./1-full-course/5-hands-on-implementation/8-forecast-module.md
./1-full-course/5-hands-on-implementation/9-forecast-database-integration.md
./1-full-course/6-ml-app-demo/1-model-library-docker.md
./1-full-course/6-ml-app-demo/2-model-train-module.md
./1-full-course/6-ml-app-demo/3-running-model-train-module.md
./1-full-course/6-ml-app-demo/4-forecast-module.md
./1-full-course/6-ml-app-demo/5-running-forecast-module.md
./1-full-course/7-user-app-demo/1-model-api-fastapi.md
./1-full-course/7-user-app-demo/2-model-dashboard-streamlit.md
./1-full-course/7-user-app-demo/3-dashboard-insights.md
./1-full-course/7-user-app-demo/4-streamlit-dashboard-code.md
./1-full-course/7-user-app-demo/5-course-summary-conclusion.md
"""

SALT = "ai_course_2025"


def strip_lesson_path(input_path) -> str:
    # Strip leading ./
    return input_path.strip().removeprefix("./").removesuffix(".md")


def create_lesson_hash(lesson_path, salt=SALT) -> str:
    """
    Create a hash for a lesson filepath.
    """
    # Combine path with salt
    salted_path = f"{lesson_path}{salt}"

    # Create hash using SHA-256
    hash_object = hashlib.sha256(salted_path.encode())
    return hash_object.hexdigest()[:12]  # Return first 12 chars for shorter IDs


def hash_all_lessons(lesson_paths: str = LESSON_PATHS):
    # Create dictionary mapping paths to their hashes
    lesson_hashes = {
        strip_lesson_path(path): create_lesson_hash(strip_lesson_path(path))
        for path in lesson_paths.strip().split("\n")
    }

    print("Lesson Hashes:")
    print(json.dumps(lesson_hashes, indent=2))

    with open("lesson_hashes.json", "w") as f:
        json.dump(lesson_hashes, f, indent=2)


if __name__ == "__main__":
    hash_all_lessons()
