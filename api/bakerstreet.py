from flask import Flask, render_template, request, session
from dashboard import get_player, level_one_stats, level_two_stats, level_three_stats
from level import get_items, get_level
from answer import check


app = Flask(__name__)
app.secret_key = 'Secret Key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard', methods=["POST"])
def dashboard():
    player = request.form.get('name').lower()
    code = request.form.get('code').lower()

    if not player or not code:
        return render_template('index.html')

    player = get_player(player, code)

    if not player:
        return render_template('index.html')

    session['playerid'] = player.id
    session['playername'] = player.name

    data = {
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
        'level': get_level(level),
        'items': get_items(level)
    }

    return render_template('level.html', data=data)


@app.route('/answer', methods=["GET", "POST"])
def answer():
    # Check session is still active
    if not session:
        render_template("index.html", data='timeout')

    level = request.args.get('l')
    item = request.args.get('q')
    answer = request.form.get('a')

    if check(item, answer, session['playerid']):
        return render_template('answer.html', data={"answer": True, "level": level})
    else:
        return render_template('answer.html', data={"answer": False, "level": level})


if __name__ == '__main__':
    app.run(debug=True)
