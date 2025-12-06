from flask import Flask, request, jsonify
import controller
import seeder

app = Flask(__name__)

@app.route('/api/artist/seed/100', methods=['POST'])
def seed_artists():    
    try:
        count = seeder.seed_artists(100)
        return jsonify({
            'message': 'Successfully seeded artists',
            'count': count
        }), 200
    except Exception as e:
        return jsonify({
            'message': 'Failed to seed artists',
            'error': str(e)
        }), 400
    
@app.route('/api/artist/leaderboard/10', methods=['GET'])
def get_top_ten_artists():    
    try:
        response = controller.get_top_artists(10)
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve artist leaderboard',
            'error': str(e)
        }), 500
    
@app.route('/api/artist/id', methods=['GET'])
def get_artist_by_id():    
    try:
        data = request.json
        response = controller.get_artist_by_id(data.get('id'))
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve artist by id',
            'error': str(e)
        }), 400
    
@app.route('/api/artist/name', methods=['GET'])
def get_artist_by_name():    
    try:
        data = request.json
        response = controller.get_artist_by_name(data.get('name'))
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'message': 'Failed to retrieve artist by name',
            'error': str(e)
        }), 400

@app.route('/api/artist/create', methods=['POST'])
def create_artist():
    try:
        data = request.json
        added_artist = controller.add_artist(data.get('name'), data.get('email'))
        if added_artist:
            return jsonify({'message': 'Succssessfully created artist'}), 200
        else:
            raise Exception('Failed to create artist.')
    except Exception as e:
        return jsonify({
            'message': 'Failed create artist',
            'error': str(e)
        }), 400
    
@app.route('/api/artist/update', methods=['PUT'])
def update_artist():
    try:
        data = request.json
        updated_artist = controller.update_artist(int(data.get('id')), data.get('name'), data.get('email'), 
            int(data.get('listeners')), int(data.get('followers')), int(data.get('songs')), int(data.get('albums')))
        if updated_artist:
            return jsonify({'message': 'Succssessfully updated artist'}), 200
        else:
            raise Exception('Failed to update artist.')
    except Exception as e:
        return jsonify({
            'message': 'Failed to update artist',
            'error': str(e)
        }), 400
    
@app.route('/api/artist/delete', methods=['DELETE'])
def delete_artist():
    try:
        data = request.json
        deleted_artist = controller.remove_artist(data.get('name'))
        if deleted_artist:
            return jsonify({'message': 'Succssessfully deleted artist'}), 200
        else:
            return jsonify({'message': 'Artist not found'}), 200
    except Exception as e:
        return jsonify({
            'message': 'Failed to delete artist',
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=6000)