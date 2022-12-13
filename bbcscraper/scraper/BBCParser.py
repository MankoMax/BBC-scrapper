from .Selenium import SeleniumParser
from selenium.webdriver.common.by import By
from .models import News
from selenium.common.exceptions import NoSuchElementException
import time
from .utils import add_data_to_excel_file


class BBCParser(SeleniumParser):
    
    
    def generate_news(self):
            self._fetch('https://www.bbc.com')
            sections = self.driver.find_elements(By.TAG_NAME, value='section')
            links = []
            
            for section in sections:
                section_links = section.find_elements(By.CSS_SELECTOR, value='a.block-link__overlay-link')
                section_link_hrefs = [link.get_attribute('href') for link in section_links]
                
                links.extend(section_link_hrefs)

            for link in links:
                try:
                    self.try_generate_news_internal(link)
                except:
                    continue
        
       
    def try_generate_news_internal(self, link): 
        self.driver.get(link)
        time.sleep(1)
            
        body = self.get_article_body()
        header = self.get_article_header()
            
        if(body != ""):
            news, created = News.objects.get_or_create(title=header, description=body, url=link)
            if created:
                news.save()
                data = news.__dict__
                try:
                    add_data_to_excel_file(data)
                except Exception as e:
                    print(e)
        raise Exception("Article can not be generated") 
    
    
    def get_article_body(self):
        body = ""
        try:
            body_content = self.driver.find_element(by=By.CSS_SELECTOR, value="div.article__body-content")
            contents = body_content.find_elements(by=By.CSS_SELECTOR, value="p")
            for content in contents:
                if "@BBCBreaking" in content.text:
                    continue
                if "© 2022 BBC" in content.text:
                    continue
                body = body + "\n" + content.text
        except NoSuchElementException:
            try:
                result = self.driver.find_element(by=By.XPATH, value="//div[contains(@class, 'ssrcss')]")
                ps = result.find_elements(by=By.XPATH, value=".//p[contains(@class, 'Paragraph')]")
                for p in ps:
                    text = p.text
                    if not text:
                        text = p.get_attribute('innerText')
                    if not text:
                        text = p.get_attribute('textContent')
                    if "@BBCBreaking" in text:
                        continue
                    if "© 2022 BBC" in text:
                        continue
                    body = body + "\n" + text
            except NoSuchElementException:
                try:
                    data_components = self.driver.find_elements(by=By.XPATH, value="//div[@data-component='text-block']")   
                    for data_component in data_components:
                        if "@BBCBreaking" in data_component.text:
                            continue
                        if "© 2022 BBC" in data_component.text:
                            continue
                        body = body + "\n" + data_component.text
                except NoSuchElementException:
                    try:
                        body = self.driver.find_element(by=By.CSS_SELECTOR, value="div.qa-story-body").text
                    except NoSuchElementException:
                        pass   
        return body
    
    
    def get_article_header(self):
        header = ""
        
        try:
            header = self.driver.find_element(by=By.CLASS_NAME, value="article-headline__text").text
        except NoSuchElementException:
            try:
                header = self.driver.find_element(by=By.TAG_NAME, value="h1").text
            except NoSuchElementException:
                pass
                
        return header