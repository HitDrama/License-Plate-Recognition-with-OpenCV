from flask import Flask
from config import Config
from routes import opencv

app= Flask(__name__)
app.config.from_object(Config)

#đăng ký blueprint
app.register_blueprint(opencv)

if __name__ == "__main__":
    app.run(debug=True)