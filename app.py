from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ootd.db'  # 使用 SQLite 資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料庫模型
class OOTD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.String(50), nullable=False)
    clothes = db.Column(db.String(200), nullable=False)
    tone = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "weather": self.weather, "clothes": self.clothes, "tone": self.tone}


# 建立資料庫
with app.app_context():
    db.create_all()


# RESTful APIs
@app.route('/api/ootd', methods=['POST'])
def create_ootd():
    data = request.json
    new_ootd = OOTD(weather=data['weather'], clothes=data['clothes'], tone=data['tone'])
    db.session.add(new_ootd)
    db.session.commit()
    return jsonify(new_ootd.to_dict()), 201


@app.route('/input_weather', methods=['GET', 'POST'])
def input_weather():
    if request.method == 'POST':
        weather = request.form['weather']
        ootds = OOTD.query.filter_by(weather=weather).all()
        return render_template('index.html', ootds=ootds, weather=weather)
    return render_template('input_weather.html')

@app.route('/api/ootd/<int:id>', methods=['GET'])
def read_ootd(id):
    ootd = OOTD.query.get_or_404(id)
    return jsonify(ootd.to_dict())


@app.route('/api/ootd/<int:id>', methods=['PUT'])
def update_ootd(id):
    ootd = OOTD.query.get_or_404(id)
    data = request.json
    ootd.weather = data.get('weather', ootd.weather)
    ootd.clothes = data.get('clothes', ootd.clothes)
    ootd.tone = data.get('tone', ootd.tone)
    db.session.commit()
    return jsonify(ootd.to_dict())


@app.route('/api/ootd/<int:id>', methods=['DELETE'])
def delete_ootd(id):
    ootd = OOTD.query.get_or_404(id)
    db.session.delete(ootd)
    db.session.commit()
    return jsonify({"message": "OOTD deleted"}), 200


# 頁面功能
@app.route('/')
def index():
    ootds = OOTD.query.all()
    return render_template('index.html', ootds=ootds)


@app.route('/new', methods=['GET', 'POST'])
def new_ootd():
    if request.method == 'POST':
        weather = request.form['weather']
        clothes = request.form['clothes']
        tone = request.form['tone']
        new_ootd = OOTD(weather=weather, clothes=clothes, tone=tone)
        db.session.add(new_ootd)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_ootd(id):
    ootd = OOTD.query.get_or_404(id)
    if request.method == 'POST':
        ootd.weather = request.form['weather']
        ootd.clothes = request.form['clothes']
        ootd.tone = request.form['tone']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', ootd=ootd)


@app.route('/exchange/<int:id>', methods=['GET', 'POST'])
def exchange_tone(id):
    ootd = OOTD.query.get_or_404(id)
    if request.method == 'POST':
        ootd.tone = request.form['tone']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('exchange.html', ootd=ootd)


if __name__ == '__main__':
    app.run(debug=True)
