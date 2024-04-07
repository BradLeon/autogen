import autogen
import openai 

import os


# define tasks
financial_tasks = [
    """What are the current stock prices of NVDA, MSFT and TESLA, and how is the performance over the past month in terms of percentage change?""",
    """Investigate possible reasons of the stock performance.""",
]

writing_tasks = ["""Develop an engaging blog post using any information provided."""]

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST",)

llm_config = {"config_list": config_list, "cache_seed": 42}

financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)
research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)
writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for
        your insightful and engaging articles.
        You transform complex concepts into compelling narratives.
        Reply "TERMINATE" in the end when everything is done.
        """,
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",  # ask human for input at each step
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

chat_results = user.initiate_chats(
    [
        {
            "recipient": financial_assistant,
            "message": financial_tasks[0],
            "clear_history": True,
            "silent": False,
            "summary_method": "reflection_with_llm",
        },
        {
            "recipient": research_assistant,
            "message": financial_tasks[1],
            "summary_method": "reflection_with_llm",
        },
        {
            "recipient": writer,
            "message": writing_tasks[0],
            "carryover": "I want to include a figure or a table of data in the blogpost.",
        },
    ]
)