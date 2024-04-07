"""
这种方式通过user proxy对同一个recipient agent持续交谈，并让其从history中获取知识并总结成技能。
并尝试将其白盒化，下次处理类似任务，只需要一次message（或者固化成function calling）。
"""
import autogen
import os
#from autogen import ConversableAgent, config_list_from_json



llm_config = {
    "timeout": 600,
    "cache_seed": 44,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-1106-preview"]},
    ),
    "temperature": 0,
}


# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "work_dir",
        "use_docker": False,
    },
)


#define tasks

task1 = """
Find arxiv papers that show how are people studying trust calibration in AI based systems
"""

task2 = "analyze the above the results to list the application domains studied by these papers "


task3 = """Use this data to generate a bar chart of domains and number of papers in that domain and save to a file
"""


task4 = """Reflect on the sequence and create a recipe containing all the steps
necessary and name for it. Suggest well-documented, generalized python function(s)
 to perform similar tasks for coding steps in future. Make sure coding steps and
 non-coding steps are never mixed in one function. In the docstr of the function(s),
 clarify what non-coding steps are needed to use the language skill of the assistant.
"""


user_proxy.initiate_chat(assistant, message=task1)

user_proxy.initiate_chat(assistant, message=task2, clear_history=False)

user_proxy.initiate_chat(assistant, message=task3, clear_history=False)

user_proxy.initiate_chat(assistant, message=task4, clear_history=False)


'''
generation by assistant after task4
Recipe Name: **Research Paper Domain Analysis and Visualization**

### Recipe Steps:

1. **Non-Coding Step**: Formulate a research question or topic of interest for which you want to analyze the literature.

2. **Coding Step**: Use the arXiv API to search for papers related to the topic of interest. This involves sending a GET request with the appropriate search query and parsing the response.

3. **Non-Coding Step**: Analyze the search results to identify the application domains of the papers. This requires reading the titles and abstracts to understand the context and focus of each paper.

4. **Coding Step**: Generate a bar chart to visualize the number of papers in each identified domain and save the chart to a file.

5. **Non-Coding Step**: Review the generated bar chart for accuracy and relevance. Use the chart in reports, presentations, or further analysis as needed.

### Generalized Python Functions:

#### Function to Search arXiv and Retrieve Paper Metadata

```python
import requests
import xml.etree.ElementTree as ET

def search_arxiv(search_query, max_results=10):
    """
    Search the arXiv API for papers matching the search query and return the metadata.

    Non-Coding Steps:
    - Formulate a search query that accurately represents the topic of interest.
    - Review the returned metadata to identify the application domains of the papers.

    :param search_query: A string containing the search query.
    :param max_results: An integer representing the maximum number of results to retrieve.
    :return: A list of dictionaries containing paper metadata.
    """
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query=all:{query}"
    start = 0
    max_results = f"max_results={max_results}"
    url = f"{base_url}{search_query}&start={start}&{max_results}"
    response = requests.get(url)
    feed = feedparser.parse(response.content)

    papers = [{"title": entry.title, "link": entry.link, "summary": entry.summary} for entry in feed.entries]
    return papers

```

#### Function to Generate and Save a Bar Chart

```python
import matplotlib.pyplot as plt

def generate_bar_chart(data, title, x_label, y_label, output_filename):
    """
    Generate a bar chart from the provided data and save it to a file.

    Non-Coding Steps:
    - Ensure that the data provided is accurate and correctly categorized.
    - Review the generated bar chart for accuracy and relevance.

    :param data: A dictionary where keys are categories and values are counts.
    :param title: A string representing the title of the bar chart.
    :param x_label: A string representing the label for the x-axis.
    :param y_label: A string representing the label for the y-axis.
    :param output_filename: A string representing the filename to save the chart.
    """
    categories = list(data.keys())
    counts = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color='skyblue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()
```

These functions provide a well-documented and generalized way to perform similar tasks in the future. The non-coding steps are clearly separated and described in the docstrings of the functions, indicating the manual analysis or review that is required to effectively use the assistant's language skills.

'''
