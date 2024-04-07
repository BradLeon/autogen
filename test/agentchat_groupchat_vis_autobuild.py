import autogen
import openai 

import os

from autogen.agentchat.contrib.agent_builder import AgentBuilder




config_file_or_env = 'OAI_CONFIG_LIST'  # modify path
llm_config = {
    'temperature': 0
}


#Step 2: create an AgentBuilder instance
builder = AgentBuilder(config_file_or_env="OAI_CONFIG_LIST")

#Step 3: specify the building task
building_task = "download data from https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv and plot a visualization that tells us about the relationship between weight and horsepower. Save the plot to a file. Print the fields in a dataset before visualizing it."


#Step 4: build group chat agents
agent_list, agent_configs = builder.build(building_task, llm_config, coding=True)


# step5: execute the task

def start_task(execution_task: str, agent_list: list, llm_config: dict):
  
    config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST",)

    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=20)
    manager = autogen.GroupChatManager(
        groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}
    )
    agent_list[0].initiate_chat(manager, message=execution_task)



start_task(
    execution_task=building_task,
    agent_list=agent_list,
    llm_config=llm_config
)
