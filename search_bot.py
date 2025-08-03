import requests
from bs4 import BeautifulSoup

def ddg_search(query: str, max_results: int = 5):
    """Search DuckDuckGo HTML endpoint and return top results."""
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Send POST request to DuckDuckGo's HTML search endpoint
    response = requests.post(url, data=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    for res in soup.select(".result__a")[:max_results]:
        title = res.get_text()
        link = res.get("href")
        snippet_tag = res.find_parent("div", class_="result").select_one(".result__snippet")
        snippet = snippet_tag.get_text() if snippet_tag else ""
        
        results.append({
            "title": title,
            "link": link,
            "snippet": snippet
        })
    
    return results
