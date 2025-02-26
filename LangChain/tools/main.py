from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

python_repl = PythonREPL()
result = python_repl.run("print(5*5)")
print(result)

duckduckgo_search = DuckDuckGoSearchRun()
query = "Qual a capital da Guiana?"
search_result = duckduckgo_search.run(query)
print(search_result)

wikipedia_query = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
query = "Guiana"
search_result = wikipedia_query.run(query)
print(search_result)
