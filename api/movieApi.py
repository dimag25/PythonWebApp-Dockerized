import json
import threading
import time
import traceback

import requests

from Models.MovieModel import MovieModel, jsonEncoder
from api.Constants import *
from DB.MongoDBApi import MongoDBApi

m_counter = 0
isStop = False


def switch_movies(moviesType):
    switcher = {
        "Top250Movies": Constants.top_rated_movies,
        "Top250TVs": Constants.top_rated_tv,
        "MostPopularMovies": Constants.popular_movies,
        "InTheaters": Constants.now_playing_movies,
        "ComingSoon": Constants.upcoming_movies
    }
    return switcher.get(moviesType)


class movieAPI:
    def __init__(self, moviesType):
        self.mongoDBThreads = []
        self.apiThreads = []
        self.lock = threading.Lock()
        self.moviesList = []
        self.moviesIds = []
        self.moviesType = moviesType
        self.dataJson = "["
        self.torrentJson = "["
        self.mongoDBClient = MongoDBApi()

    @staticmethod
    def createValuesJson(movieJson, keys):
        res = ""
        for key, value in movieJson.items():
            if key in keys:
                res += "\"" + str(value) + "\","
        return res

    def saveToMongoDB(self, movieJsons, page):
        self.mongoDBClient.createCollections(movieJsons)
        with self.lock:
            global m_counter
            m_counter += 1
            print("Page: {0}, Saved \"{1}\" Movies to mongo DB".format(page, m_counter))

    def create_movie_model(self, movieResponse):
        movie_model = MovieModel(movieResponse)
        movieJson = jsonEncoder().encode(movie_model)
        self.moviesList.append(movieJson)
        self.dataJson += movieJson + ","  #
        if movie_model.torrents:
            self.torrentJson += str(movieJson.split("\"torrents\": [")[1])[:-2] + ","

    def create_movies_list(self, page):
        start_time = time.time()
        global isStop
        movieURL = Constants.api_domain.format(page)
        response = requests.get(movieURL)
        if response.json() == {"MovieList": []}:
            isStop = True
        for movieJson in response.json()['MovieList']:
            self.saveToMongoDB(movieJson, page)
        with self.lock:
            if response.status_code == 200:
                movieList = response.json()['MovieList']
                for movieResponse in movieList:
                    self.create_movie_model(movieResponse)
        print(" Downloaded Page:%s ---Movies:%s ---  %s seconds ---" % (page, m_counter, time.time() - start_time))

    def create_ImdbModel(self, item):
        start_time = time.time()
        self.create_movie_model(item)
        print(" Create_movieModel : %s ---- Count :%s -----  %s seconds ---" % (
            self.moviesType, self.moviesList.__len__(), time.time() - start_time))

    def createJSon(self, jsonFile, jsonData):
        with open(jsonFile, 'r', encoding="utf-8") as f:
            contents = f.read()
            # json_headers = contents.split("\"data\":")[0]
        with open(jsonFile, 'w', encoding="utf-8") as f:
            try:
                # dataJson = "\"data\":[[" + jsonData
                # dataJson = dataJson[:-2] + "]}"
                f.write(jsonData[:-1] + "]")
            except Exception as e:
                print(e)
                f.write(contents)

    def downloadAllMovies(self):
        page = 0
        while True:
            if isStop:
                break
            page += 1
            try:
                self.create_movies_list(page)
                # t = threading.Thread(target=self.create_movies_list, args=(page,))
                # t.daemon = True
            # t.start()
            # self.mongoDBThreads.append(t)
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                # self.mongoDBThreads.remove(t)
                pass

    def downloadMoviesByType(self, items):
        for item in items:
            try:
                t = threading.Thread(target=self.create_ImdbModel, args=(item,))
                self.apiThreads.append(t)
                t.start()
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                self.apiThreads.remove(t)

    def finalizeFlow(self, start_time, saveToJson=True):
        for t in self.apiThreads:
            t.join()
        print(" Get {0} Movies --- {1} seconds --- Total Movies: {2}".format(self.moviesType,
                                                                             time.time() - start_time,

                                                                             self.moviesList.__len__()))
        if saveToJson:
            self.createJSon(Constants.movies_json_file, self.dataJson)
            self.createJSon(Constants.torrents_json_file, self.torrentJson)
        return self.moviesList

    @staticmethod
    def downloadAndGetMovies(option):
        movieDbApi = movieAPI(option)
        items = requests.get(switch_movies(option)).json()["items"]
        start_time = time.time()
        movieDbApi.downloadMoviesByType(items)
        return movieDbApi.finalizeFlow(start_time, saveToJson=True)

    @staticmethod
    def updateMongoDB():
        movieDbApi = movieAPI("Get_All_Data")
        start_time = time.time()
        movieDbApi.downloadAllMovies()
        return movieDbApi.finalizeFlow(start_time, saveToJson=False)

    @staticmethod
    def getDBValuesCount():
        movieDbApi = movieAPI("Get_All_Data")
        return movieDbApi.mongoDBClient.getCollectionCount()

    @staticmethod
    def getMoviesUpdatedCounter():
        return m_counter

# movieAPI.updateMongoDB()
# movieAPI.downloadAndGetMovies("Top250Movies")
