import os

data = {
    "course": {
        "name": "ML Quest 1: Demand Forecasting",
        "topicGroups": [
            {
                "id": "1-full-course",
                "name": "Full Course",
                "topicSubGroups": [
                    {
                        "id": "1-introduction",
                        "name": "Introduction",
                        "topics": [
                            {
                                "id": "1-introduction-to-course",
                                "name": "Introduction to ML Quest #1 - Demand Forecasting",
                                "content": "Overview of the course objectives and structure",
                                "lesson_hash_id": "intro_001",
                            },
                            {
                                "id": "2-understanding-dataset-problem",
                                "name": "Understanding the Dataset & the Problem to Model",
                                "content": "Introduction to the dataset and the forecasting problem",
                                "lesson_hash_id": "intro_002",
                            },
                        ],
                    },
                    {
                        "id": "2-data-exploration",
                        "name": "Data Exploration",
                        "topics": [
                            {
                                "id": "1-loading-dataset",
                                "name": "Loading the Dataset",
                                "content": "Step-by-step process of loading the dataset",
                                "lesson_hash_id": "data_001",
                            },
                            {
                                "id": "2-handling-missing-data",
                                "name": "Handling Missing Data",
                                "content": "Techniques to manage missing data",
                                "lesson_hash_id": "data_002",
                            },
                            {
                                "id": "3-anomaly-outlier-detection",
                                "name": "Anomaly and Outlier Detection",
                                "content": "Methods for identifying and addressing anomalies",
                                "lesson_hash_id": "data_003",
                            },
                            {
                                "id": "4-temporal-coverage-analysis",
                                "name": "Temporal Coverage and Distribution Analysis",
                                "content": "Analyzing time-based data coverage and distributions",
                                "lesson_hash_id": "data_004",
                            },
                        ],
                    },
                    {
                        "id": "3-feature-engineering",
                        "name": "Feature Engineering",
                        "topics": [
                            {
                                "id": "1-goal-general-considerations",
                                "name": "Our Goal & General Considerations",
                                "content": "Defining objectives for feature engineering",
                                "lesson_hash_id": "feat_001",
                            },
                            {
                                "id": "2-one-hot-encoding",
                                "name": "One-Hot Encoding",
                                "content": "Encoding categorical data",
                                "lesson_hash_id": "feat_002",
                            },
                            {
                                "id": "3-custom-ordered-categorical",
                                "name": "Custom Ordered Categorical Encoder",
                                "content": "Creating custom encoders",
                                "lesson_hash_id": "feat_003",
                            },
                            {
                                "id": "4-numeric-date-features",
                                "name": "Numeric & Date Features",
                                "content": "Engineering numeric and date-based features",
                                "lesson_hash_id": "feat_004",
                            },
                            {
                                "id": "5-moving-average-lag-features",
                                "name": "Moving Average & Lag Features",
                                "content": "Creating lag-based features for forecasting",
                                "lesson_hash_id": "feat_005",
                            },
                            {
                                "id": "6-data-imputation-temporal-gaps",
                                "name": "Data Imputation for Temporal Gaps",
                                "content": "Handling gaps in time-series data",
                                "lesson_hash_id": "feat_006",
                            },
                        ],
                    },
                    {
                        "id": "4-modeling",
                        "name": "Modeling",
                        "topics": [
                            {
                                "id": "1-modeling-introduction",
                                "name": "Introduction",
                                "content": "Overview of modeling techniques",
                                "lesson_hash_id": "model_001",
                            },
                            {
                                "id": "2-simple-heuristics-model",
                                "name": "Create a Model Using Simple Heuristics",
                                "content": "Building a baseline model",
                                "lesson_hash_id": "model_002",
                            },
                            {
                                "id": "3-general-considerations",
                                "name": "General Considerations",
                                "content": "Key considerations for modeling",
                                "lesson_hash_id": "model_003",
                            },
                            {
                                "id": "4-hyperparameter-optimization",
                                "name": "Grid Search for Hyperparameter Optimization",
                                "content": "Using grid search to optimize models",
                                "lesson_hash_id": "model_004",
                            },
                            {
                                "id": "5-gradient-boosted-regression",
                                "name": "Gradient Boosted Regression",
                                "content": "Introduction to gradient boosted models",
                                "lesson_hash_id": "model_005",
                            },
                            {
                                "id": "6-train-test-split",
                                "name": "Train-Test Split for Timeseries Data",
                                "content": "Splitting data for time-series models",
                                "lesson_hash_id": "model_006",
                            },
                            {
                                "id": "7-grid-search-continued",
                                "name": "Grid Search Continued",
                                "content": "Continuing the grid search process",
                                "lesson_hash_id": "model_007",
                            },
                            {
                                "id": "8-grid-search-visualization",
                                "name": "Visualizing & Interpreting Grid Search Results",
                                "content": "Analyzing grid search results",
                                "lesson_hash_id": "model_008",
                            },
                            {
                                "id": "9-training-final-model",
                                "name": 'Training the "Final Model"',
                                "content": "Building and training the final model",
                                "lesson_hash_id": "model_009",
                            },
                            {
                                "id": "10-stack-of-models",
                                "name": "Training a Stack of Models",
                                "content": "Combining models for improved forecasting",
                                "lesson_hash_id": "model_010",
                            },
                            {
                                "id": "11-generating-forecast",
                                "name": "Generating the Forecast",
                                "content": "Creating forecasts from the model",
                                "lesson_hash_id": "model_011",
                            },
                            {
                                "id": "12-forecast-visualization",
                                "name": "Visualizing the Forecast",
                                "content": "Interpreting and visualizing model outputs",
                                "lesson_hash_id": "model_012",
                            },
                            {
                                "id": "13-forecast-database-upload",
                                "name": "Uploading Forecast to Postgres",
                                "content": "Saving forecasts to a database",
                                "lesson_hash_id": "model_013",
                            },
                        ],
                    },
                    {
                        "id": "5-hands-on-implementation",
                        "name": "Hands-On Implementation",
                        "topics": [
                            {
                                "id": "1-implementation-introduction",
                                "name": "Introduction",
                                "content": "Overview of hands-on implementation",
                                "lesson_hash_id": "hands_001",
                            },
                            {
                                "id": "2-ml-app-overview",
                                "name": "ML App Overview",
                                "content": "Introduction to the ML app structure",
                                "lesson_hash_id": "hands_002",
                            },
                            {
                                "id": "3-docker-compose-overview",
                                "name": "Docker Compose App Overview",
                                "content": "Using Docker Compose for ML apps",
                                "lesson_hash_id": "hands_003",
                            },
                            {
                                "id": "4-data-loading-cleanup",
                                "name": "Data Loading & Cleanup Module",
                                "content": "Implementing the data loading pipeline",
                                "lesson_hash_id": "hands_004",
                            },
                            {
                                "id": "5-feature-encoding-module",
                                "name": "Feature Encoding Module",
                                "content": "Encoding features for the ML model",
                                "lesson_hash_id": "hands_005",
                            },
                            {
                                "id": "6-numeric-features-module",
                                "name": "Numeric Features Module",
                                "content": "Engineering numeric features",
                                "lesson_hash_id": "hands_006",
                            },
                            {
                                "id": "7-model-training-module",
                                "name": "Model Training Module",
                                "content": "Building the training module",
                                "lesson_hash_id": "hands_007",
                            },
                            {
                                "id": "8-forecast-module",
                                "name": "Model Forecast Module",
                                "content": "Generating and saving forecasts",
                                "lesson_hash_id": "hands_008",
                            },
                            {
                                "id": "9-forecast-database-integration",
                                "name": "Forecast Database Integration",
                                "content": "Integrating forecasts with the database",
                                "lesson_hash_id": "hands_009",
                            },
                        ],
                    },
                    {
                        "id": "6-ml-app-demo",
                        "name": "ML App Demo & Walk-Through",
                        "topics": [
                            {
                                "id": "1-model-library-docker",
                                "name": "Model Library Docker App",
                                "content": "Overview of the model library",
                                "lesson_hash_id": "demo_001",
                            },
                            {
                                "id": "2-model-train-module",
                                "name": "Model Train Module",
                                "content": "Details of the training module",
                                "lesson_hash_id": "demo_002",
                            },
                            {
                                "id": "3-running-model-train-module",
                                "name": "Running the Model Train Module",
                                "content": "Executing the training process",
                                "lesson_hash_id": "demo_003",
                            },
                            {
                                "id": "4-forecast-module",
                                "name": "Model Forecast Module",
                                "content": "Details of the forecasting module",
                                "lesson_hash_id": "demo_004",
                            },
                            {
                                "id": "5-running-forecast-module",
                                "name": "Running the Model Forecast Module",
                                "content": "Executing the forecasting process",
                                "lesson_hash_id": "demo_005",
                            },
                        ],
                    },
                    {
                        "id": "7-user-app-demo",
                        "name": "User App Demo / Walk-Through",
                        "topics": [
                            {
                                "id": "1-model-api-fastapi",
                                "name": "Model API with FastAPI on Docker",
                                "content": "Implementing a model API",
                                "lesson_hash_id": "user_001",
                            },
                            {
                                "id": "2-model-dashboard-streamlit",
                                "name": "Model Dashboard with Streamlit on Docker",
                                "content": "Building a dashboard for the model",
                                "lesson_hash_id": "user_002",
                            },
                            {
                                "id": "3-dashboard-insights",
                                "name": "Model Dashboard Insights",
                                "content": "Interpreting insights from the dashboard",
                                "lesson_hash_id": "user_003",
                            },
                            {
                                "id": "4-streamlit-dashboard-code",
                                "name": "Streamlit Dashboard Code",
                                "content": "Code walk-through of the dashboard",
                                "lesson_hash_id": "user_004",
                            },
                            {
                                "id": "5-course-summary-conclusion",
                                "name": "Course Summary & Conclusion",
                                "content": "Summarizing key learnings",
                                "lesson_hash_id": "user_005",
                            },
                        ],
                    },
                ],
            }
        ],
    }
}


# Base directory
base_dir = "content"


# Function to create markdown files
def create_markdown_files(course_data):
    for topic_group in course_data["course"]["topicGroups"]:
        group_dir = os.path.join(base_dir, topic_group["id"])
        os.makedirs(group_dir, exist_ok=True)

        for sub_group in topic_group["topicSubGroups"]:
            sub_group_dir = os.path.join(group_dir, sub_group["id"])
            os.makedirs(sub_group_dir, exist_ok=True)

            for topic in sub_group["topics"]:
                file_path = os.path.join(sub_group_dir, f"{topic['id']}.md")
                with open(file_path, "w") as file:
                    file.write(f"# {sub_group['name']}\n\n")
                    file.write(f"## {topic['name']}\n\n")
                    file.write(f"{topic['content']}.\n")


# Create the markdown files
if __name__ == "__main__":
    response = input(
        "This will replace all markdown files in the 'content' directory. Continue? (y/n): "
    )
    if response.lower() == "y":
        create_markdown_files(data)
        print("Markdown files created successfully!")
    else:
        print("Operation cancelled.")
