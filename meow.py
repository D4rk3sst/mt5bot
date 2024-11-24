from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    content_type = request.content_type

    if content_type.startswith('text/plain'):
        # Handle plain text
        print('plain text')
        data = request.data.decode('utf-8')
        print('Plain text received')
        print(data)
        return jsonify({"status": "success", "message": "Plain text received"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
