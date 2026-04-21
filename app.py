from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # سيقوم الآن بفتح ملف index.html الموجود في مجلد templates
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
