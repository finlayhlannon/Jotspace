

import random
import string
from flask import Flask, request, render_template, jsonify, redirect

app = Flask(__name__, template_folder=".")

# Define a dictionary to store the jots
jots = {}

@app.route('/')
def index():
    return render_template('index.html')

# Define a function to generate a unique URL
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
    url = generate_url()
    jots[url] = {'name': name, 'jotspace': jotspace}
    print(url)  # Debugging line
    return redirect(f'/jot/{url}')



# Define the route to view a jot
@app.route('/jot/<url>')
def view_jot(url):
    jot = jots.get(url)
    if jot:
        return render_template('jot.html', jot=jot)
    else:
        return 'Jot not found'

if __name__ == '__main__':
    app.run(debug=True)
