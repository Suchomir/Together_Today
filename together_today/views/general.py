import time
from datetime import datetime
from flask import Blueprint, render_template, Response
from flask_login import login_required


general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/", methods=["GET"])
def index():
        return render_template("general/index.html")


@general_blueprint.route('/time_feed') 
@login_required
def time_feed():
        def generate():
                yield datetime.now().strftime("%H:%M:%S")
        return Response(generate(), mimetype='text') 