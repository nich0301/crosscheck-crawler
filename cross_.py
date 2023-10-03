from bs4 import BeautifulSoup
import decoder,os
import pandas as pd
from lxml import etree

def html1(html_file):

    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    element = etree.HTML(str(soup))

    title = element.xpath('//*[@id="mainContent"]/table/tbody/tr[1]/td/div/text()[2]')
    for i in title:
        title = i.replace("\n", "")
    
    print("start crawler on {title}, decoding the identifications...".format(title=title))
    index = ['准考證號碼', "考區", '校系名稱']
        
    exam_dis = None
    df_ = pd.DataFrame(columns=index)
    img_num = -1
    count = 0
    while True:
        if( count >= 4):
            school_list = []
            result = element.xpath('//*[@id="mainContent"]/table[1]/tbody/tr[{}]/td[3]/div/img'.format(count))
            for i in result:
                src = i.get('src')
                img_num = decoder.base64_to_text(src)
            search_school = element.xpath('//*[@id="mainContent"]/table[1]/tbody/tr[{}]/td[5]/div[1]/div/table'.format(count))
            for i in search_school:
                school = i.xpath('.//a')
                for j in school:
                    text = j.text
                    if(text != None):
                        school_list.append(text)
            exam_district = element.xpath('//*[@id="mainContent"]/table[1]/tbody/tr[{}]/td[3]/div/a/text()'.format(count)) 
            for i in exam_district:
                if( len(i.replace("\n","").replace(" ","").replace("\r","")) > 0 ):
                    exam_dis = i.replace("考區 :","")
            if ( img_num != -1 and len(school_list) > 0 ):
                df_ = df_.append(pd.Series((img_num, exam_dis, ",".join(school_list)), index=df_.columns), ignore_index=True)
            if ( len(result) < 1 or len(school) < 1 ):
                break
        count += 1

    return df_, title

def html2(html_file):

    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    element = etree.HTML(str(soup))

    title = element.xpath('//*[@id="mainContent"]/table/tbody/tr[1]/td/div/text()[2]')
    for i in title:
        title = i.replace("\n", "")
    
    print("start crawler on {title}, decoding the identifications...".format(title=title))

    index = ['准考證號碼', '校系名稱']
    df_ = pd.DataFrame(columns=index)
    img_num = -1
    count = 0
    while True:
        if( count >= 4):
            school_list = []
            result = element.xpath('//*[@id="mainContent"]/table/tbody/tr[{}]/td[3]/img'.format(count))
            for i in result:
                src = i.get('src')
                img_num = decoder.base64_to_text(src)
            search_school = element.xpath('//*[@id="mainContent"]/table/tbody/tr[{}]/td[5]/div[1]/div/table'.format(count))
            for i in search_school:
                school = i.xpath('.//a')
                for j in school:
                    text = j.text
                    if(text != None):
                        school_list.append(text)
            if ( img_num != -1 and len(school_list) > 0 ):
                df_ = df_.append(pd.Series((img_num, ",".join(school_list)), index=df_.columns), ignore_index=True)
            if ( len(result) < 1 or len(school) < 1 ):
                break
        count += 1

    return df_, title

year = 112

path, dirs, files = next(os.walk("./html/{year}/".format(year=year)))

# for i in range(1, len(files)+1):
#     print("--------")
#     url = './html/{year}/nsysu_{no}.html'.format(year=year, no=i)
#     dataframe, title = html1(url)
#     dataframe.to_csv('./csv/{}/{}.csv'.format(year, title), index=False, encoding='utf-8-sig')


path, dirs, files = next(os.walk("./html/{year}_統測/".format(year=year)))
for i in range(1, len(files)+1):
    print("--------")
    url = './html/{year}_統測/nsysu_{no}.html'.format(year=year, no=i)
    dataframe, title = html2(url)
    dataframe.to_csv('./csv/{}_統測/{}.csv'.format(year, title), index=False, encoding='utf-8-sig')
