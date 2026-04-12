from flask import Flask, jsonify, render_template

from flask_cors import CORS

import threading

import controller



app = Flask(

    __name__,

    template_folder="../templates",

    static_folder="../static"

)



CORS(app)



@app.route("/")

def home():

    return render_template("index.html")



def run_controller():
    print("Controller")
    controller.main()



@app.route("/run", methods=["GET"])

def run():

    print("🔥 /run endpoint hit")

    threading.Thread(target=run_controller).start()

    return jsonify({"status": "Controller started"})



if __name__ == "__main__":

    app.run(debug=True, port=5000)

