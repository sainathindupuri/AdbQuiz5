from locale import currency
import string
import time
import pyodbc
import os
# import redis
import timeit
import hashlib
import pickle
from flask import Flask, Request, render_template, request, flash
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import numpy as np
import base64

app = Flask(__name__, template_folder="templates")
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbsai.database.windows.net,1433;Database=adb;Uid=sainath;Pwd=Shiro@2018;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
cursor = connection.cursor()

# r = redis.StrictRedis(host='adb-quiz3.redis.cache.windows.net', port=6380, db=0,
#                       password='bGWVXkw0gkglji3NxJ2c4dapdnXSxI8dtAzCaKsPnF8=', ssl=True)





@app.route('/Question10ab', methods=['GET', 'POST'])
def Question10ab():
    # cursor = connection.cursor()    
    inputText = (request.form.get("inputText")).replace(" ", "")
    inputText = inputText.lower()
    all_freq = {}
    all_freq["Alphabet"] = 0
    all_freq["Number"] = 0
    all_freq["Punctuation"] = 0
    for i in inputText:
        if i.isalpha():
            all_freq["Alphabet"] += 1
        elif i.isnumeric():
            all_freq["Number"] = +1
        elif i == "." or i=="," or i=="?" or i=="!" or i=="$" or i =="*":
            all_freq["Punctuation"]+=1
    
    print("freq is ",all_freq)
    sum = 0
    labels = []
    percentageList = []
    freqCountList = []
    labels =list(all_freq.keys())
    for i in labels:
        sum = sum+all_freq[i]
        freqCountList.append((i,all_freq[i]))
    
    for i in freqCountList:
        percentageList.append((i[1]/sum)*100)
    
    colors = ['#ff6666', '#ffcc99', '#99ff99']
    print("labels",labels)
    print("percentage",percentageList)
    plt.pie(percentageList, labels=labels, colors=colors)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    # plt.show()

    return render_template('Question10ab.html', data = freqCountList,count = sum, pieChart = files)  

@app.route('/Question11ab', methods=['GET', 'POST'])
def Question1qab():
    # cursor = connection.cursor()    
    rangeStart = (request.form.get("rangeStart"))
    rangeEnd = (request.form.get("rangeEnd"))

    cursor = connection.cursor()    
   
    query_str1 = "select store,sum(num) from f where store>="+rangeStart+" and store<="+rangeEnd+" group by store"
    query_str2 = "select store,sum(num) from f  group by store"
    cursor.execute(query_str1)    
    data1 = cursor.fetchall()
    cursor.execute(query_str2)
    data2 = cursor.fetchall()
    labels1=[]
    heights1 = []
    labels2=[]
    heights2 = []
    for i in data1:
        labels1.append(i[0])
        heights1.append(i[1])

    for i in data2:        
        labels2.append(i[0])
        heights2.append(i[1])


    plt.bar(labels1, heights1, color=['blue'])
    plt.xlabel("Stores")
    plt.ylabel("Amount of food")
    plt.title("Total amount of foods for each store in entered range")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files1 = figdata_jpeg.decode('utf-8')



    plt.bar(labels2, heights2, color=['blue'])
    plt.xlabel("Stores")
    plt.ylabel("Amount of food")
    plt.title("Total amount of foods for all in entered range")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files2 = figdata_jpeg.decode('utf-8')

    return render_template('Question11.html', output1 = files1, output2=files2)  

@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')




@app.route('/Question12ab', methods=['GET', 'POST'])
def Question12ab():
    
    cursor = connection.cursor()    
    
    query_str = "select * from p"
    cursor.execute(query_str)    
    data = cursor.fetchall()
    x =[]
    y = []
    colors =[]
    for i in data:
       x.append(i[0])
       y.append(i[1])
       colors.append(i[2])    

    
   
    plt.scatter(x, y, c=colors)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Graph")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')

    return render_template("Question12ab.html", output = files)
    

if __name__ == '__main__':    
    app.run()

