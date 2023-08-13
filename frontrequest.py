from flask import Flask, render_template, request
from backend.apirequest import simplApiPullRequestCall

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formSubmit', methods=['POST'])
async def formSubmit():
    if request.method != 'POST':
        return {"status": False, "message": "Invalid request method."}
    try:
        data = request.get_json()
        response = await simplApiPullRequestCall(data)
        print("final", response)
        if response is True:
            return {"status": True}
        else:
            return {"status": False}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": False, "message": "Error occurred."}


if __name__ == '__main__':
    app.run(debug=True)
