from flask import Flask, request ,render_template  # Flaskは必須、requestはリクエストパラメータを処理する場合に使用します。
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')



if __name__ == '__main__':
    app.run(debug=True)