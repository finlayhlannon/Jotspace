import random
import string
from flask import Flask, request, render_template, jsonify, redirect, url_for
import time

app = Flask(__name__, template_folder=".")

# View counts and timers
view_count = 0
mview_count = 0
wview_count = 0
view_timer = int(time.time())
mview_timer = 0
wview_timer = 0

# Dictionary to store jots
jots = {}

# Function to generate a unique URL
def generate_url():
    chars = string.ascii_lowercase + string.digits
    url = ''.join(random.choice(chars) for _ in range(6))
    while url in jots:
        url = ''.join(random.choice(chars) for _ in range(6))
    return url

# Route to create a jot
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

    jots[url] = {'name': name, 'language': language, 'jotspace': jotspace, 'topic': topic, 'password': password}
    print(url)  # Debugging line
    return url, 200, {'Cache-Control': 'no-cache'}

# Route to view a jot
@app.route('/jot/<url>')
def view_jot(url):
    jot = jots.get(url)
    if jot:
        return render_template('jot.html', jot=jot), 200, {'Cache-Control': 'no-cache'}
    else:
        return render_template('error.html'), 404, {'Cache-Control': 'no-cache'}

# Update the view timers outside of the index route
@app.before_first_request
def update_timers():
    global view_timer
    global mview_timer
    global wview_timer
    view_timer = int(time.time())
    mview_timer = int(time.time())
    wview_timer = int(time.time())

# Index route
@app.route('/')
def index():
    global view_count
    global mview_count
    global wview_count
    global view_timer
    global mview_timer
    global wview_timer
    current_time = int(time.time())

    # Reset counters after specific intervals
    if current_time - view_timer >= 86400:  # 86400 seconds in 24 hours
        view_count = 0
        view_timer = current_time

    if current_time - wview_timer >= 604800:  # 604800 seconds in 7 days
        wview_count = 0
        wview_timer = current_time
        print("weekly has reset to 0")

    if current_time - mview_timer >= 2592000:  # 2592000 seconds in 30 days
        mview_count = 0
        mview_timer = current_time
        print("monthly has reset to 0")

    # Increment view counters
    view_count += 1
    mview_count += 1
    wview_count += 1

    # Pass timestamp to template for cache-busting
    return render_template('index.html', view_count=view_count, mview_count=mview_count, wview_count=wview_count, timestamp=current_time), 200, {'Cache-Control': 'no-cache'}

# Cache-Control header to ensure fresh content
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
