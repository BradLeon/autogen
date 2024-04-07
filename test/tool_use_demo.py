from typing import Annotated, Literal
import os

from autogen import ConversableAgent
import autogen
import openai 

import os



# step1 define a simple function as tool
Operator = Literal["+", "-", "*", "/"]

def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")
    



config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST",)

llm_config = {"config_list": config_list, "cache_seed": 42}


# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": config_list},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

'''
# step2. mothod No.1 seperately register tool for agent which to call and execute it .
# Register the tool signature with the assistant agent.
assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)

# Register the tool function with the user proxy agent.
user_proxy.register_for_execution(name="calculator")(calculator)
'''


# step2 method No.2 register a tool with both agents at once.
from autogen import register_function

# Register the calculator function to the two agents.
register_function(
    calculator,
    caller=assistant,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="calculator",  # By default, the function name is used as the tool name.
    description="A simple calculator",  # A description of the tool.
)



# step3 Using Tool
chat_result = user_proxy.initiate_chat(assistant, message="What is (44232 + 13312 / (232 - 32)) * 5?")
