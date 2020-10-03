import pymongo


class MongoDBApi:
    # Create mongo client connection to Mongo Cloud DB.
    def __init__(self):
        self.mongoClient = pymongo.MongoClient(
            "mongodb+srv://dimagurevich:Sibo1989@cluster0-kcwxg.mongodb.net/test?retryWrites=true&w=majority")
        # use database named "movies" & collection : movies_data
        self.myDB = self.mongoClient["movies"]
        self.movies_data = self.myDB["movies_data"]

    # use collection named "movies_data"
    # insert a json to the collection
    def createCollections(self, movie_json):
        try:
            updateQuery = {"$set": {"imdb": movie_json["imdb"]}}
            self.movies_data.update(movie_json, updateQuery, upsert=True)
        except Exception as e:
            print(e.__cause__)

    def findMovieById(self, imdb_id):
        try:
            return self.movies_data.find_one({"imdb": imdb_id})
        except Exception as e:
            print(e.__cause__)

    def getCollectionCount(self):
        return self.movies_data.count()
