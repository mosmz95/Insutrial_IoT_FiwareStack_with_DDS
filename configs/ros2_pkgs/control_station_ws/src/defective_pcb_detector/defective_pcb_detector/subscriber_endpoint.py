from flask import Flask, request

app = Flask(__name__)

@app.route('/update_image', methods=['POST'])
def update_image():
    data = request.get_json(force=True)
    print("Received NGSI payload:")
    print(data)
    return 'Payload received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)




