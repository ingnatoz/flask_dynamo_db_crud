from flask import Flask
from controllers.movie_controller import movie_r
from controllers.bucket_controller import bucket_r

app = Flask(__name__)
app.register_blueprint(movie_r)
app.register_blueprint(bucket_r)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
