#Gets the data from the websites
from bs4 import BeautifulSoup, NavigableString
import requests
import file_io as fi

class Spider:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def get_body_html(self, url):
        #Gets the html from the url
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            soup =  BeautifulSoup(response.content, 'html.parser')

            body = soup.find('body')
            script_tags = body.find_all('script', recursive=False)

            for script_tag in script_tags:
                script_tag.decompose()

            new_html = scrub_element(body)
            text = new_html.get_text(separator='\n', strip=True)

            return text
        else:
            print('Unable to get html from url')
            return None

def scrub_element(element):
    for option in element.find_all('option'):
        option.decompose()

    if element.text != '':
        return element
    
    # Create a new tag with the same name and attributes as the current element
    new_tag = element.new_tag(element.name, **element.attrs)
    
    # Recursively rebuild the element's children and append them to the new tag
    for child in element.children:
        if child.name:
            new_child = scrub_element(child)
            new_tag.append(new_child) 
        else:
            new_tag.append(child)
    return new_tag
