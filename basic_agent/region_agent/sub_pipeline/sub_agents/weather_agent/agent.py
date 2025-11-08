

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

import pandas as pd
from google.adk.tools import ToolContext
# Note: ToolResult import removed

from ....data_setup import STATE_KEY_NAME, WEATHER_KEY_NAME, RECOMMENDATION_KEY_NAME, WEATHER_CSV_PATH, CROP_CSV_PATH, REGIONS

Climate_Zones = {
    "Tropical Wet-Dry": 70, "Humid Subtropical": 70, "Subtropical": 60, 
    "Tropical Monsoon": 75, "Arid/Tropical Wet-Dry": 35, "Subtropical Semi-Arid": 45, 
    "Humid Subtropical/Alpine": 65, "Arid/Desert": 15, "Tropical Wet": 90, 
    "Temperate/Alpine": 55, "Cold Desert/Alpine": 40, "Tropical Maritime": 85
}

# --- Tool 1: Weather Data Aggregation ---
def get_avg_weather(tool_context: ToolContext) -> dict:
    """
    Reads the region key from the shared state and retrieves weather data.
    Returns a dictionary representing the tool's result.
    """
    region_key = tool_context.state.get(STATE_KEY_NAME)

    if not region_key or region_key not in REGIONS:
        # Return an error dictionary instead of ToolResult
        return {"status": "error", "error_message": f"Region key '{region_key}' is invalid or missing in state. Cannot proceed."}

    try:
        df = pd.read_csv(WEATHER_CSV_PATH)
        
        # Filter for the specific region requested
        region_data = df[
            df['Region'] == region_key
        ].round(1)
        
        if region_data.empty:
            return {"status": "error", "error_message": f"Weather data not found for region: {region_key}."}
            
        # Convert the filtered row to a dictionary
        weather = region_data.drop(columns=['Region']).to_dict('records')[0]
        
        # Write the data to state
        tool_context.state[WEATHER_KEY_NAME] = weather
        
        # Return a success dictionary
        return {
            "status": "success", 
            "message": f"Aggregated weather data for {region_key} is now available in state.",
            "data": weather
        }
        
    except Exception as e:
        # 🔑 THIS IS THE CRITICAL DEBUGGING SECTION:
        # 1. Print the full traceback to the execution logs
        print("\n--- TOOL EXECUTION ERROR DEBUG ---")
        print(f"Exception Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        print(f"Full Traceback:\n{traceback.format_exc()}")
        print("---------------------------------\n")

        # 2. Return an error message indicating a processing failure
        return {"status": "error", "error_message": "Internal data processing error. See logs for details."}


weather_agent = Agent(
    name="weather_agent",
    model='gemini-2.5-flash',
    instruction="""
    You are the weather data processor. The data you process is being used to determine best crop cycle by another tool. Your job is to call the **WeatherAggregator tool**. 
    The region key is already available in the state. Provide final answer. 
    """,
    tools=[get_avg_weather]
)