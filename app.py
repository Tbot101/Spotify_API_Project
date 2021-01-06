from flask import Flask, render_template, request, session, redirect
import json
import backend

app = Flask(__name__)
obj = backend.lastFmSpotify()

app.secret_key = 'fweSjieEJKp'

topsongs = obj.fetch_songs_from_lastfm()


@app.route('/')
def hello_world():
    return redirect('/create')


@app.route('/top', methods=['GET', 'POST'])
def top_songs():
    if request.method == 'GET':
        return render_template('index.html', topsongs=topsongs, template='top')
    else:
        if 'id' in session.keys():
            uri = obj.get_uri_from_spotify(topsongs)
            playlist_id = session['id']
            ans = obj.add_songs_to_playlist(uri, playlist_id)
            return redirect('/view')
        return redirect('/create')


@app.route('/create', methods=['GET', 'POST'])
def create_playlist():
    print(request.method)
    if request.method == 'GET':
        return render_template('index.html', template='create')
    if request.method == 'POST':
        name = request.form["playlist_name"].strip()
        desc = request.form["playlist_desc"].strip()
        session['id'] = obj.create_spotify_playlist(name, desc)
        return redirect('/top')


@app.route('/view')
def view_songs():
    if 'id' in session.keys():
        songs = obj.list_songs_in_playlist(session['id'])
        return render_template('index.html', songs=songs, template='view')
    return redirect('/create')


if __name__ == '__main__':
    app.run(debug=True)
