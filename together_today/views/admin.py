import uuid
import os
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from flask import current_app as app

from together_today.models import User, Profile, Photo_and_Message, db
from together_today.utils.decorators.admin import admin_required
from together_today.forms.photos_messages import AddForm, EditForm

admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.route("/admin", methods=["GET"])
@login_required
@admin_required
def index():
    users = User.query.all()
    profiles = Profile.query.all()
    photos_and_messages = Photo_and_Message.query.all()


    return render_template(
        "admin/index.html",
        user=current_user,
        users=users,
        profiles=profiles,
        photos_and_messages=photos_and_messages

    )


@admin_blueprint.route("/admin/<user_id>/toggle", methods=["GET", "POST"])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    user.is_admin = not user.is_admin
    db.session.commit()

    return jsonify({"status": "OK"}), 200


@admin_blueprint.route("/admin/add_photo_message", methods=["GET", "POST"])
@login_required
@admin_required
def add_photo_message():

    add_form = AddForm()

    if request.method == "POST":
        if add_form.validate_on_submit():
            photo = add_form.data["photo"]
            message = add_form.data["message"]
     
            if photo:
                extension = os.path.splitext(photo.filename)[1]
                photo_name = f"{uuid.uuid4()}{extension}"
                photo.save(os.path.join(app.config["PHOTOS_FOLDER"], photo_name))
            else:
                flash("Error with photo! Try again.", category="form_error")
                return render_template("admin/add.html", form=add_form)

            if not message:
                flash("Error with message! Try again.", category="form_error")
                return render_template("admin/add.html", form=add_form)

            photo_and_message = Photo_and_Message(
                photo_name=photo_name,
                message=message
            )

    

            db.session.add_all([photo_and_message])
            db.session.commit()

            flash("Successfully added your photo and message!", category="success")
            return redirect(url_for("admin.index"))

    # GET request or invalid POST request
    return render_template("admin/add.html", form=add_form)


    
@admin_blueprint.route("/admin/<photo_message_id>/edit_photo_message", methods=["GET", "POST"])
@login_required
def edit_photo_message(photo_message_id):
    photo_and_message = Photo_and_Message.query.filter_by(id=photo_message_id).first_or_404()

    
    edit_form = EditForm(
            message=photo_and_message.message
        )

    if request.method == "POST":
            if edit_form.validate_on_submit():
                photo = edit_form.data["photo"]
                message = edit_form.data["message"]

                if photo:
                    extension = os.path.splitext(photo.filename)[1]
                    photo_name = f"{uuid.uuid4()}{extension}"
                    photo.save(os.path.join(app.config["PHOTOS_FOLDER"], photo_name))
                    photo_and_message.photo_name = photo_name

                if message:
                    photo_and_message.message = message

                db.session.commit()

                return redirect(url_for("admin.index"))

        # GET request or invalid POST request
    return render_template("admin/edit.html", form=edit_form, photo_and_message=photo_and_message)


@admin_blueprint.route("/admin/<photo_message_id>/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_photo_message(photo_message_id):
    # delete_profile in reality deletes profile with the user and all the data
    photo_and_message = Photo_and_Message.query.filter_by(id=photo_message_id).first_or_404()
    db.session.delete(photo_and_message)
    db.session.commit()

    return jsonify({"status": "OK"}), 200
    
