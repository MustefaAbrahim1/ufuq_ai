import os
import google.generativeai as genai
from pytrends.request import TrendReq
from dotenv import load_dotenv

# ========== Load API Key ==========
load_dotenv()
# Set up Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
# Initialize Google Trends
pytrends = TrendReq(hl='en-US', tz=360)

def get_trending_keywords(niche):
    try:
        pytrends.build_payload([niche], cat=0, timeframe='now 7-d', geo='', gprop='')
        trending_searches = pytrends.related_queries()
        top_queries = trending_searches.get(niche, {}).get("top", {}).get("query", [])
        return top_queries[:5] if top_queries else []
    except Exception as e:
        print("Trend fetch error:", e)
        return []


def generate_content_ideas(platform, niche, audience, past_topics, language):
    trending_keywords = get_trending_keywords(niche)
    keywords_text = ", ".join(trending_keywords) if trending_keywords else "No trending keywords found."

    prompt = f"""You are a multilingual social media content strategist specialized in generating platform-specific and trend-based post ideas.
    Your task:
    > Generate 2-3 highly engaging content ideas for {platform} in {language}, based on current trends in the niche: {niche}.

    Platform: {platform}
    Language: {language}
    Niche: {niche}
    Audience: {audience}
    Previous Topics: {past_topics or 'N/A'}
    Trending Keywords: {keywords_text}

    Respond in this format (no more, no less):

    
    1. Title: [Short and bold]

    Description: [2 - 3 paragraph in simple language]

    Hashtags: #[hashtag1] #[hashtag2] #[hashtag3]


    ---
    2. Title: [Short and bold]

    Description: [2 - 3 paragraph in simple language]

    Hashtags: #[hashtag1] #[hashtag2] #[hashtag3]

    ---
    3. Title: [Short and bold]

    Description: [2 - 3 paragraph in simple language]
    
    Hashtags: #[hashtag1] #[hashtag2] #[hashtag3]

    """

    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return "⚠️ Error generating ideas. Please try again later."
