from flask import Flask, request, jsonify
import leaderboard

app = Flask(__name__)

@app.route('/api/artist_leaderboard', methods=['GET'])
def get_artist_leaderboard():
    response = leaderboard.get_top_ten_artists()
    return jsonify(response)

@app.route('/api/add_artist', methods=['POST'])
def add_artist():
    data = request.json
    try:
        leaderboard.add_artist(data.get('name'), data.get('score'))
        return jsonify({"received": data, "status": "success"})
    except Exception as e:
        print(f"Could not add artist: {e}")
        return jsonify({"received": data, "status": "failed"})

if __name__ == '__main__':
    app.run(debug=True, port=6000)