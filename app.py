from flask import Flask
from flask_cors import CORS
from routes.user_routes import user_blueprint
from routes.document_routes import document_blueprint
from routes.query_routes import query_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(document_blueprint)
app.register_blueprint(query_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
