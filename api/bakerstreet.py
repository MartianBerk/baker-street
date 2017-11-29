from flask import Flask, render_template, request
from dashboard import validate, level_one_stats, level_two_stats, level_three_stats


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    player = request.args.get('name').lower()
    code = request.args.get('code').lower()

    if not player or not code:
        return render_template('index.html')

    player = validate(player, code)

    if not player:
        return render_template('index.html')

    data = {
        "player": player,
        "totals": [
            {"title": "Level 1", "stats": level_one_stats(player.id)},
            {"title": "Level 2", "stats": level_two_stats(player.id)},
            {"title": "Level 3", "stats": level_three_stats(player.id)}
        ]
    }

    # Return dashboard
    return render_template('dashboard.html', data=data)


@app.route('/level')
def level():
    level = request.args.get('level')

    data = {
        'level': {
            'id': 1,
            'name': 'One'
        }
    }

    return render_template('level.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
