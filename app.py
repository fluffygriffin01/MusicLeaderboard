from flask import Flask, request, jsonify
import controller

app = Flask(__name__)

@app.route('/api/artist/leaderboard/10', methods=['GET'])
def get_top_ten_artists():    
    try:
        response = controller.get_top_artists(10)
        return jsonify(response)
    except Exception as e:
        return jsonify({"Failed to retrieve artist leaderboard": 500, "Error": str(e)})
    
@app.route('/api/artist/id', methods=['GET'])
def get_artist_by_id():    
    try:
        data = request.json
        response = controller.get_artist_by_id(data.get('id'))
        return jsonify(response)
    except Exception as e:
        return jsonify({"Failed to retrieve artist by id": 500, "Error": str(e)})
    
@app.route('/api/artist/name', methods=['GET'])
def get_artist_by_name():    
    try:
        data = request.json
        response = controller.get_artist_by_name(data.get('name'))
        return jsonify(response)
    except Exception as e:
        return jsonify({"Failed to retrieve artist by name": 500, "Error": str(e)})

@app.route('/api/artist/create', methods=['POST'])
def create_artist():
    try:
        data = request.json
        added_artist = controller.add_artist(data.get('name'), data.get('email'))
        if added_artist:
            return jsonify({"Succssessfully created artist": 200})
        else:
            raise Exception("Failed to create artist.")
    except Exception as e:
        return jsonify({"Failed to create artist": 400, "Error": str(e)})
    
@app.route('/api/artist/update', methods=['PUT'])
def update_artist():
    try:
        data = request.json
        updated_artist = controller.update_artist(int(data.get('id')), data.get('name'), data.get('email'), 
            int(data.get('listeners')), int(data.get('followers')), int(data.get('songs')), int(data.get('albums')))
        if updated_artist:
            return jsonify({"Succssessfully updated artist": 200})
        else:
            raise Exception("Failed to update artist.")
    except Exception as e:
        return jsonify({"Failed to update artist": 400, "Error": str(e)})
    
@app.route('/api/artist/delete', methods=['DELETE'])
def delete_artist():
    try:
        data = request.json
        deleted_artist = controller.remove_artist(data.get('name'))
        if deleted_artist:
            return jsonify({"Succssessfully deleted artist": 200})
        else:
            return jsonify({"Artist not found": 200})
    except Exception as e:
        return jsonify({"Failed to delete artist": 400, "Error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=6000)