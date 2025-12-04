from flask import Flask, request, jsonify
import leaderboard

app = Flask(__name__)

@app.route('/api/artist_leaderboard/10', methods=['GET'])
def get_top_ten_artists():    
    try:
        response = leaderboard.get_top_artists(10)
        return jsonify(response)
    except Exception as e:
        return jsonify({"Failed to retrieve artist leaderboard": 500, "Error": str(e)})

@app.route('/api/artist_leaderboard/create', methods=['POST'])
def create_artist():
    try:
        data = request.json
        added_artist = leaderboard.add_artist(data.get('name'), data.get('score'))
        if added_artist:
            return jsonify({"Succssessfully created artist": 200})
        else:
            raise Exception("Failed to create artist.")
    except Exception as e:
        return jsonify({"Failed to create artist": 400, "Error": str(e)})
    
@app.route('/api/artist_leaderboard/update', methods=['PUT'])
def update_artist():
    try:
        data = request.json
        updated_artist = leaderboard.update_artist(data.get('name'), data.get('score'))
        if updated_artist:
            return jsonify({"Succssessfully updated artist": 200})
        else:
            raise Exception("Failed to update artist.")
    except Exception as e:
        return jsonify({"Failed to update artist": 400, "Error": str(e)})
    
@app.route('/api/artist_leaderboard/delete', methods=['DELETE'])
def delete_artist():
    try:
        data = request.json
        deleted_artist = leaderboard.remove_artist(data.get('name'))
        if deleted_artist:
            return jsonify({"Succssessfully deleted artist": 200})
        else:
            return jsonify({"Artist not found": 200})
    except Exception as e:
        return jsonify({"Failed to delete artist": 400, "Error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=6000)