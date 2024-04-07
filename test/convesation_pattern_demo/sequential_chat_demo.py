# The Number Agent always returns the same numbers.

import os

from autogen import ConversableAgent, config_list_from_json


config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST",)

llm_config = {"config_list": config_list, "cache_seed": 42}

APIKEY="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"

number_agent = ConversableAgent(
    name="Number_Agent",
    system_message="You return me the numbers I give you, one number each line.",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply = 5,
)

# The Adder Agent adds 1 to each number it receives.
adder_agent = ConversableAgent(
    name="Adder_Agent",
    system_message="You add 1 to each number I give you and return me the new numbers, one number each line.",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply = 5,
)

# The Multiplier Agent multiplies each number it receives by 2.
multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    system_message="You multiply each number I give you by 2 and return me the new numbers, one number each line.",
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    max_consecutive_auto_reply = 5,
)

# The Subtracter Agent subtracts 1 from each number it receives.
subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    system_message="You subtract 1 from each number I give you and return me the new numbers, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": APIKEY}]},
    human_input_mode="NEVER",
    max_consecutive_auto_reply = 5,
)

# The Divider Agent divides each number it receives by 2.
divider_agent = ConversableAgent(
    name="Divider_Agent",
    system_message="You divide each number I give you by 2 and return me the new numbers, one number each line.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": APIKEY}]},
    human_input_mode="NEVER",
    max_consecutive_auto_reply = 5,
)



# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
chat_results = number_agent.initiate_chats(
    [
        {
            "recipient": adder_agent,
            "message": "14",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": multiplier_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": subtracter_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": divider_agent,
            "message": "These are my numbers",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
    ]
)



print("First Chat Summary: ", chat_results[0].summary)
print("Second Chat Summary: ", chat_results[1].summary)
print("Third Chat Summary: ", chat_results[2].summary)
print("Fourth Chat Summary: ", chat_results[3].summary)
