from flask import Flask, render_template, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_socketio import SocketIO, emit
import os
from scheme import *

app = Flask(__name__, root_path='/home/shurik/Work/python/RPGQtWebApp/web_app')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

callback_map_global = None
callback_loc_global = None
callback_char_global = None
callback_char_stat_global = None

def set_callbacks(
        callback_map = None,
        callback_loc = None, 
        callback_char = None, 
        callback_char_stat = None
        ):
    global callback_map_global, callback_loc_global, callback_char_global, callback_char_stat_global
    if callback_map:
        callback_map_global = callback_map
    if callback_loc:
        callback_loc_global = callback_loc
    if callback_char:
        callback_char_global = callback_char
    if callback_char_stat:
        callback_char_stat_global = callback_char_stat
    print(callback_map_global, callback_loc_global, callback_char_global, callback_char_stat_global)

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

def broadcast_reload():
    socketio.emit('reload', {'message': 'Please reload the page'})

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

@app.route('/character/<int:id>')
def character_detail(id):
    character = g.db_session.query(PlayerCharacter).get(id)
    # Получение навыков персонажа по группам
    skills_by_group = {}
    
    stats = g.db_session.query(Stat).filter_by(characterId=id).all()
    
    for stat in stats:
        skill = g.db_session.query(Skill).get(stat.skillId)
        if skill.groupName not in skills_by_group:
            skills_by_group[skill.groupName] = []
        skills_by_group[skill.groupName].append([id, skill.id, skill.name, stat.value, stat.initValue])
    print(skills_by_group)
    return render_template('character_detail.html', character=character, skills_by_group=skills_by_group)

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
        return {'success': True}
    
    return {'success': False}, 400

if __name__ == '__main__':
    app.run(debug=True)