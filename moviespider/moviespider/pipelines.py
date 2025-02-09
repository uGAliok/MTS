# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests

class MoviespiderPipeline:
    def process_item(self, item, spider):
        return item

class ImdbRatingPipeline:
    def __init__(self, omdb_api_key):
        self.omdb_api_key = omdb_api_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            omdb_api_key=crawler.settings.get("OMDB_API_KEY")
        )

    def process_item(self, item, spider):
        title = item.get("title")
        if title:
            url = "http://www.omdbapi.com/"
            params = {
                "apikey": self.omdb_api_key,
                "t": title,
                "r": "json",
                "plot": "short"
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("Response") == "True":
                    imdb_rating = data.get("imdbRating")
                    if imdb_rating:
                        item["imdb_rating"] = imdb_rating
        return item
