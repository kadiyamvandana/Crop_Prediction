import { useState } from "react";
import axios from "axios";

function App() {
  const [showPrediction, setShowPrediction] = useState(false);
  const [showResult, setShowResult] = useState(false);

  const [formData, setFormData] = useState({
    N: "",
    P: "",
    K: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        {
          N: Number(formData.N),
          P: Number(formData.P),
          K: Number(formData.K),
          temperature: Number(formData.temperature),
          humidity: Number(formData.humidity),
          ph: Number(formData.ph),
          rainfall: Number(formData.rainfall),
        }
      );

      console.log("Prediction Result:", response.data);

      setResult(response.data);
      setShowResult(true);

    } catch (error) {
      console.error("Prediction Error:", error);

      alert(
        "Unable to connect to the prediction server. Please make sure the Flask backend is running."
      );

    } finally {
      setLoading(false);
    }
  };

  const goHome = () => {
    setShowPrediction(false);
    setShowResult(false);
    setResult(null);
  };

  return (
    <div className="app">

      {/* NAVBAR */}

      <nav className="navbar">

        <div
          className="logo"
          onClick={goHome}
        >
          🌱 CropPredict
        </div>

        <div className="nav-links">

          <span onClick={goHome}>
            Home
          </span>

          <span>
            About
          </span>

        </div>

      </nav>


      {/* HOME PAGE */}

      {!showPrediction && !showResult && (

        <main className="hero">

          <div className="hero-content">

            <div className="badge">
              📊 Probability & Statistics
            </div>

            <h1>
              Smart Crop
              <br />
              <span>Prediction System</span>
            </h1>

            <p>
              Discover the most suitable crop for your soil
              and environmental conditions using probability
              and statistical analysis.
            </p>

            <button
              className="start-button"
              onClick={() => setShowPrediction(true)}
            >
              🌾 Start Prediction
            </button>


            <div className="features">

              <div className="feature-card">

                <div className="feature-icon">
                  📈
                </div>

                <h3>
                  Statistical Analysis
                </h3>

                <p>
                  Mean, standard deviation and z-score
                  based analysis.
                </p>

              </div>


              <div className="feature-card">

                <div className="feature-icon">
                  🎯
                </div>

                <h3>
                  Probability Based
                </h3>

                <p>
                  Calculate the probability of suitable
                  crops from historical data.
                </p>

              </div>


              <div className="feature-card">

                <div className="feature-icon">
                  🌱
                </div>

                <h3>
                  Smart Recommendation
                </h3>

                <p>
                  Get the top crops suitable for your
                  given conditions.
                </p>

              </div>

            </div>

          </div>

        </main>

      )}


      {/* PREDICTION FORM */}

      {showPrediction && !showResult && (

        <main className="prediction-page">

          <div className="prediction-container">

            <div className="prediction-header">

              <div className="badge">
                🌾 Crop Analysis
              </div>

              <h1>
                Enter Your <span>Conditions</span>
              </h1>

              <p>
                Provide your soil and environmental values
                to find the most suitable crop.
              </p>

            </div>


            <form
              className="prediction-form"
              onSubmit={handleSubmit}
            >

              <div className="input-group">

                <label>
                  Nitrogen (N)
                </label>

                <input
                  type="number"
                  name="N"
                  placeholder="Example: 90"
                  value={formData.N}
                  onChange={handleChange}
                  required
                />

                <small>
                  Amount of nitrogen present in the soil.
                </small>

              </div>


              <div className="input-group">

                <label>
                  Phosphorus (P)
                </label>

                <input
                  type="number"
                  name="P"
                  placeholder="Example: 42"
                  value={formData.P}
                  onChange={handleChange}
                  required
                />

                <small>
                  Amount of phosphorus present in the soil.
                </small>

              </div>


              <div className="input-group">

                <label>
                  Potassium (K)
                </label>

                <input
                  type="number"
                  name="K"
                  placeholder="Example: 43"
                  value={formData.K}
                  onChange={handleChange}
                  required
                />

                <small>
                  Amount of potassium present in the soil.
                </small>

              </div>


              <div className="input-group">

                <label>
                  Temperature (°C)
                </label>

                <input
                  type="number"
                  step="0.1"
                  name="temperature"
                  placeholder="Example: 25.5"
                  value={formData.temperature}
                  onChange={handleChange}
                  required
                />

                <small>
                  Average temperature of the area.
                </small>

              </div>


              <div className="input-group">

                <label>
                  Humidity (%)
                </label>

                <input
                  type="number"
                  step="0.1"
                  name="humidity"
                  placeholder="Example: 80"
                  value={formData.humidity}
                  onChange={handleChange}
                  required
                />

                <small>
                  Moisture level present in the air.
                </small>

              </div>


              <div className="input-group">

                <label>
                  Soil pH
                </label>

                <input
                  type="number"
                  step="0.1"
                  name="ph"
                  placeholder="Example: 6.5"
                  value={formData.ph}
                  onChange={handleChange}
                  required
                />

                <small>
                  Acidity or alkalinity of the soil.
                </small>

              </div>


              <div className="input-group">

                <label>
                  Rainfall (mm)
                </label>

                <input
                  type="number"
                  step="0.1"
                  name="rainfall"
                  placeholder="Example: 200"
                  value={formData.rainfall}
                  onChange={handleChange}
                  required
                />

                <small>
                  Expected rainfall in the region.
                </small>

              </div>


              <button
                type="submit"
                className="predict-button"
                disabled={loading}
              >

                {loading
                  ? "🔄 Analyzing..."
                  : "🔮 Predict Best Crop"}

              </button>

            </form>


            <button
              className="back-button"
              onClick={goHome}
            >
              ← Back to Home
            </button>

          </div>

        </main>

      )}


      {/* RESULT PAGE */}

      {showResult && result && (

        <main className="result-page">

          <div className="result-container">

            <div className="badge">
              🎯 Prediction Complete
            </div>

            <h1>
              Your Recommended <span>Crop</span>
            </h1>

            <p className="result-subtitle">
              Based on probability and statistical analysis
            </p>


            {/* MAIN RESULT */}

            <div className="main-result-card">

              <div className="crop-icon">
                🌱
              </div>

              <p className="recommended-label">
                MOST SUITABLE CROP
              </p>

              <h2>
                {result.recommended_crop}
              </h2>

              <div className="probability">
                {result.recommended_probability}%
              </div>

              <p>
                Probability of suitability
              </p>

            </div>


            {/* TOP 3 */}

            <div className="top-crops-card">

              <h2>
                📊 Top 3 Crop Predictions
              </h2>

              {result.top_3.map((crop, index) => (

                <div
                  className="crop-row"
                  key={crop.crop}
                >

                  <div className="crop-name">
                    <span>
                      {index + 1}
                    </span>

                    {crop.crop}
                  </div>

                  <div className="crop-percentage">
                    {crop.probability}%
                  </div>

                </div>

              ))}

            </div>


            {/* STATISTICS */}

            <div className="statistics-card">

              <h2>
                📈 Statistical Analysis
              </h2>

              <p>
                Z-score analysis for the recommended crop
              </p>

              <div className="statistics-table">

                <div className="table-header">
                  <span>Feature</span>
                  <span>Input</span>
                  <span>Mean</span>
                  <span>Std Dev</span>
                  <span>Z-Score</span>
                </div>

                {Object.entries(result.z_scores).map(
                  ([feature, values]) => (

                    <div
                      className="table-row"
                      key={feature}
                    >

                      <span>
                        {feature}
                      </span>

                      <span>
                        {values.input}
                      </span>

                      <span>
                        {values.mean}
                      </span>

                      <span>
                        {values.std_dev}
                      </span>

                      <span>
                        {values.z_score}
                      </span>

                    </div>

                  )
                )}

              </div>

            </div>


            <button
              className="predict-again-button"
              onClick={() => {
                setShowResult(false);
                setShowPrediction(true);
              }}
            >
              🔄 Predict Again
            </button>


            <button
              className="back-button"
              onClick={goHome}
            >
              ← Back to Home
            </button>

          </div>

        </main>

      )}


      <footer>
        <p>
          CropPredict • Probability & Statistical Analysis
        </p>
      </footer>

    </div>
  );
}

export default App;