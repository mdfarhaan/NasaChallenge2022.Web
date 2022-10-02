from msilib.schema import Error
from fastapi import FastAPI
from pydantic import BaseModel
import fitz
from PIL import Image
import pytesseract
import yake
text=''
import spacy
import pytextrank
import PyPDF2
import urllib.request 
from cleantext import clean



pytesseract.pytesseract.tesseract_cmd = 'D:/Tesseract-OCR/tesseract.exe'

class Item(BaseModel):
    url: str
    
app = FastAPI()

def getKeyWords(text):
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    
    return keywords

def getImgDescp(filename):
    pdf_file = fitz.open(filename)
    pdf_image_list=[]
    imgdescps=[]

    for page_index in range(len(pdf_file)):
    
        page = pdf_file[page_index]
        image_list = pdf_file.get_page_images(page_index)
        if image_list:
            pdf_image_list.append(image_list)
            
        for image_index, img in enumerate(pdf_file.get_page_images(page), start=1):
            xref = img[0]
            pix = fitz.Pixmap(pdf_file,xref)
            piximg = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # piximgarr = np.array(pix)
            decp=''
            decp=pytesseract.image_to_string(piximg)
            imgdescps.append(decp)
            
            
    return imgdescps
def getimgdescptext(filename):
    pdf_file = fitz.open(filename)
    pdf_images = []
    imgdescp=[]
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('textrank')
    for page_ndex in range(len(pdf_file)):
        page = pdf_file[page_ndex]
        image_list= pdf_file.get_page_images(page_ndex)
        if image_list:
            # tottext = page.extract_text()
            doc = nlp(page.extract_text())
            for sent in doc.sents:
                if 'figure' in sent.text.lower():
                    imgdescp.append(sent.text)
                if 'fig' in sent.text.lower():
                    imgdescp.append(sent.text)
                
    return imgdescp

def getabstract(filereader):
    fulltext = []
    for i in filereader.pages:
        fulltext+= [i.extract_text()]
        currpage = i.extract_text().lower()
        if 'abstract' in currpage:
            abstract = currpage[currpage.find('abstract'):]
            # print('abstrat',abstract)
            return abstract
        if 'a b s t r a c t' in currpage:
            abstract = currpage[currpage.find('a b s t r a c t'):]
            # print('abstract',abstract)
            return abstract
    
    return ' '.join(fulltext[:4])


