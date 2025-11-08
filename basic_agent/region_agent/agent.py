
from google.adk.agents import Agent
#from google.adk.runners import Runner
#from google.adk.sessions import InMemorySessionService
# Import the main pipeline and constants
from .sub_pipeline.sub_pipeline import sub_pipeline
from .data_setup import STATE_KEY_NAME, REGIONS
#import asyncio
 # To ensure data files are created

# --- 1. Define Models ---


# --- 2. Define the Root Agent (The Conductor) ---
root_agent = Agent(
    name="region_agent",
    model="gemini-2.5-flash",
    description="Region finding agent",
    instruction=f"""
    **ask the user for their locality and language preference.**
    Communicate to them further in their preferred language. 
    Identify the state in India that they are from based on their locality.
    The output must be a single string matching one of these valid regions: {REGIONS}.
    DO NOT include any conversational text, formatting, or prefixes. to complete the task.
    Give the output matching one of the regions in : {REGIONS} to the state key.
    """,

    output_key = STATE_KEY_NAME,

    sub_agents=[sub_pipeline],
)



async def run_pipeline(user_input):
    print(f"\n Farmer's Query: {user_input}")
    

    runner = Runner(
        agent=root_agent,
        app_name="Kissan_Saathi",
        session_service=InMemorySessionService()
    )

    # Run the pipeline
    async for event in runner.run_async("user_farmer", "session_modular", user_input):
        if event.text:
            print("\n Final Potential Crop Cycles Recommendation:")
            print("---------------------------")
            print(event.text)
            