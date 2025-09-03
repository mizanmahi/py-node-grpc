import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel
from pydantic import BaseModel, Field
import json
import gradio as gr
import asyncio

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

# {
#     "message": "Your friendly response message",
#     "isLearningRelated": true|false,
#     "suggestedTopics": ["topic1", "topic2", "topic3"] // only if isLearningRelated is false
#   }
class IsEducationalOutput(BaseModel):
    is_educational: bool = Field(description="Whether the prompt is related to tech education")
    reason: str = Field(description="Brief reason for the decision")
    suggested_topics: list[str] = Field(description="List of suggested topics if not educational")

is_educational_agent = Agent(
    name="Educational Checker",
    instructions="""You are a conversational AI assistant that helps people learn. Your task is to analyze the user’s input and classify it into one of two categories:

Non-learning input: This includes greetings (e.g., 'hello', 'hi', 'how are you'), small talk, or questions/statements unrelated to learning (e.g., 'what’s the weather', 'tell me a joke'). For these, you must respond with a friendly, conversational message and also suggest 3 possible learning topics the user might explore.

Learning-related input: This includes any question, statement, or request directly related to learning something (e.g., 'I want to learn React', 'Explain Python functions'). For these, do not give a friendly message or suggested topics. Instead, simply mark the input as learning-related so the normal learning analysis flow can continue.

You must always respond with valid JSON in the following schema:

{
'conversationalResponse': {
'message': 'Your friendly response message',
'isLearningRelated': true|false,
'suggestedTopics': ['topic1', 'topic2', 'topic3'] // only include if isLearningRelated is false
}
}

Examples:

Input: 'Hello'
Output: { 'conversationalResponse': { 'message': 'Hi there! How’s your day going?', 'isLearningRelated': false, 'suggestedTopics': ['JavaScript basics', 'Cloud computing', 'Database design'] } }

Input: 'How are you?'
Output: { 'conversationalResponse': { 'message': 'I’m doing great, thanks for asking! What about you?', 'isLearningRelated': false, 'suggestedTopics': ['Python programming', 'Web development', 'Machine learning'] } }

Input: 'I want to learn React'
Output: { 'conversationalResponse': { 'message': '', 'isLearningRelated': true } }""",
    model=model,
    output_type=IsEducationalOutput
)

is_educational_tool = is_educational_agent.as_tool(
    tool_name="check_educational",
    tool_description="Check if the prompt is related to tech education"
)

class PromptAnalysis(BaseModel):
    summary: str = Field(description="Brief summary of the prompt")
    questions: list[str] = Field(description="List of 3-5 clarifying questions")
    quality_score: int = Field(description="Quality score from 1-10")
    questionOptions: dict[str, list[str]] = Field(description="Options for each question, including 'Other'")

analyzer_instructions = """You are an educational prompt analyzer. Analyze the given prompt and provide:
1. A brief summary of what the user is asking
2. 3-5 clarifying questions to better understand their learning needs
3. A quality score (1-10) based on how clear and specific the prompt is
4. For each question, provide 3-4 contextually relevant answer options plus an "Other" option

For answer options, consider these categories based on the question context:
- Grade levels: "Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/University", "Other"
- Subjects: "Math", "Science", "English/Language Arts", "History/Social Studies", "Computer Science", "Other"
- Difficulty: "Beginner", "Intermediate", "Advanced", "Other"
- Time commitment: "15-30 minutes", "30-60 minutes", "1-2 hours", "Other"
- Learning styles: "Visual", "Auditory", "Hands-on/Kinesthetic", "Other"
- Learning goals: "Understanding concepts", "Practical application", "Test preparation", "Other"
"""

analyzer_agent = Agent(
    name="Prompt Analyzer",
    instructions=analyzer_instructions,
    model=model,
    output_type=PromptAnalysis
)

analyzer_tool = analyzer_agent.as_tool(
    tool_name="analyze_prompt",
    tool_description="Analyze an educational prompt and provide structured output"
)

main_instructions = """
You are the main agent handling user prompts.
1. Use the check_educational tool to verify if the prompt is related to tech education.
2. If not educational, respond politely and redirect to education, Be creative in your responses and suggestions.
3. If educational, use the analyze_prompt tool to get the analysis, then output the JSON from it.
Do not add extra text; if analysis, output only the JSON."""

main_agent = Agent(
    name="Main Educational Agent",
    instructions=main_instructions,
    tools=[is_educational_tool, analyzer_tool],
    model=model
)

async def handle_prompt(prompt: str):
    with trace("Educational Agent System"):
        result = await Runner.run(main_agent, prompt)
    if result.final_output:
        try:
            # Assuming if analysis, it's JSON
            json_output = json.loads(result.final_output)
            print(json.dumps(json_output, indent=2))
        except json.JSONDecodeError:
            print(result.final_output)
    else:
        print("No output generated.")



async def agent_response(prompt: str) -> str:
    result = await Runner.run(main_agent, prompt)
    return result.final_output or "No output generated."

def gradio_agent(prompt: str):
    # Run the async agent in a sync context for Gradio
    return asyncio.run(agent_response(prompt))

if __name__ == "__main__":
    # import asyncio
    # # Example usage
    # async def main():
    #     prompts = [
    #         "Good Morning",
    #         "I want to learn Node.js"
    #     ]
    #     for prompt in prompts:
    #         print(f"\nProcessing prompt: {prompt}")
    #         await handle_prompt(prompt)

    # asyncio.run(main())

   gr.Interface(
        fn=gradio_agent,
        inputs=gr.Textbox(lines=2, label="Enter your prompt"),
        outputs=gr.Textbox(label="Agent Response"),
        title="Educational Agent",
        description="Ask a question related to tech education."
    ).launch()