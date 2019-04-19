from flask import Flask, jsonify, request, g
import sqlite3


app = Flask(__name__)


@app.route('/')
def root():
    return 'Hello, World!'




DATABASE = "db\\chinook.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/genres')
def genres_list():
    db = get_db()
    cursor = db.cursor()
    data = cursor.execute('''
        SELECT count(tracks.GenreId), genres.Name  from tracks
        join genres on tracks.GenreId=genres.GenreId
        GROUP by genres.Name ''').fetchall()
    cursor.close()
    result=dict()
    for element in data:
        result[element[1]]=int(element[0])

    return jsonify(result)




@app.route('/tracks', methods=['GET','POST'])
def tracks_list():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'GET':
        user = request.args.get('artist')
        limit = request.args.get('per_page')
        page = request.args.get('page') or 1
        if user is not None and (page is None or limit is None):
            data = cursor.execute('''SELECT tracks.name FROM tracks
                                         JOIN albums on tracks.albumid=albums.albumid
                                         JOIN artists on albums.artistid=artists.artistid WHERE artists.name=\'{}\' COLLATE NOCASE ORDER by tracks.name'''.format(
                user))
        else:
            data = cursor.execute('SELECT name FROM tracks ORDER BY tracks.name')

        if limit is not None:
            page = int(page) - 1
            offset = int(page) * int(limit)
            if user is not None:
                data = cursor.execute('''SELECT tracks.name FROM tracks
                                                     JOIN albums on tracks.albumid=albums.albumid
                                                     JOIN artists on albums.artistid=artists.artistid WHERE artists.name=\'{}\' COLLATE NOCASE ORDER by tracks.name
                                                     LIMIT {} OFFSET {};'''.format(user, limit, offset))
            else:
                data = cursor.execute('''SELECT name FROM tracks ORDER BY tracks.name COLLATE NOCASE
                                                     LIMIT {} OFFSET {};'''.format(limit, offset))
        return jsonify([row[0] for row in data.fetchall()])
    else:
        json_data = request.get_json()
        if json_data == None:
            cursor.close()
            return 400
        else:
            try:
                album_id = json_data.get('album_id')
                media_type_id = json_data.get('media_type_id')
                genre_id = json_data.get('genre_id')
                name = json_data.get('name')
                composer = json_data.get('composer')
                milliseconds = json_data.get('milliseconds')
                bbytes = json_data.get('bytes')
                price = json_data.get('price')
            except:
                return 'incomplete data', 400

            else:
                cursor.execute('''INSERT INTO tracks (name, albumid, mediatypeid, genreid, composer, milliseconds, bytes, unitprice)
                                          VALUES (?,?,?,?,?,?,?,?)''',
                               (name, album_id, media_type_id, genre_id, composer, milliseconds, bbytes, price))
                data = cursor.execute('''SELECT * FROM tracks
                                                    WHERE trackid = (SELECT MAX(trackid)  FROM tracks)''').fetchone()
            cursor.close()
            return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
