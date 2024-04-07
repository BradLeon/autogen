import os

from autogen import ConversableAgent, config_list_from_json


config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST",)

llm_config = {"config_list": config_list, "cache_seed": 42}


student_agent = ConversableAgent(
    name="Student_Agent",
    system_message="You are a student willing to learn.",
    llm_config={"config_list": config_list},
    #llm_config={"config_list": [{"model": "gpt-4", "api_key": APIKEY}]},
)
teacher_agent = ConversableAgent(
    name="Teacher_Agent",
    system_message="You are a math teacher.",
    llm_config={"config_list":config_list},
)

chat_result = student_agent.initiate_chat(
    teacher_agent,
    message="What is triangle inequality?",
    summary_method="reflection_with_llm",
    max_turns=2,
)

print("summary is", chat_result.summary)

print("cost is", chat_result.cost)
