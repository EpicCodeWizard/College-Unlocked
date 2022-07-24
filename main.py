from markdown_to_html import markdown_to_html
from db_helper import db, all, one, db_raw
from deso_helper import upload_to_deso
from uuid_helper import gen_uuid
from predict import predict
from cors import cors
from flask import *
import csv

app = Flask(__name__)
colleges = [{k: v for k, v in row.items()} for row in csv.DictReader(open("College_Data.csv"), skipinitialspace=True)]
for index, college in enumerate(colleges):
  colleges[index]["is_private"] = True if college["is_private"] == "Yes" else False
  colleges[index]["accept"] = int(colleges[index]["accept"])
  colleges[index]["enroll"] = int(colleges[index]["enroll"])
  colleges[index]["fail"] = int(colleges[index]["fail"])
  colleges[index]["graduation_rate"] = int(colleges[index]["graduation_rate"])
  colleges[index]["pass"] = int(colleges[index]["pass"])
db["colleges"] = colleges

@app.route("/advice/all", methods=["GET"])
@cors(origin="*")
def all_advice():
  return jsonify(all("advice"))

@app.route("/advice/get/<aid>", methods=["GET"])
@cors(origin="*")
def get_one_advice(aid):
  try:
    return jsonify(one(aid))
  except:
    return "Not found.", 404

@app.route("/advice/create", methods=["POST"])
@cors(origin="*")
def create_advice():
  data = request.form.to_dict()
  data["aid"] = gen_uuid()
  data["description"] = markdown_to_html(data["description"])
  data["cover"] = upload_to_deso(request.files["cover"])
  db["advice"][data["aid"]] = data
  return ""

@app.route("/colleges/all", methods=["GET"])
@cors(origin="*")
def all_colleges():
  return jsonify(all("colleges"))

@app.route("/colleges/find", methods=["POST"])
@cors(origin="*")
def find_college():
  return jsonify(predict(request.form.to_dict()))

app.run(host="0.0.0.0")
