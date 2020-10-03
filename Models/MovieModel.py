from json import JSONEncoder
from Models.TorrentModel import *
from DB.MongoDBApi import *

mongoDB = MongoDBApi()


class MovieModel:

    def __init__(self, movieDict):
        self.title = movieDict["title"].replace("\"", '')
        self.genres = []
        self.id = movieDict["id"]
        self.poster_path = ""
        if "image" in movieDict:
            self.poster_path = movieDict["image"]
        if "releaseState" in movieDict:
            self.release_date = movieDict["releaseState"] + " " + movieDict["year"]
        else:
            self.release_date = movieDict["year"]
        self.rating = ""
        if "imDbRating" in movieDict:
            self.rating = movieDict["imDbRating"]
        if "crew" in movieDict:
            self.actors = movieDict["crew"]
        elif "stars" in movieDict:
            self.actors = movieDict["stars"]
        self.imdb_link = self.create_imdb_link("http://imdb.com/title/{0}".format(self.id))
        self.popcornTime = self.create_stream_links().get("PopcornTime")
        self.iSubsMovies = self.create_stream_links().get("ISubsMovies")
        self.torrents = []
        movieDbObject = mongoDB.findMovieById(self.id)
        if movieDbObject is not None:
            self.genres = movieDbObject["genres"]
            self.torrents = self.attach_torrents(movieDbObject["items"])
        elif "genres" in movieDict:
            self.genres = movieDict["genres"]

    @staticmethod
    def create_imdb_link(link):
        return link

    # create stream links -> Popcorn Time / SubsMovies
    def create_stream_links(self):
        links = {}
        try:
            if self.id is not None:
                links["PopcornTime"] = "https://popcorntime-online.io/" + str(self.title).replace(" ", "-"). \
                    replace("(", "").replace(")", "") + ".html?imdb=" + self.id
                links["ISubsMovies"] = ("https://isubsmovies.com/movie/{0}".format(self.id))
        except:
            print("Error create_stream_links!!")
        for key in links.keys():
            value = links.get(key)
            links[key] = value
        return links

    def attach_torrents(self, torrentsDict):
        torrents = []
        for t in torrentsDict:
            if t["torrent_url"] != "":
                torrentModel = TorrentModel(t, self.title)
                torrents.append(torrentModel)
        return torrents


class jsonEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__
