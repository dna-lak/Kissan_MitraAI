

from google.adk.agents import SequentialAgent

from .sub_agents.weather_agent.agent import weather_agent
from .sub_agents.crop_agent.agent import crop_agent
from .sub_agents.market_agent.agent import market_agent

# --- Sequential Sub-Agent Pipeline ---

sub_pipeline = SequentialAgent(
    name="sub_pipeline",
    sub_agents=[
        weather_agent, crop_agent, market_agent 
    ],
    
)