def getsummary(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('textrank')
    doc = nlp(text)
    summ1 = list(doc._.textrank.summary())
    tostring = lambda sent:sent.text
    summary = list(map(tostring,summ1))
    summary = ' '.join(summary)
    return summary

def main(filename):
    text=''
    # filename=''
    file = open(filename,'rb')
    filereader = PyPDF2.PdfReader(file)
    text = getabstract(filereader)
    resp = {'summary':'','keywords':'',"img_descp":''}
    resp['keywords'] = getKeyWords(text)
    resp['summary']= getsummary(text)
    resp['img_descp'] = getImgDescp(filename)
    return resp

def main_with_url(url):
    
    # url = 'https://doc-0c-2c-prod-03-apps-viewer.googleusercontent.com/viewer2/prod-03/pdf/9jn1e0jcb4vuhlg2rg91j1rkel93775u/jdslu3fdm904jf00s88jviollq5lj7qq/1664634000000/3/*/APznzaZjmDhh-2YM8NCN4_g2PwbQnvEvPkTDC9Q3H9ffqn47r551wvZ5pLpd_e9GQNaG2evnY3VhP5C1wzK2TRovD9xLrMgq--XeZo4q28pVCwh5Wbdz9Gk_ykUUbe8PBD2NaQTeGi_qMbSESp86cDxYP6k8XEwywie8DK7EHdEl17CXEruJ49FLwGFzR8MJ3qUPYip0ybcEc8X2Tyc5s08ft2sqyl6KMyy8jrSLv0J9KMCS0xaW-0vYn7G2PDqQjx2YflnJjjQD8ucdqfCkr2MNMSoqjnMnJCLDjJQ4xAam68YPLY8qoS_WFhZT9O5EMEm463QQ2eukgNGOLIx0oVFhL6TMe1M6jISCDkcp_7_85w3xD4293xiJnG-dYkOAGOfInMGzj5oz?authuser'
    

    urllib.request.urlretrieve(url, "mast.pdf")
    text=''
    
    file = open("mast.pdf",'rb')
    filereader = PyPDF2.PdfReader(file)
    text = getabstract(filereader)
    file.close()
    resp = {'summary':'','keywords':'',"img_descp":''}
    
    resp['keywords'] = getKeyWords(text)
    resp['summary']= getsummary(text)
    resp['img_descp'] = getImgDescp('mast.pdf')

    resp['img_descp']=clean(resp["img_descp"],
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=True,                     # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=False,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=False,               # replace all numbers with a special token
        no_digits=False,                # replace all digits with a special token
        no_currency_symbols=False,      # replace all currency symbols with a special token
        no_punct=False,                 # remove punctuations
        replace_with_punct="",          # instead of removing punctuations you may replace them
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
        lang="en"                       # set to 'de' for German special handling
    )
    return resp


@app.post('/nlpmodel/')
async def create_item(item: Item):
    try:
        return main_with_url(item.url)
    except Error as e:
        print(e)
        # return {'summary':'','keywords':'',"img_descp":'','message':'there exists a problem'}
        return {
            "summary": "while\nrecent work (zhao et al., 2021; min et al., 2022; ye\nand durrett, 2022) has analyzed and evaluated this\nparadigm across a number of tasks, it has only been\nstudied for text summarization with unreliable au-\ntomatic metrics (he et al., 2022; chowdhery et al.,\n2022; ouyang et al., 2022) or in non-standard set-\ntings (saunders et al., 2022).\n the suc-\ncess of prompt-based models (gpt-3 (brown et al.,\n2020), t0 (sanh et al., 2022), palm (chowdhery\net al., 2022), etc.) provides an alternative approach,\nnamely learning from natural language task instruc-\ntions and/or a few demonstrative examples in the\ncontext without updating model parameters. finally, we discuss fu-\nture research challenges beyond generic sum-\nmarization, speciﬁcally, keyword- and aspect-\nbased summarization, showing how dominant\nﬁne-tuning approaches compare to zero-shot\nprompting.\nto support further research, we release: (a)\na corpus of 10k generated summaries from\nﬁne-tuned and zero-shot models across 4\nstandard summarization benchmarks, (b) 1k\nhuman preference judgments and rationales\ncomparing different systems for generic- and\nkeyword-based summarization.1\n1 introduction\nfine-tuning pre-trained models on domain-speciﬁc\ndatasets has been the leading paradigm in text sum-\nmarization research in recent years (lewis et al.,\n2020; zhang et al., 2020; raffel et al., 2020). in this pa-\nper, we study its impact on text summarization,\nfocusing on the classic benchmark domain of\nnews summarization.",
            "keywords": [
            ["shift in nlp",0.048136971684981246],["summarization",0.05026972585975926],["models",0.06259845616958987],["summaries",0.07897458061742815],["zero-shot",0.09309138730309043],["research",0.09586878870725504],["text summarization",0.09727045996221506],["study", 0.1082572396874762],["nlp research", 0.1144859536485805],["few-shot prompting", 0.1209764410549975],["trump",0.12280484833176196],["text",0.12482285179994512],["recent success",0.12903505039167384],["paradigm shift",0.12903505039167384],["datasets",0.15578825112116548],["sum", 0.1564895488633192],["recent",0.17776598109031674],["paradigm",0.17776598109031674],["judge",0.17824596668038856],["prompt-based models",0.18084030392848247]
            ],
            "img_descp": "[\"workflow\nfor each article, first read the news article carefully on the left panel of the task. the summaries\nfor the article are shown on the right panel. you will answer 2 questions about these summaries.\n1. which summary/summaries do you prefer the most? you can select more than one summary\nhere if there are multiple good summaries and you have no clear preference between them.\njustify your selection in the text box below. you can say things like 'summary a misses the main\nintent of the summary / summar a is non-factual / etc.\n2. which summary/summaries is the worst? similar to the previous case, justify your selection in\nthe text box below. (you can select all if no one summary is noticeably worse than the other\ntwo).\n\", \"basic task description\nthank you for participating in this study! first, enter your prolific id here:\nthe goal of this study is to rate evaluate machine-generated summaries of news articles.\nyou will evaluate summaries for 5 different news articles in this study, each of which has 3\nsummaries. suppose you were browsing social media and saw one of these summaries with a\nlink to the article. which summary/summaries would you prefer to see or which summary\nprovides the truest description of the article's content and intent.\nyou can make this judgment based on your own browsing habits. for example, you can\nevaluate the summary based on characteristics like does it focus on the main topic or content\nof the article?, is all the information in the summary factually correct?, or any other\ncharacteristics that are important to you in this setting. note that the summaries are\nautomatically generated and can contain small errors. keep an eye out for these and\nappropriately penalize them while making your decision.\n\", \"basic task description\nthank you for participating in this study! first, enter your prolific id here:\nthe goal of this study is to evaluate machine-generated summaries of news articles. you\nwill evaluate summaries for 5 different news articles. each summary is expected to be 2-3\nsentences long.\nsuppose you search for a keyword (e.g. a person's name or an organization) and saw one of\nthese summaries with a link to the article. which summary would you prefer to see? you should\nmake this judgment based on the following criterion:\n1. does the summary provide an appropriate description of the person/organizations's role in\nthe news story?\n2. does the summary give enough context of the broader news story around the\nperson/organization? e.g. 'boris johnson is expected to respond to the accusation on tuesday'\nis not an ideal summary as it does not give any details about the main event 'the accusation' in\nthe summary.\n\", \"apart from these criterion, you can also make your judgment based on your personal\npreferences and browsing behavior. note that the summaries are automatically generated and\ncan contain small errors, e.g. the summary may not present a coherent narrative or contain\ninformation not in the input article. keep an eye out for these and appropriately penalize them\nwhile making your decision.\nworkflow\nfor each article, first read the news article carefully on the left panel of the task. on the right\npanel, you will be shown two keywords. for each keyword, you will be shown 2 summaries. you\nwill be asked to compare the two summaries and answer the following questions:\n1. which summary do you prefer the most?\n2. justify your selection in the text box below. you can say things like 'summary a misses the\nmain intent of the summary' / 'summary a does not talk about the keyword's role' etc.\n\"]"
        }

@app.get('/')
async def index():
    return {"message":"<h1>Page Works/<h1>"}