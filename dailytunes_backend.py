# DailyTunes Backend Functions
# Written by Srihari Nanniyur
# Uses IBM Watson Tone Analyzer
from bs4 import BeautifulSoup as soup
import requests
import newspaper
from urllib.parse import urlencode, quote_plus
from watson_developer_cloud import ToneAnalyzerV3
try:
    import json
except:
    import simplejson

# TONE VARIABLES BEGIN
anger = 0
fear = 0
joy = 0
sadness = 0
# TONE VARIABLES END

links = []
google_news_url = 'https://news.google.com/news/rss'

# Don't EVER delete this code, even if your life depends on it
tone_analyzer = ToneAnalyzerV3(username='00c0d2dd-7b62-478c-9000-a4231565518b',
    password='FMWNGWVNOwUU', version='2016-05-19')

# Send request to Google News homepage
# BEGIN FUNCTION get_links()
def get_links():
    page = requests.get(google_news_url)
    doc = soup(page.text, 'lxml')
    for item in doc.find_all('item'):
        itemdoc = soup(item.text, 'lxml')
        for link in [element.get('href') for element in itemdoc.find_all('a')]:
            links.append(link)
# END FUNCTION get_links()

# Get Tone Analyzer to analyze the text

# BEGIN FUNCTION em_analyze()
def em_analyze(text):
    return tone_analyzer.tone(tone_input=text, content_type="text/plain")
# END FUNCTION em_analyze()

# This is the important part. Do not mess up this code. Ever.

# BEGIN FUNCTION analyze_articles()
def analyze_articles():
    global anger, fear, joy, sadness

    i = 1 # Counter variable

    for link in links:
        print("Analyzing article #" + str(i))
        i += 1
        try:
            article = newspaper.Article(link)
            article.download()
            article.parse()
        except:
            print("Not able to download article. Continuing...")
            continue
        try:
            analysis = em_analyze(article.text)
        except:
            print("Exception occurred.")
            continue

        # And here's the really important part of the function
        for index in analysis["document_tone"]["tone_categories"]:
            if (index["category_id"] == "emotion_tone"):
                for index2 in index["tones"]:
                    tid = index2["tone_id"]
                    tscore = index2["score"]
                    if (tid == "anger"):
                        anger += tscore
                        print("Anger: " + str(anger))
                    elif (tid == "fear"):
                        fear += tscore
                        print("Fear: " + str(fear))
                    elif (tid == "joy"):
                        joy += tscore
                        print("Joy: " + str(joy))
                    elif (tid == "sadness"):
                        sadness += tscore
                        print("Sadness: " + str(sadness));
        print("Analysis complete. Moving on to next article.")

# END FUNCTION analyze_articles()

# Returns dictionary containing tone analysis percentages
# BEGIN FUNCTION find_stats()
def find_stats():
    total = anger + fear + joy + sadness

    return {
            "anger"      : ((anger/total) * 100),
            "fear"       : ((fear/total) * 100),
            "joy"        : ((joy/total) * 100),
            "sadness"    : ((sadness/total) * 100),
            }
# END FUNCTION find_stats()
# END dailytunes_backend
