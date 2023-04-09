from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

jots = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_jot', methods=['POST'])
def create_jot():
    name = request.form['name']
    content = request.form['jotspace']
    jot = {'name': name, 'content': content}
    jots.insert(0, jot)
    return render_template('stream.html', jots=jots)


@app.route('/stream')
def stream():
    return render_template('stream.html', jots=jots)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
