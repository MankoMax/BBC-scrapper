from .BBCParser import BBCParser
from .models import News
from .utils import add_data_to_excel_file



def parser_job():
    BBCParser().generate_news()
    # news = News.objects.all()
    # for new in news:
    #     data = new.__dict__
    #     try:
    #         add_data_to_excel_file(data)
    #     except Exception as e:
    #         print(e)
        
    