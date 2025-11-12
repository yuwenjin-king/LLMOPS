import os
import requests
from serpapi import GoogleSearch  # pip install google-search-results
import os
def google_search(query, num_results=5):
    params = {
        "q": query,
        "hl": "zh-cn",
        "gl": "cn",
        "api_key": os.environ["SERPAPI_KEY"],  # 改成这行
        #        "num": num_results
    }
    search = GoogleSearch(params)
    res = search.get_dict()
    return res.get("organic_results", [])