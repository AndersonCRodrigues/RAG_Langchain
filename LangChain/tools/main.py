import os
from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, SerpAPIWrapper

SERP_API_KEY = os.getenv("SERP_API_KEY")

python_repl = PythonREPL()
result = python_repl.run("print(5*5)")
print(result)

google_search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
query = "Qual a capital da Guiana?"
search_result = google_search.run(query)
print(search_result)

wikipedia_query = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
query = "Guiana"
search_result = wikipedia_query.run(query)
print(search_result)
