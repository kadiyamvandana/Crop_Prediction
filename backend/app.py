from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np


# ============================================================
# 1. CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)


# ============================================================
# 2. LOAD DATASET
# ============================================================

data = pd.read_csv("../dataset/crop_recommendation.csv")


# ============================================================
# 3. FEATURES USED FOR PREDICTION
# ============================================================

features = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]


# ============================================================
# 4. CALCULATE STATISTICAL VALUES
# ============================================================

# Mean for every crop
mean_values = data.groupby("label")[features].mean()

# Standard deviation for every crop
std_values = data.groupby("label")[features].std()

# Number of samples for each crop
crop_counts = data["label"].value_counts()

# Total number of samples
total_samples = len(data)

# Prior probability of each crop
prior_probability = crop_counts / total_samples


# ============================================================
# 5. GAUSSIAN PROBABILITY FUNCTION
# ============================================================

def gaussian_probability(x, mean, std):
    """
    Calculate Gaussian probability density.
    """

    if std == 0 or np.isnan(std):
        return 1.0

    exponent = np.exp(
        -((x - mean) ** 2) / (2 * std ** 2)
    )

    probability = (
        1 / (np.sqrt(2 * np.pi) * std)
    ) * exponent

    return probability


# ============================================================
# 6. CROP PREDICTION FUNCTION
# ============================================================

def predict_crop(user_input):

    results = {}

    # Calculate probability for every crop
    for crop in mean_values.index:

        # Start with prior probability
        total_probability = prior_probability[crop]

        # Calculate likelihood for each feature
        for feature in features:

            mean = mean_values.loc[crop, feature]
            std = std_values.loc[crop, feature]

            probability = gaussian_probability(
                user_input[feature],
                mean,
                std
            )

            total_probability *= probability

        results[crop] = total_probability


    # --------------------------------------------------------
    # Normalize probabilities
    # --------------------------------------------------------

    total = sum(results.values())

    percentages = {}

    if total > 0:

        for crop, value in results.items():
            percentages[crop] = (value / total) * 100

    else:

        for crop in results:
            percentages[crop] = 0


    # --------------------------------------------------------
    # Sort crops by probability
    # --------------------------------------------------------

    sorted_results = sorted(
        percentages.items(),
        key=lambda x: x[1],
        reverse=True
    )


    # --------------------------------------------------------
    # Recommended crop
    # --------------------------------------------------------

    recommended_crop = sorted_results[0][0]

    recommended_probability = sorted_results[0][1]


    # --------------------------------------------------------
    # Z-score analysis
    # --------------------------------------------------------

    z_scores = {}

    for feature in features:

        input_value = user_input[feature]

        mean = mean_values.loc[
            recommended_crop,
            feature
        ]

        std = std_values.loc[
            recommended_crop,
            feature
        ]

        if std == 0 or np.isnan(std):

            z_score = 0

        else:

            z_score = (input_value - mean) / std

        z_scores[feature] = {
            "input": round(float(input_value), 2),
            "mean": round(float(mean), 2),
            "std_dev": round(float(std), 2),
            "z_score": round(float(z_score), 2)
        }


    # --------------------------------------------------------
    # Top 5 crops
    # --------------------------------------------------------

    top_5 = []

    for crop, probability in sorted_results[:5]:

        top_5.append({
            "crop": crop,
            "probability": round(float(probability), 2)
        })


    # --------------------------------------------------------
    # Top 3 crops
    # --------------------------------------------------------

    top_3 = []

    for crop, probability in sorted_results[:3]:

        top_3.append({
            "crop": crop,
            "probability": round(float(probability), 2)
        })


    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "recommended_crop": recommended_crop,
        "recommended_probability": round(
            float(recommended_probability),
            2
        ),
        "top_3": top_3,
        "top_5": top_5,
        "z_scores": z_scores
    }


# ============================================================
# 7. HOME ROUTE
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Crop Prediction API is running successfully!",
        "project": "Crop Prediction Using Probability and Statistical Analysis"
    })


# ============================================================
# 8. PREDICTION API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data from frontend
        user_input = request.get_json()


        # ----------------------------------------------------
        # Check whether all required features are provided
        # ----------------------------------------------------

        for feature in features:

            if feature not in user_input:

                return jsonify({
                    "error": f"Missing value for {feature}"
                }), 400


        # ----------------------------------------------------
        # Convert values to float
        # ----------------------------------------------------

        for feature in features:

            user_input[feature] = float(
                user_input[feature]
            )


        # ----------------------------------------------------
        # Predict crop
        # ----------------------------------------------------

        result = predict_crop(user_input)


        return jsonify(result)


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# 9. RUN SERVER
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("       CROP PREDICTION API")
    print("========================================")
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("========================================\n")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )