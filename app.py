from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "تطبيق التحليلات الرياضية والذكاء الاصطناعي يعمل بنجاح على Render!"

@app.route('/predict')
def predict():
    # هنا سنضع خوارزمية الذكاء الاصطناعي لاحقاً
    return jsonify({
        "match": "Real Madrid vs Barcelona",
        "prediction": "Home Win",
        "confidence": "85%"
    })

if __name__ == "__main__":
    app.run(debug=True)
