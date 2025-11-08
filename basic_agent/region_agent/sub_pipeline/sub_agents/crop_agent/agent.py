

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ....data_setup import RECOMMENDATION_KEY_NAME

import pandas as pd
from google.adk.tools import ToolContext
from ....data_setup import STATE_KEY_NAME, WEATHER_KEY_NAME, RECOMMENDATION_KEY_NAME, WEATHER_CSV_PATH, CROP_CSV_PATH, REGIONS

Climate_Zone = {
    "Tropical Wet-Dry": 70, "Humid Subtropical": 70, "Subtropical": 60, 
    "Tropical Monsoon": 75, "Arid/Tropical Wet-Dry": 35, "Subtropical Semi-Arid": 45, 
    "Humid Subtropical/Alpine": 65, "Arid/Desert": 15, "Tropical Wet": 90, 
    "Temperate/Alpine": 55, "Cold Desert/Alpine": 40, "Tropical Maritime": 85
}

def determine_best_crop(tool_context: ToolContext) -> dict:
    """
    Reads weather data from state and uses the crop rules to find the best match.
    Returns a dictionary representing the tool's result.
    """

    weather = tool_context.state.get(WEATHER_KEY_NAME)
    region_key = tool_context.state.get(STATE_KEY_NAME)
    
    if not weather:
        return {"status": "error", "error_message": "Average weather data not found in state."}

    try:
        crop_df = pd.read_csv(CROP_CSV_PATH)
        
        # Initialize scores
        winter_crop_scores = {}
        summer_crop_scores = {}
        best_crop_cycle = {}
        
        # Extract and validate weather data keys (assuming keys like Avg_Summer_Temp_C exist in WEATHER_FILE)
        avg_summer_temp = weather.get('Avg_Summer_Temp_C', 0)
        avg_winter_temp = weather.get('Avg_Winter_Temp_C', 0)
        # precipitation = weather.get('Precipitation', 0) # Not used in the scoring logic below
        soil_type_str = weather.get('Soil_Type', '').lower()
        climate_zone = weather.get('Climate_Zone', '')
        
        # Get climate humidity or default to 0
        climate_humidity = Climate_Zone.get(climate_zone, 0)

        for _, row in crop_df.iterrows():
            
            # Initialized correctly here for each crop iteration
            summer_score = 0 
            winter_score = 0
            
            # --- Score 1: Temperature Match (using +/- 2 tolerance) ---
            target_temp = row.get('Temperature', 0)
            
            # Check Summer Temperature
            if (target_temp - 2) <= avg_summer_temp <= (target_temp + 2):
                summer_score += 3
            else:
                summer_score -=3
            
            # Check Winter Temperature
            if (target_temp - 2) <= avg_winter_temp <= (target_temp + 2):
                winter_score += 3
            else:
                winter_score -=3

            # --- Score 2: Humidity Match (using +/- 5 tolerance) ---
            target_humidity = row.get('Humidity', 0)
            max_humidity = row.get('MaxHumidity', 100) # Added max humidity check for original logic
            
            # The original logic was complex/had errors, simplifying to a general humidity match:
            if (target_humidity - 5) <= climate_humidity <= (max_humidity + 5):
                summer_score += 1
                winter_score += 1
            else:
                summer_score -= 1
                winter_score -= 1
            
            # --- Score 3: Soil Type Match ---
            target_soil = row.get('Soil_Type', '').lower()
            
            # Check against keywords in the region's soil_type string
            soil_match = False
            if target_soil == "red" and any(st in soil_type_str for st in ["red", "laterite", "mountain"]):
                soil_match = True
            elif target_soil == "black" and ("black" in soil_type_str):
                soil_match = True
            elif target_soil == "loamy" and ("alluvial" in soil_type_str):
                soil_match = True
            elif target_soil == "sandy" and any(st in soil_type_str for st in ["desert", "sandy"]):
                soil_match = True
            elif target_soil == "clayey" and ("black" in soil_type_str):
                soil_match = True
            
            if soil_match:
                summer_score += 1
                winter_score += 1
            else:
                summer_score -= 1
                winter_score -= 1

            # Store scores (assuming 'Crop_Type' is the correct column name for the crop)
            crop_type = row.get('Crop_Type', row.get('Crop', 'Unknown')) 
            winter_crop_scores[crop_type] = winter_score
            summer_crop_scores[crop_type] = summer_score
        
        # --- Final Recommendation Logic ---

        sorted_winter_scores = dict(sorted(winter_crop_scores.items(), key=lambda item: item[1], reverse=True))
        sorted_summer_scores = dict(sorted(summer_crop_scores.items(), key=lambda item: item[1], reverse=True))
        
        # Extract top 3 crops, handling cases with fewer than 3 entries
        best_summer_crops = list(sorted_summer_scores.keys())[:3] 
        best_winter_crops = list(sorted_winter_scores.keys())[:3]
        
        best_crop_cycle["summer"] = best_summer_crops
        best_crop_cycle["winter"] = best_winter_crops
        
        final_result = {
            "region": region_key,
            "weather_summary": weather,
            "recommendation": best_crop_cycle,
            "reason": f"Potential crop cycles of {best_crop_cycle} were chosen based on average conditions."
        }
        
        tool_context.state[RECOMMENDATION_KEY_NAME] = final_result

        # Return a success dictionary
        return {
            "status": "success",
            "message": "Crop determination logic executed successfully.",
            "final_recommendation": final_result
        }
        
    except Exception as e:
        return {"status": "error", "error_message": f"Error calculating crop recommendation: {e}"}
# --- Agent Definition ---
crop_agent = Agent(
    name="crop_agent",
    model='gemini-2.5-flash',
    instruction=f"""
    You are the final Crop Recommendation Expert.
    1. **You must call the determine_best_crop tool first** to execute the crop matching logic.
    2. Read the final recommendation from the state key '{RECOMMENDATION_KEY_NAME}'.
    3. Present a helpful, clear, and encouraging response to the farmer based ONLY on the tool's output.
    """,
    tools=[determine_best_crop]
)