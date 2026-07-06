from flask import Flask
import os
app = Flask(__name__)

@app.route("/version", methods=['GET'])
def version():
    return os.environ['VERSION']

@app.route("/process_etds/<date>", methods=['GET'])
def process_etds(date):
    return "processed " + str(date)

@app.route("/process_chc", methods=['GET'])
def process_chc():
  return "processed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
