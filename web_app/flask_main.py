from flask import Flask, render_template, request, send_file, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
import os
from scheme import *

WEB_APP_DIR = f'{os.getcwd()}/web_app'

app = Flask(__name__, root_path=WEB_APP_DIR)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

callback_map_global = None
callback_loc_global = None
callback_item_global = None
callback_char_global = None
callback_char_stat_global = None
callback_connection_global = None

def set_callbacks(
        callback_map = None,
        callback_loc = None, 
        callback_item = None, 
        callback_char = None, 
        callback_char_stat = None,
        callback_connection = None
        ):
    global callback_map_global, callback_loc_global, callback_item_global, callback_char_global, callback_char_stat_global, callback_connection_global
    if callback_map:
        callback_map_global = callback_map
    if callback_loc:
        callback_loc_global = callback_loc
    if callback_item:
        callback_item_global = callback_item
    if callback_char:
        callback_char_global = callback_char
    if callback_char_stat:
        callback_char_stat_global = callback_char_stat
    if callback_connection:
        callback_connection_global = callback_connection
    # print(callback_map_global, callback_loc_global, callback_char_global, callback_char_stat_global)

@app.before_request
def before_request():
    # Создаем новую сессию для каждого запроса
    g.db_session = SessionMaker()

@app.teardown_request
def teardown_request(exception):
    # Закрываем сессию после завершения запроса
    db_session = getattr(g, 'db_session', None)
    if db_session is not None:
        db_session.close()

@app.route('/')
def index():
    characters = g.db_session.query(PlayerCharacter).all()
    return render_template('index.html', characters=characters)

def get_client_ip():
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    return ip_addr

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Здесь можно обновить путь к изображению в базе данных
        return redirect(url_for('index'))

@app.route('/player/<int:id>')
def player(id):
    character = g.db_session.query(PlayerCharacter).get(id)
    return render_template('player.html', character=character)

@app.route('/get_global_map_image', methods=['GET'])
def get_global_map_image():
    try:
        return send_file(f'../{GLOBAL_MAP_PATH}', mimetype='image/png')
    except Exception as e:
        print(e)
        return str(e), 404
    
@app.route('/get_curr_map_image', methods=['GET'])
def get_curr_map_image():
    try:
        return send_file(f'../{CURR_MAP_PATH}', mimetype='image/png')
    except Exception as e:
        print(e)
        return str(e), 404

@app.route('/character/<int:id>')
def character_detail(id):
    character = g.db_session.query(PlayerCharacter).get(id)
    # Получение навыков персонажа по группам
    global_map = g.db_session.query(GlobalMap).first()
    global_datetime = datetime.now()
    if global_map and global_map.time:
        global_datetime = global_map.time

    skills_by_group = {}
    stats = g.db_session.query(Stat).filter_by(characterId=id).all()
    
    for stat in stats:
        skill = g.db_session.query(Skill).get(stat.skillId)
        if skill.groupName not in skills_by_group:
            skills_by_group[skill.groupName] = []
        skills_by_group[skill.groupName].append([id, skill.id, skill.name, stat.value, stat.initValue])
    # print(skills_by_group)
    items = g.db_session.query(GameItem).join(WhereObject).filter(WhereObject.playerId == id).all()

    return render_template('character_detail.html', character=character, global_datetime=global_datetime, skills_by_group=skills_by_group, gameitems=items)

@app.route('/update_skill', methods=['POST'])
def update_skill():
    character_id = request.form.get('character_id')
    skill_id = request.form.get('skill_id')
    new_value = request.form.get('new_value')
    character = g.db_session.query(PlayerCharacter).get(character_id)
    if character is None:
        return {'success': False}, 400
    
    address = get_client_ip()
    if character.address != address:
        return {'success': False}, 402

    stat = g.db_session.query(Stat)\
        .filter(Stat.characterId == character_id)\
        .filter(Stat.skillId == skill_id).first()
    if stat:
        callback_data = {int(skill_id): int(stat.value)}
        stat.value = new_value
        g.db_session.commit()
        callback_char_stat_global(int(character_id), callback_data)
        return {'success': True}
    return {'success': False}, 400

@app.route('/update_color', methods=['POST'])
def update_color():
    character_id = request.form.get('character_id')
    color = request.form.get('color')
    character = g.db_session.query(PlayerCharacter).get(character_id)
    if character:
        character.color = color
        g.db_session.commit()
        callback_map_global()
        return {'success': True}
    return {'success': False}, 400

@app.route('/save_address', methods=['POST'])
def save_address():
    character_id = request.form.get('character_id')
    address = get_client_ip()
    
    # Обновите адрес персонажа в базе данных
    character = g.db_session.query(PlayerCharacter).get(character_id)
    if character:
        if character.player_locked:
            return {'success': False}, 402
        character.address = address
        g.db_session.commit()
        callback_connection_global()
        return {'success': True}
    
    return {'success': False}, 400

@app.route('/get_notes/<int:player_id>', methods=['GET'])
def notes(player_id):
    notes = []
    for note in g.db_session.query(Note).all():
        ids = json.loads(note.player_shown_json)
        if player_id in ids:
            notes.append(note)
    return render_template('notes.html', notes=notes)

@app.route('/get_note/<int:note_id>', methods=['GET'])
def note(note_id):
    note = g.db_session.query(Note).get(note_id)
    return note.xml_text if note else ""

@app.route('/get_characters', methods=['GET'])
def get_characters():
    characters = g.db_session.query(PlayerCharacter).all()
    character_data = [{'id': character.id, 'name': character.name} for character in characters]
    return character_data

@app.route('/get_character_story/<int:player_id>', methods=['GET'])
def get_character_story(player_id):
    character = g.db_session.query(PlayerCharacter).get(player_id)
    return character.story if character else ""

@app.route('/process_choice', methods=['POST'])
def process_choice():
    data = request.json
    character_id = data.get('character_id')
    item_id = data.get('item_id')
    choice_id = data.get('choice_id')

    where = g.db_session.query(WhereObject)\
        .filter(WhereObject.gameItemId == item_id)\
        .filter(WhereObject.playerId == character_id).first()
    if where is None:
        return {'success': False}, 400
    
    location_id = None
    npc_id = None
    character_to_id = None
    if choice_id is None:
        player = g.db_session.query(PlayerCharacter).get(character_id)
        if player is None:
            return {'success': False}, 400
        location_id = player.location_id
    else:
        character_to_id = choice_id

    where.npcId = npc_id
    where.locationId = location_id
    where.playerId = character_to_id
    g.db_session.commit()

    if callback_item_global:
        callback_item_global(item_id=item_id, from_player=character_id, to_player=character_to_id, to_location_id=location_id)

    return {'success': True}


def broadcast_reload():
    socketio.emit('reload', {'message': 'Please reload the page'})

def broadcast_character_reload():
    socketio.emit('character_reload', {'message': 'Please reload the page'})

def broadcast_map_reload():
    socketio.emit('map_reload', {'message': 'Please reload the page'})

def broadcast_notes_reload():
    socketio.emit('notes_reload', {'message': 'Please reload the page'})

if __name__ == '__main__':
    app.run(debug=True)