from flask import Flask, render_template
import json
import backend

app = Flask(__name__)
obj = backend.lastFmSpotify()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/top')
def top_songs():
    topsongs = obj.fetch_songs_from_lastfm()
    return render_template('index.html', topsongs=topsongs, template='top')

@app.route('/create')
def create_playlist():
    return render_template('index.html', template='create')    

if __name__=='__main__':
    app.run(debug=True)