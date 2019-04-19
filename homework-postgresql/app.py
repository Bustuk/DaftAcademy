import os

from flask import Flask, abort, render_template, request, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models import Base

DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_engine("postgresql://postgres:postgres@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 404

    def __init__(self, error, status_code=None, payload=None):
        super().__init__(self)
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/artists", methods=["GET", "PATCH", "POST"])
def artists():
    if request.method == "GET":
        return get_artists()
    elif request.method == "PATCH":
        return patch_artist()
    elif request.method == "POST":
        return post_artists()
    else:
        abort(405)

   
@app.route("/albums")
def get_albums():
    albums = db_session.query(models.Album).order_by(models.Album.title)
    return render_template("albums.html", albums=albums)


@app.route("/count_songs")
def count_songs():
    a = request.args
    if ('artist' in a):
        art = str(a['artist'])
        art = art.split(",")

    else:
        abort(404)
    try:
        result_dict = {}
        songs = (
            db_session.query(models.Artist.name, func.count(models.Track.name))
                .join(models.Track.album)
                .join(models.Album.artist)
                .filter(models.Artist.name.in_(art))
                .group_by(models.Artist.name)
        )
        if len(songs.all()) == 0:
            abort(404)

        for u in songs.all():
            result_dict[u[0]] = u[1]

        return jsonify(result_dict)
    except:
        abort(404)


@app.route("/longest_tracks")
def longest_tracks():
    tracks = db_session.query(models.Track).order_by(models.Track.milliseconds.desc()).limit(10)
    print(tracks)
    result_dict = []
    for u in tracks.all():
        result_dict.append(u.__dict__)
    for i in result_dict:
        del i['_sa_instance_state']
        dic = list(i.keys())
        for di in dic:
            i[di] = str(i[di])
    return jsonify(result_dict)

@app.route("/playlists")
def get_playlists():
    playlists = db_session.query(models.Playlist).order_by(
        models.Playlist.name)
    return render_template("playlists.html", playlists=playlists)


@app.route("/longest_tracks_by_artist")
def longest_tracks_by_artist():
    a = request.args
    if ('artist' in a):
        art = a['artist']
    else:
        abort(404)
    try:
        tracks = db_session.query(models.Track).join(models.Track.album).join(models.Album.artist).filter(
            models.Artist.name == art).order_by(models.Track.milliseconds.desc()).limit(10).all()
        result_dict = []
        for u in tracks:
            result_dict.append(u.__dict__)
        for i in result_dict:
            del i['_sa_instance_state']
            dic = list(i.keys())
            for di in dic:
                i[di] = str(i[di])

        if len(result_dict) == 0:
            abort(404)

    except:
        abort(404)

    return jsonify(result_dict)


def patch_artist():
    data = request.json
    artist_id = data.get("artist_id")
    new_name = data.get("name")
    if artist_id is None:
        abort(404)
    artist = (
        db_session.query(models.Artist)
            .filter(models.Artist.artist_id == artist_id)
            .with_for_update()
            .one()
    )
    artist.name = new_name
    db_session.add(artist)
    db_session.commit()
    return "OK"

def get_artists():
    artists = db_session.query(models.Artist).order_by(models.Artist.name)
    return "<br>".join(


        f"{idx}. {artist.name}" for idx, artist in enumerate(artists)
    )

def post_artists():
    data = request.json
    new_name = data.get("name")
    if new_name is None or len(data) != 1:
        abort(400)

    try:
        art = models.Artist(name=new_name)
        db_session.add(art)
        db_session.commit()

        artist = db_session.query(models.Artist).filter(models.Artist.name == new_name).with_for_update().one()
        result_dict = artist.__dict__
        print(result_dict)

        del result_dict['_sa_instance_state']
        dic = list(result_dict.keys())
        for di in dic:
            result_dict[di] = str(result_dict[di])

        return jsonify(result_dict[0])
    except:
        abort(400)




if __name__ == "__main__":
    app.run(debug=False)

#
