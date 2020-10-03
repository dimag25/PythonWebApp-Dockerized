# file: app.py

import pandas as pd
from flask import Flask, request, render_template, json, jsonify

from api.movieApi import movieAPI, Constants

app = Flask('movieApp')


# Decorator defines a route
# http://localhost:5000/
@app.route('/', methods=['GET'])
def index():
    return GetMoviesAndTorrentsData()


@app.route('/', methods=['POST'])
def startDownload():
    try:
        moviesType = str(request.values['movieType'])
        movieAPI.downloadAndGetMovies(moviesType)
        return GetMoviesAndTorrentsData()

    except Exception as e:
        return render_template('index.html')


def GetMoviesAndTorrentsData():
    moviesColumns, moviesData = getDataFromJson("movies.json", Constants.movieKeys)
    torrentsColumns, torrentsData = getDataFromJson("torrents.json", Constants.torrentsKeys)
    return render_template('index.html', torrentsData=torrentsData, torrentsColumns=torrentsColumns,
                           moviesData=moviesData,
                           moviesColumns=moviesColumns)


def getDataFromJson(jsonFile, keys):
    with open(jsonFile) as json_file:
        js = json.load(json_file)
    df = pd.DataFrame.from_dict(createJsonWithKeys(js, keys))
    data = df.to_dict('records')
    columns = df.columns.values
    return (columns, data)


def createJsonWithKeys(js, keys):
    lst = []
    for jObj in js:
        newJson = {}
        for key, val in jObj.items():
            if key in keys:
                newJson[key] = val
        lst.append(newJson)
    return lst


@app.route('/updateDB', methods=['GET'])
def getDBValues():
    try:
        dbValues = movieAPI.getDBValuesCount()
        movieAPI.updateMongoDB()
        print(jsonify({'dbCount': dbValues}))
        return jsonify({'dbCount': dbValues})
    except Exception as e:
        print(e.__cause__)
        return "Error getting data from Database : " + e.__cause__


if __name__ == '__main__':
    app.run()
