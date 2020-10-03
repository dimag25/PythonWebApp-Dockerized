class TorrentModel():
    def __init__(self, torrentDict, title):
        self.title = title
        self.quality = torrentDict["quality"]
        self.torrent_peers = torrentDict["torrent_peers"]
        self.torrent_seeds = torrentDict["torrent_seeds"]
        self.torrent_url = torrentDict["torrent_url"]
