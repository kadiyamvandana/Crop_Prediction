import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD DATASET
# ============================================================

data = pd.read_csv("../dataset/crop_recommendation.csv")

print("\n========================================")
print("       CROP PREDICTION PROJECT")
print("   Probability & Statistical Analysis")
print("========================================")


# ============================================================
# 2. DISPLAY BASIC DATASET INFORMATION
# ============================================================

print("\nDataset Shape:")
print(data.shape)

print("\nDataset Columns:")
print(list(data.columns))

print("\nCrop Names:")
print(data["label"].unique())

print("\nNumber of Samples for Each Crop:")
print(data["label"].value_counts())


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
# 4. CALCULATE MEAN FOR EACH CROP
# ============================================================

mean_values = data.groupby("label")[features].mean()

print("\n========================================")
print("             MEAN VALUES")
print("========================================")

print(mean_values)


# ============================================================
# 5. CALCULATE STANDARD DEVIATION
# ============================================================

std_values = data.groupby("label")[features].std()

print("\n========================================")
print("       STANDARD DEVIATION VALUES")
print("========================================")

print(std_values)


# ============================================================
# 6. CALCULATE PRIOR PROBABILITY
# ============================================================

crop_counts = data["label"].value_counts()
total_samples = len(data)

prior_probability = crop_counts / total_samples

print("\n========================================")
print("          PRIOR PROBABILITY")
print("========================================")

for crop, probability in prior_probability.items():
    print(f"{crop}: {probability:.4f}")


# ============================================================
# 7. GAUSSIAN PROBABILITY FUNCTION
# ============================================================

def gaussian_probability(x, mean, std):
    """
    Calculate Gaussian probability density.

    x    = input value
    mean = mean value of the crop
    std  = standard deviation of the crop
    """

    # Prevent division by zero
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
# 8. USER INPUT
# ============================================================

user_input = {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 25.5,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200
}


print("\n========================================")
print("             USER INPUT")
print("========================================")

for feature, value in user_input.items():
    print(f"{feature}: {value}")


# ============================================================
# 9. CALCULATE CROP PROBABILITY
# ============================================================

results = {}

for crop in mean_values.index:

    # Start with prior probability
    total_probability = prior_probability[crop]

    # Calculate likelihood for every feature
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


# ============================================================
# 10. NORMALIZE PROBABILITIES
# ============================================================

total = sum(results.values())

percentages = {}

if total > 0:

    for crop, value in results.items():
        percentages[crop] = (value / total) * 100

else:

    for crop in results:
        percentages[crop] = 0


# ============================================================
# 11. SORT CROPS BY PROBABILITY
# ============================================================

sorted_results = sorted(
    percentages.items(),
    key=lambda x: x[1],
    reverse=True
)


# ============================================================
# 12. DISPLAY FINAL PREDICTION
# ============================================================

print("\n========================================")
print("          CROP PREDICTION")
print("========================================")

for crop, probability in sorted_results[:5]:

    print(
        f"{crop.capitalize():15s} : "
        f"{probability:.2f}%"
    )


# ============================================================
# 13. RECOMMENDED CROP
# ============================================================

recommended_crop = sorted_results[0][0]
recommended_probability = sorted_results[0][1]

print("\n========================================")
print("       RECOMMENDED CROP")
print("========================================")

print(
    f"Crop        : {recommended_crop.capitalize()}"
)

print(
    f"Probability : {recommended_probability:.2f}%"
)


# ============================================================
# 14. Z-SCORE ANALYSIS
# ============================================================

print("\n========================================")
print("           Z-SCORE ANALYSIS")
print("========================================")

print(
    f"\nAnalysis for recommended crop: "
    f"{recommended_crop.capitalize()}"
)

print(
    "\nFeature             Input       Mean       Std Dev       Z-score"
)
print("-" * 70)


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

    print(
        f"{feature:15s}"
        f"{input_value:10.2f}"
        f"{mean:12.2f}"
        f"{std:13.2f}"
        f"{z_score:13.2f}"
    )


# ============================================================
# 15. TOP 3 CROPS
# ============================================================

print("\n========================================")
print("             TOP 3 CROPS")
print("========================================")

for position, (crop, probability) in enumerate(
    sorted_results[:3],
    start=1
):

    print(
        f"{position}. "
        f"{crop.capitalize():12s} "
        f"→ {probability:.2f}%"
    )


# ============================================================
# 16. PROJECT COMPLETED
# ============================================================

print("\n========================================")
print("       ANALYSIS COMPLETED SUCCESSFULLY")
print("========================================")