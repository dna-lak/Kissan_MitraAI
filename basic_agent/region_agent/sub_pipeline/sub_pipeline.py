

from google.adk.agents import SequentialAgent

from .sub_agents.weather_agent.agent import weather_agent
from .sub_agents.crop_agent.agent import crop_agent

# --- Sequential Sub-Agent Pipeline ---
# This is the agent that the Root Agent will delegate to.
sub_pipeline = SequentialAgent(
    name="sub_pipeline",
    sub_agents=[
        weather_agent, crop_agent       # Step 2: Weather Aggregation           # Step 3: Crop Recommendation
    ],
    
)