import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_ROUTER_API_KEY")
if not api_key:
    raise ValueError("Set OPEN_ROUTER_API_KEY environment variable")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

model = OpenAIChatCompletionsModel(
    model="z-ai/glm-4.5-air:free",
    openai_client=client
)

agent = Agent(
    name="Tech Learning Assistant",
    instructions="""
    You are a helpful AI assistant specialized in technology education.
    Your tasks include:
    - Providing explanations of technical concepts.
    - Assisting with coding questions and debugging.
    - Suggesting resources for learning new technologies.
    - Offering tips for effective online learning.
    Always respond concisely, use bullet points for clarity, and cite any assumptions.
    If the query involves code, review it for security issues.
    """,
    model=model
)

async def run_agent_query(query: str) -> str:
    result = await Runner.run(agent, query)
    return result.final_output