import datetime


import requests
from bs4 import BeautifulSoup
import cycloon
import numpy as np
import pandas as pd

import re

provinces = {1:"Вінницька", 13 : "Миколаївська", 2:"Волинська", 14:"Одеська", 3:"Дніпропетровська", 15:"Полтавська",
    4:"Донецька", 16:"Рівенська", 5:"Житомирська", 17:'Сумська', 6:"Закарпатська", 18:"Тернопільська", 7:"Запорізька", 19:"Харківська",
    8:"Івано-Франківська", 20:"Херсонська", 9:"Київська", 21:"Хмельницька", 10:"Кіровоградська", 22:"Черкаська", 11:"Луганська", 23:"Чернівецька",
    12:"Львівська", 24:"Чернігівська", 25:"Республіка Крим" }



def get_url(url):
    
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content




def get_provinces_data(what, TYPE=["VHI_Parea", "Mean"]):

    # https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=11&year1=1981&year2=2018&type=Mean

    files = []

    for count in range(0, 2):

        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1={}&year2={}&type={}".format(what, 1982, 2017, TYPE[count])

        resp = get_url(url)

        timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%Hh")#replace(' ', '_').replace('-', '_').replace(':', '_').replace('.', '_')

        filename = '{}_{}_{}-{}_{}.txt'.format(what, TYPE[count], 1982, 2017, "12_05-15h")
        
        #filename = '{}.txt'.format(what)

        file = open(filename, 'wb')
        file.write(str.encode(resp))
        print(filename, " created.")
        files.append(filename)


    return files





def validation(what):
    if int(what) not in dict.keys(provinces):
        return False
    else:
        return True


def choose_province():
    print("Hey, choose province and years you need: (E.g. 11 2017 2018) ")
    for every in dict.keys(provinces):
        print(every, " <=> ", provinces[every])

    what = input("Your choice: ")

    if validation(what):
        print("Proceeding...")
        return(get_provinces_data(what))

    else:
        print("Something wrong!")
        a = input("Try again?[y/n]")
        if a == 'y' or a == "Y":
            chose_province()
        elif a == 'n' or a == 'N':
            print("Bye.")
            exit()


def mean_file(file):
        raw = open(file,'r+')
        headers = raw.readline().rstrip()
        headers = headers.split(',')[:2] + headers.split(',')[4:]
        data = raw.readlines()

        result = []

        # deleting stuff to get it in df
        for every in data:
            result.append(str(re.sub(r',\s\s|\s\s|\s|,\s',',',every)[:-1]).split(','))


        df = pd.DataFrame(result,columns=headers)

        return df

def vhi_file(file):
    raw = open(file,'r+')
    headers = raw.readline().rstrip()
    headers = headers.split(',')[:2] + headers.split(',')[4:]
    data = raw.readlines()

    result = []

    # deleting stuff to get it in df
    for every in data:
        result.append(str(re.sub(r'\s\s\s|,\s\s|\s\s|,\s|\s',',',every)[:-1]).split(','))

    df = pd.DataFrame(result,columns=headers)

    # print(df)

    return df


def get_data_from_txt_to_df(filenames):
    for file in filenames:
        if "Mean" in file:
            df_mean = mean_file(file)
            return df_mean
        if "VHI" in file:
            df_vhi =vhi_file(file)
            return  df_vhi



def get_file_to_normal_stage(filenames):
    for file in filenames:
        data = open(file,'r').read()
        data = data[data.find('<pre>')+5:data.find("</pre></tt>")]

        write_to = open(file,'w').write(data)

def need_file( TYPE=["VHI_Parea", "Mean"]):
        file=[]
        what = input("Your choice: ")
        #file = ("downloads/{}.csv").format(what)
        #df = pd.read_csv(file,index_col=False)
        #return df
        for i in range(0, 2):
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d-%Hh")
            filename = '{}_{}_{}-{}_{}.txt'.format(what, TYPE[i], 1982, 2017, "12_05-15h")
            file.append(filename)
        return file   
def min_max(filenames):
    df = pd.read_csv(filenames,encoding = 'utf8', sep = ',',index_col=False, header=0)#mean_file(filenames)
    np_matrix = df.values
    A = np_matrix.shape

    k = 0
    percen = 10                   #<-- print percent
    while True:
        if k == A[0]:
            break
        if np_matrix[k][percen] < 15:
            print(np_matrix[k][0], " VHI < 15(extremal drought): ", np_matrix[k][percen])
        else:
            if np_matrix[k][percen] < 35:
                print(np_matrix[k][0], " VHI < 35(moderate drought): ", np_matrix[k][percen])
        k = k+1
        
    k = 0
    year = 2000
    yyear = str(year)

    #txtcsv1 = txt1+area_id+txtcsv
    # df = pd.read_csv(filenames,encoding = 'utf8', sep = ',',index_col=False, header=0)
    # np_matrix = df.values
    # A = np_matrix.shape

    # percen = 6
    # max_a = 0
    # min_a = 0
    # puma = 0
    # while k != A[0]-1:
        
        # lima = np_matrix[k][0]
        # lim = int(lima)
          
        # if year == lim:
            # if puma == 0:
                # min_a = np_matrix[k][percen]
                # puma = 1
                

        # if year == lim:
            # if np_matrix[k][percen] > max_a:
                # max_a = np_matrix[k][percen]
                # print(k)
            # if np_matrix[k][percen] < min_a:
                # min_a = np_matrix[k][percen]
                # print(k)
        # k = k+1
    
    # print("Max for ", yyear,  " is: ", max_a)
    # print("Min for ", yyear,  " is: ", min_a)

def main():
    filenames = choose_province()
    get_file_to_normal_stage(filenames)
    df_vhi = get_data_from_txt_to_df(filenames)
    name = need_file()
    print(name)
    for i in name:
        if "VHI" in i:  
            df = vhi_file(i)
            print(df.head(40))
            min_max(i)
            #print(df.idxmax())
            #print(df.min())
            #print(df.max())

        else:
            df = mean_file(i)
            
            print(df.head(20))







if __name__ == "__main__":

    main()

     #df = vhi_file("13_VHI_Parea_2017-2018(2018-11-18 22:27:19.221941).txt")




     #print(df.VHI.max())

    # print(df1.head(20))


    # res = 0
    # for every in df.VHI:
    #     if  float(every) > 25:
    #         res += 1

    # print("res= ", res)
    # get_file_to_normal_stage(["11_Mean_2017-2018(2018-11-12 08:46:54.301805).txt"])
