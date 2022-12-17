import subprocess
from flask import Blueprint, render_template, make_response, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_, or_


general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/", methods=["GET"])
def index():
        return render_template("general/index.html")