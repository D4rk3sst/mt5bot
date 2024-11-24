from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if data:
            print('Data received')
            print(data)
            return jsonify({"status": "success", "message": "Data received"}), 200
        else:
            return jsonify({"status": "error", "message": "No data received"}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
