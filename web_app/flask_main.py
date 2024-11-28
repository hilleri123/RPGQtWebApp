from flask import Flask, render_template, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_socketio import SocketIO, emit
import os
from scheme import *

app = Flask(__name__, template_folder='/home/shurik/Work/python/RPGQtWebApp/web_app/templates')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
        skills_by_group[skill.groupName].append((skill.name, stat.value))
    
    return render_template('character_detail.html', character=character, skills_by_group=skills_by_group)

if __name__ == '__main__':
    app.run(debug=True)