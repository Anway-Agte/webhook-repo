from app import create_app
from app.extensions import mongo
app = create_app()
app.config["MONGO_URI"] = "mongodb://localhost:27017/webhook"
mongo.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
