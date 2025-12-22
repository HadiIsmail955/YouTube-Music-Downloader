from ytmusicapi import YTMusic

yt = YTMusic()


def get_artist(artist_id):
    return yt.get_artist(artist_id)


def get_albums(artist):
    return artist.get("albums", {}).get("results", [])


def get_singles(artist):
    return artist.get("singles", {}).get("results", [])


def get_playlists(artist):
    return artist.get("playlists", {}).get("results", [])


def get_songs(artist):
    return artist.get("songs", {}).get("results", [])
