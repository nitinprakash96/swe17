import os
from flask import render_template

# Import the main Flask app
from app import app

# Get Blueprint Apps
from auth import auth

# Register Blueprints
app.register_blueprint(auth)

@app.route('/')
def home():
    return render_template('index.html')

# start the server
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 8000))
app.run(host='127.0.0.1', port=port)
