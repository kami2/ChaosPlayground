import requests
from bs4 import BeautifulSoup


def instagram_media_extractor(link: str):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the meta tag with property 'og:image' to extract the source URL
    meta_tags = soup.find_all('meta', property='og:image')

    if meta_tags:
        # Extract the 'content' attribute from the first meta tag
        source_url = meta_tags[0]['content']
        return source_url
    else:
        return None


if __name__ == '__main__':
    instagram_media_extractor("url")

