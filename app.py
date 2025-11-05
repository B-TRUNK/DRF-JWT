from flask import Flask

# Flask looks for an 'application' object when running with Gunicorn, 
# so we must name the instance 'application'.
application = Flask(__name__)

@application.route("/")
def index():
    """Returns a simple greeting message."""
    return "<h1>Hello from Flask running on Wasmer WASI! 🚀</h1>"

if __name__ == "__main__":
    # This block is for local testing, Gunicorn will handle the production run.
    application.run(debug=True)