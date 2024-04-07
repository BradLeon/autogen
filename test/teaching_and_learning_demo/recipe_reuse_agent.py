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

task1 = '''
This recipe is available for you to reuse..
<begin recipe>
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
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': max_results
    }
    response = requests.get(base_url, params=params)
    papers = []

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        namespaces = {
            'open_search': 'http://a9.com/-/spec/opensearch/1.1/',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        for entry in root.findall('arxiv:entry', namespaces):
            paper = {
                'title': entry.find('arxiv:title', namespaces).text,
                'authors': [author.find('arxiv:name', namespaces).text for author in entry.findall('arxiv:author', namespaces)],
                'summary': entry.find('arxiv:summary', namespaces).text.strip(),
                'link': entry.find('arxiv:link[@title="pdf"]', namespaces).attrib['href'],
                'published': entry.find('arxiv:published', namespaces).text
            }
            papers.append(paper)
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


**Usage:**

1. Use the `search_arxiv` function to collect relevant papers from arxiv using a search query.
2. Analyze the abstracts of the collected papers using your language skills to identify application domains and count the number of papers in each domain.
3. Use the `generate_bar_chart` function to generate a bar chart of the application domains and the number of papers in each domain, and save it as an image file.


</end recipe>


Here is a new task:
Plot a chart for application domains of GPT models
'''

user_proxy.initiate_chat(assistant, message=task1)

