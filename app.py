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



@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')

@app.route('/quakecluster', methods=['GET', 'POST'])
def quakecluster():
    earthquakes = []
    quake = []
    pie = []

    cursor.execute("select count(*) from [all_month]")
    for data in cursor:
        for value in data:
            earthquake_total = value
    print(earthquake_total)

    for i in range(-2, 8):
        cursor.execute("select * from [all_month] where Mag>="+str(i)+" and Mag<="+str(i+1))
        for data in cursor:
            quake.append(data)
        earthquakes.append(quake)
        earthquake_len = len(quake)
        pie.append((earthquake_len/earthquake_total)*100)

    labels = ["Mag((-2)-(-1))","Mag((-1)-0)","Mag(0to1)","Mag(1-2)","Mag(2-3)","Mag(3-4)","Mag(4-5)", "Mag(5-6)","Mag(6-7)","Mag(7-8)"]
    explode = [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]
    colors = ['#ff6666', '#ffcc99', '#99ff99', '#66b3ff']
    plt.pie(pie, labels=labels, colors=colors, explode=explode, autopct='%.0f%%')
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template("magnitude_cluster.html", output = files)


@app.route('/quakeclusterdepth', methods=['GET', 'POST'])
def quakeclusterdepth():
    quake_depth = []
    mag = []
    cursor.execute("select top 500 depth from [all_month]")
    for data in cursor:
        for value in data:
            quake_depth.append(value)

    cursor.execute("select top 500 mag from [all_month]")
    for data in cursor:
        for value in data:
            mag.append(value)

    viridis = cm.get_cmap('viridis', 12)
    colors = viridis(np.linspace(0, 1, len(quake_depth)))
    plt.scatter(quake_depth, mag, c=colors)
    plt.xlabel("Earthquake Depth")
    plt.ylabel("Earthquake Magnitude")
    plt.title("Graph of Earthquake Depth Vs Earthquake Magnitude")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')

    return render_template("earthquake_magdepth.html", output = files)
    
@app.route('/quakeclustermagtype', methods=['GET', 'POST'])
def quakeclustermagtype():
    quake = []
    earthquakes = []
    limits = []
    types = []
    labels = []

    cursor.execute("select distinct Magtype from [all_month]")
    for data in cursor:
        for value in data:
            if value != None:
                types.append(value)

    for i in range(len(types)):
        cursor.execute("select * from [all_month] where Magtype=?",types[i])
        for data in cursor:
            quake.append(data)
        earthquakes.append(quake)
        earthquake_len = len(quake)
        limits.append(earthquake_len)

    cursor.execute("Select distinct Magtype from [all_month]")
    for data in cursor:
        for value in data:
            if value != None:
                labels.append(value)

    print(labels)
    plt.bar(labels, limits, color=(0.9, 0.2, 0.5, 0.2))
    plt.xlabel("Earthquake Type")
    plt.ylabel("Earthquake Count")
    plt.title("Earthquake count based on Type")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template("magnitudetype_cluster.html", output=files)


@app.route('/quakelocation', methods=['GET', 'POST'])
def quakelocation():
    earthquakes = []
    quake = []
    plot = []
    place = request.form.get("Place")
    cursor.execute("select count(*) from [all_month]")
    for data in cursor:
        for value in data:
            earthquake_total = value
    print(earthquake_total)

    for i in range(-2, 8):
        cursor.execute("select * from [all_month] where place like'%"+place+"%'")
        for data in cursor:
            quake.append(data)
        earthquakes.append(quake)
        earthquake_len = len(quake)
        plot.append((earthquake_len/earthquake_total)*100)
    
    labels = ["Mag((-2)-(-1))","Mag((-1)-0)","Mag(0to1)","Mag(1-2)","Mag(2-3)","Mag(3-4)","Mag(4-5)", "Mag(5-6)","Mag(6-7)","Mag(7-8)"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(labels, plot)
    plt.title('Count of Magnitude of a particular location')
    plt.xlabel('Magnitude')
    plt.ylabel('Count of earthquakes')
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    return render_template("quakelocation.html", output=files)

@app.route('/cleaning', methods=['GET', 'POST'])
def cleaning():
    # Store all the filenames
    stop_words = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"}
    n = str(request.form.get('n'))
    n = int(n)
    files = ['text.txt']

    for filename in files:
        print(filename)
        word = []

        # Change the file data into lowercase

        with open(filename, 'r', encoding="utf-8") as input:
            for each_line in input:
                for words in each_line.split():
                    word.append(words.lower())
        # Remove punctuation from the file data

        finaldata = []
        data_tokens = " ".join(word)
        # print(data_tokens)
        # tokens = word_tokenize(data_tokens)
        tokens = (data_tokens.translate(str.maketrans('', '', string.punctuation))).split(" ")
        # print(tokens)
        for word in tokens:
            if word not in stop_words:
                finaldata.append(word)
        exclude = set(string.punctuation)
        # print(finaldata)
        finaldata = [''.join(char for char in str if char not in exclude)
                     for str in finaldata]
        finaldata = list(filter(None, finaldata))

        # Store the cleaned data in new file'
        # os.chdir('static')
        fpathout = filename.split(".")[0] + "_clean.txt"

        with open(fpathout, "w", encoding="utf-8") as output:
            output.write(str(' '.join(finaldata)))

    with open('text_clean.txt', 'r', encoding="utf-8") as input:
        l = input.readline()
        no = l[:n]
        print(no)
    return render_template("clean.html", cleandata=files, n=no)




if __name__ == '__main__':    
    app.run()

