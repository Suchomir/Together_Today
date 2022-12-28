from datetime import datetime
from flask import Blueprint, render_template, Response
from flask_login import login_required
from together_today.models import Image_Counter, Photo_and_Message, db
general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/", methods=["GET"])
def index():
        return render_template("general/index.html")


@general_blueprint.route('/time_feed') 
@login_required
def time_feed():
        def generate():
                yield datetime.now().strftime("%H:%M:%S")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        photo_and_message = False
        if current_time == "19:09:54":
                counter = Image_Counter.query.filter_by(id=1).first_or_404()
                photo_and_message = Photo_and_Message.query.filter_by(id=counter.counter)
                print(counter.counter)
                counter.counter +=1
                db.session.commit()

        if photo_and_message:
                return Response(generate(), mimetype='text') 

        return Response(generate(), mimetype='text') 