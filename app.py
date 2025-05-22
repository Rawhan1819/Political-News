from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "fa7e205f8c444fe5b5fedf39f4636a86"

def get_political_news(location):
    url = "https://newsapi.org/v2/everything"

    political_keywords = [
        "politics", "government", "election", "parliament", "minister",
        "president", "political party", "policy", "diplomacy", "congress"
    ]
    
    query = f"{location} AND ({' OR '.join(political_keywords)})"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("articles", [])
    political_news = []

    for article in articles[:10]:
        if any(keyword.lower() in (article["title"] + (article["description"] or "")).lower()
               for keyword in political_keywords):
            news = {
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "publishedAt": article["publishedAt"]
            }
            political_news.append(news)

    return political_news

@app.route('/', methods=['GET', 'POST'])
def index():
    news = []
    location = ""
    if request.method == 'POST':
        location = request.form.get('location')
        news = get_political_news(location)
    return render_template("index.html", news=news, location=location)

if __name__ == "__main__":
    app.run(debug=True)
