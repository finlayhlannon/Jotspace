import random
import string
from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__, template_folder=".")
view_count = 0

# Define a dictionary to store the jots
jots = {}

# Define a function to generate a unique URL
def generate_url():
    chars = string.ascii_lowercase + string.digits
    url = ''.join(random.choice(chars) for _ in range(6))
    while url in jots:
        url = ''.join(random.choice(chars) for _ in range(6))
    return url

# Define the route to create a jot
@app.route('/create_jot', methods=['POST'])
def create_jot():
    name = request.form['name']
    jotspace = request.form['jotspace']
    language = request.form['language']
    topic = request.form['topic']
    password = request.form['password']
    url = generate_url()
    if language == 'cpp':
        language = 'c++'
    jots[url] = {'name': name, 'language' : language, 'jotspace': jotspace, 'topic': topic, 'password': password}
    print(url)  # Debugging line
    return url

# Define the route to view a jot
@app.route('/jot/<url>')
def view_jot(url):
    jot = jots.get(url)
    if jot:
        return render_template('jot.html', jot=jot)
    else:
        return render_template('error.html')

# Define the index route
@app.route('/')
def index():
    global view_count  # Declare view_count as a global variable
    view_count += 1
    #print(view_count)
    return render_template('index.html', view_count=view_count)


if __name__ == '__main__':
    app.run(debug=True)
