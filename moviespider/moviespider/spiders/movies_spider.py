import scrapy
import re
from moviespider.items import MoviespiderItem


def clean_text(value):
    if not value:
        return ""

    value = re.sub(r"\[[^\]]*\]", "", value)
    value = re.sub(r"\.mw-parser-output[^,]*,", "", value)
    value = re.sub(r"#[a-z0-9]{6}\)\}#[a-z0-9]{6}\)\}", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["ru.wikipedia.org", "ru.wikiquote.org"]
    start_urls = [
        "https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту",
        "https://ru.wikipedia.org/wiki/Категория:Фильмы_по_годам"
    ]

    def parse(self, response):
        links = response.css(".mw-category a::attr(href)").getall()
        for link in links:
            if "/wiki/Категория:" in link:
                yield response.follow(link, callback=self.parse)
            else:
                yield response.follow(link, callback=self.parse_movie_page)

        next_links = response.css("a:contains('Следующая страница')::attr(href)").getall()
        for link in next_links:
            yield response.follow(link, callback=self.parse)

    def parse_movie_page(self, response):
        infobox = response.css("table.infobox")
        if not infobox:
            return

        page_title = response.css("title::text").get()
        if any(prefix in page_title for prefix in ["Категория:", "Портал:", "Служебная:", "Список "]):
            return

        item = MoviespiderItem()

        title = response.css("h1#firstHeading::text").get()
        if not title:
            title = response.css("h1.mw-firstHeading::text").get()
        if not title:
            title = response.css("h1 .mw-page-title-main::text").get()

        if title:
            item["title"] = clean_text(title)

        # парсим инфобокс
        rows = response.css("table.infobox tr")
        mapping = {
            "жанр": "genre",
            "жанры": "genre",
            "genre": "genre",
            "режиссёр": "director",
            "режиссер": "director",
            "director": "director",
            "страна": "country",
            "год": "year",
            "year": "year"
        }

        for row in rows:
            header = row.css("th *::text").get()
            if not header:
                continue

            header_lower = header.lower()
            for key in mapping:
                if key in header_lower:
                    field_name = mapping[key]
                    value_list = row.css("td ::text").getall()
                    raw_value = " ".join(v.strip() for v in value_list if v.strip())
                    cleaned_value = clean_text(raw_value)
                    item[field_name] = cleaned_value
                    break

        yield item
