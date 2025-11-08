from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import pandas as pd
from google.adk.tools import ToolContext
import traceback
from ....data_setup import (
    STATE_KEY_NAME, WEATHER_KEY_NAME, RECOMMENDATION_KEY_NAME, 
    FINAL_RECOMMENDATION_KEY_NAME, SALES_CSV_PATH, REGIONS
)

def determine_most_profitable_crop(tool_context: ToolContext) -> dict:
    """
    Reads the top 3 crop candidates from the state and filters them based on sales data.
    Chooses the highest revenue crop for each cycle from the candidates.
    """
    recommendation_data = tool_context.state.get(RECOMMENDATION_KEY_NAME)

    if not recommendation_data or 'recommendation' not in recommendation_data:
        return {"status": "error", "error_message": "Crop recommendation candidates not found in state."}
    
    # Extract the top 3 lists
    candidates = recommendation_data['recommendation']
    summer_candidates = candidates.get('summer', [])
    winter_candidates = candidates.get('winter', [])

    try:
        sales_df = pd.read_csv(SALES_CSV_PATH)
        
   
        if 'Crop_Type' not in sales_df.columns or 'modal_price' not in sales_df.columns:
            raise KeyError("Sales data CSV must contain 'Crop_Type' and 'modal_price' columns.")

        # Filter the sales data to only include the recommended crops
        sales_df_filtered = sales_df[
            sales_df['Crop_Type'].isin(summer_candidates + winter_candidates)
        ].copy()

        if sales_df_filtered.empty:
            tool_context.state[FINAL_RECOMMENDATION_KEY_NAME] = tool_context.state[RECOMMENDATION_KEY_NAME]

        # Find the max revenue crop from the summer candidates
        best_summer_sales = sales_df_filtered[
            sales_df_filtered['Crop_Type'].isin(summer_candidates)
        ].sort_values(by='modal_price', ascending=False)
        
        final_summer_crop = best_summer_sales.iloc[0]['Crop_Type'] if not best_summer_sales.empty else summer_candidates[0]

        # Find the max revenue crop from the winter candidates
        best_winter_sales = sales_df_filtered[
            sales_df_filtered['Crop_Type'].isin(winter_candidates)
        ].sort_values(by='modal_price', ascending=False)
        
        final_winter_crop = best_winter_sales.iloc[0]['Crop_Type'] if not best_winter_sales.empty else winter_candidates[0]
        
        final_recommendation = {
            "summer_crop": final_summer_crop,
            "winter_crop": final_winter_crop,
            "reasoning": "Filtered top candidates based on maximum average sales revenue.",
        }

        # Update the state with the final, single-crop recommendation
        tool_context.state[FINAL_RECOMMENDATION_KEY_NAME] = final_recommendation
        
        return {
            "status": "success", 
            "message": "Final crop selection based on profitability is complete.",
            "final_crop": final_recommendation
        }
        
    except Exception as e:
        print(f"Error in determine_most_profitable_crop: {traceback.format_exc()}")
        return {"status": "error", "error_message": f"Error calculating sales profit: {e}"}

from google.adk.agents import Agent 
market_agent = Agent(
    name="market_agent",
    model='gemini-2.5-flash',
    instruction=f"""
    You are the Final Profitability Expert. Your job is to select the single best crop for the Summer and Winter cycles.

    1. **You must call the determine_most_profitable_crop tool first** to execute the sales and filtering logic.
    2. Read the final recommendation from the state key '{FINAL_RECOMMENDATION_KEY_NAME}'.
    3. Generate a concise, conclusive, and actionable recommendation for the farmer. State the best crop for summer and the best crop for winter.
    """,
    tools=[determine_most_profitable_crop]
)