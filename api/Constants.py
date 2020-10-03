import os


class Constants:
    movies_json_file = os.path.realpath(os.path.join(os.getcwd(), "./movies.json"))
    torrents_json_file = os.path.realpath(os.path.join(os.getcwd(), "./torrents.json"))
    api_domain = "https://api.apidomain.info/list?quality=720p,1080p,3d&page={0}"
    movieKeys = ["title", "genres", "release_date", "imdb_link", "popcornTime", "iSubsMovies"]
    torrentsKeys = ["title", "quality", "torrent_peers", "torrent_seeds", "torrent_url"]
    upcoming_movies = "https://imdb-api.com/en/API/ComingSoon/k_a24Jvt5R"
    top_rated_movies = "https://imdb-api.com/en/API/Top250Movies/k_a24Jvt5R"
    top_rated_tv = "https://imdb-api.com/en/API/Top250TVs/k_a24Jvt5R"
    now_playing_movies = "https://imdb-api.com/en/API/InTheaters/k_a24Jvt5R"
    popular_movies = "https://imdb-api.com/en/API/MostPopularMovies/k_a24Jvt5R"
