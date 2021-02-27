from flask import Flask, render_template, jsonify

app = Flask(__name__)


class FlaskException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status_code'] = self.status_code
        rv['message'] = self.message
        return rv


class InvalidUsage(FlaskException):
    status_code = 400

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response




@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    if list_type not in ['ol', 'ul']:
        raise InvalidUsage(f'Invalid parameter: {list_type}')

    prof_list = ["Инженер исследователь", "Пилот", "Строитель", "Экзобиолог"]

    return render_template('list_prof.html', list_type=list_type, prof_list=prof_list)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
