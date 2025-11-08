**Kissan Mitra AI: Crop Recommendation System for Indian Farmers**

This project is a multi-agent AI system built using the Google Agent Development Kit (ADK) designed to provide Indian farmers with data-driven, actionable crop recommendations. The system ensures recommendations are not only suitable for the local climate but are also the most profitable choice among the top candidates.

**Key Features:**

Three-Stage Pipeline: The system uses a specialized 3-stage sequential pipeline to ensure high-quality recommendations:

Region & Weather Data Acquisition

Weather Suitability Scoring (Ranks top candidates based on temperature, soil, and humidity)

Price Optimization (Filters candidates based on historical sales revenue for the final selection)

Seasonal Recommendations: Provides distinct, single best-crop recommendations for both Winter and Summer cycles.

Tool-Driven Logic: All data reading, scoring, and filtering logic is handled by pure Python tools (pandas based) for speed, accuracy, and deterministic output.

ADK Web Ready: Project structure is optimized for immediate deployment and testing via the Google ADK Web interface.

**Project Structure**

The project maintains a modular structure, separating roles for clarity and maintainability:

```
basic_agent/region_agent/
├──sub_pipeline/
|   ├──sub_pipeline.py
|   ├── sub_agents/             # Defines all LlmAgent and their instructions (Root, Weather, Crop, Sales)
│       ├── crop_agent/
|       ├── agent.py
│       └── ... (other agents)
├── data_setup.py       # Defines all CSV paths (Weather, Crop, Sales) and state keys.
│   
├── data/               # Static CSV rule files (must be present for tools to work)
│   ├── weather_data.csv    # Climate and soil data by region.
│   ├── crop_suitability.csv# Crop requirements data.
│   └── crop_sales.csv      # Historical average revenue by crop type.
```

**Setup and Installation**

**Prerequisites**:

Python 3.9+

Google ADK CLI installed (google-adk)

Access to a Google Gemini API Key

The three required data CSV files (weather_data.csv, crop_suitability.csv, sales_data.csv) placed in the core/ directory.

**Installation Steps**

1. Clone the Repository:

git clone [https://github.com/dna-lak/Kissan_MitraAI.git](https://github.com/dna-lak/Kissan_MitraAI.git)
cd Kissan_MitraAI


2. Set up the Environment and Install Dependencies:

python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt 


3. Configure API Key:

export GEMINI_API_KEY="YOUR_API_KEY_HERE"


**Running the Application (ADK Web)**

Choose the basic_agent directory in terminal
Run the following command: adk web

Test the Agent: Initiate the conversation with a location-based query:

Example Input: "I am from Ponda"

**Detailed Workflow Execution (sub_pipeline)**

The system executes the agents in a strict sequence to build the recommendation:

Steps:

1

weather_agent uses the tool get_avg_weather.

avg_weather_data state key is updated.

Fetches climate, soil, and temp data for the requested region from weather_data.csv.

2

crop_agent uses the tool determine_best_crop

recommendation_candidates state key is updated with both summer and winter candidates, by comparing with crop_suitability.csv

Scores all crops against the climate data and saves the top 3 suitable crops for each season (Summer/Winter).

3

market_agent uses the tool determine_most_profitable_crop

final_profitable_crop state key is updated.

Filters the top 3 candidates (from Step 2) using crop_sales.csv to select the single highest-revenue crop for each season.
