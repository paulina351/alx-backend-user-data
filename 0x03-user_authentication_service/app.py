#!/use/bin/env python3
"""#"""


@app.route
def get("/", method='GET'):
    return flask.jsonify{"message": "Bienvenue"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
