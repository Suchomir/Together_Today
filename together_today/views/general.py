from datetime import datetime
from flask import Blueprint, render_template, Response, jsonify, send_from_directory
from flask import current_app as app
from flask_login import login_required
from together_today.models import Photo_and_Message, Current_Photo, db
general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/", methods=["GET"])
def index():
        current_photo = Current_Photo.query.filter_by(id=1).first()
        photo_and_message = Photo_and_Message.query.filter_by(id=current_photo.counter).first()
        if current_photo.counter == 0:
                return render_template("general/index.html")
        else:
                return render_template("general/index.html", photo_and_message=photo_and_message)
                


@general_blueprint.route('/time_feed') 
@login_required
def time_feed():
        def generate():
                yield datetime.now().strftime("%H:%M:%S")
        return Response(generate(), mimetype='text') 


@general_blueprint.route('/check_for_photo') 
@login_required
def check_for_photo():
        current_time = datetime.now().strftime("%H:%M:%S")
        new_photo = False
        if current_time == "15:57:05":
                current_photo = Current_Photo.query.filter_by(id=1).first()
                photo_and_message = Photo_and_Message.query.filter_by(id=current_photo.counter).first()
                current_photo.current_photo = photo_and_message.photo_name
                current_photo.message = photo_and_message.message
                current_photo.counter +=1
                db.session.commit()
                new_photo = True

        if new_photo:
                return jsonify({"status": "Accepted"}), 202

        return jsonify({"status": "OK"}), 200


@general_blueprint.route("/index/uploads/<path:filename>")
@login_required
def index_photo(filename):
    return send_from_directory(app.config["PHOTOS_FOLDER"], filename)
