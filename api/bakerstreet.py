from flask import Flask, render_template, request
from dashboard import validate, level_one_stats, level_two_stats, level_three_stats


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    player = request.args.get('name').lower()

    if not player:
        return render_template('index.html')

    player = validate(player)
    if not player:
        return render_template('index.html')

    data = {
        "player": player,
        "level_one": level_one_stats(player.id),
        "level_two": level_two_stats(player.id),
        "level_three": level_three_stats(player.id)
    }

    # Return dashboard
    return render_template('dashboard.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
