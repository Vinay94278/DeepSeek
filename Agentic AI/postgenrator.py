from phi.agent import Agent , RunResponse
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from phi.tools.wikipedia import WikipediaTools
from phi.tools.googlesearch import GoogleSearch
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.utils.pprint import pprint_run_response

# Agent 1: Research Agent
research_agent = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    tools=[DuckDuckGo(), Newspaper4k(), WikipediaTools(), ArxivToolkit(),GoogleSearch()],
    description="You are a research assistant specializing in AI and technology trends.",
    instructions=[
        "Search for the latest trends in AI and technology using DuckDuckGo.",
        "Extract key insights from articles, research papers, and Wikipedia.",
        "Summarize the findings in a concise format for the content creation agent.",
    ],
    markdown=True,
    show_tool_calls=True,
)

# Agent 2: Content Creation Agent
content_agent = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    tools=[],
    description="You are a creative AI content writer specializing in LinkedIn and X posts.",
    instructions=[
        "Write a short, engaging post for LinkedIn and X based on the research summary.",
        "Use emojis, humor, and a conversational tone.",
        "Add a call-to-action (e.g., 'What do you think?' or 'Let's discuss!').",
        "For LinkedIn, expand on the topic with more detail and professionalism.",
        "For X, keep it concise, witty, and impactful (280 characters max).",
    ],
    markdown=True,
    show_tool_calls=True,
)
# Create a MultiAgent system
# multiagent = Agent(agents=[research_agent, content_agent])

# Function to generate posts
def generate_posts(topic=None):
    # If no topic is provided, default to "latest trends in AI"
    if not topic:
        topic = "latest trends in AI"

    # Step 1: Research the topic
    research_summary: RunResponse = research_agent.run(f"Find information about: {topic}")

    # Step 2: Generate LinkedIn and X posts
    linkedin_post: RunResponse = content_agent.run(f"Write a LinkedIn and X post based on this research: {research_summary}")

    # Print results
    # print("### Research Summary ###")
    pprint_run_response(research_summary,markdown=True)
    pprint_run_response(linkedin_post,markdown=True)

# Get user input
user_topic = input("Enter a specific topic (or press Enter for default AI trends): ")

# Generate posts based on user input
generate_posts(user_topic if user_topic else None)