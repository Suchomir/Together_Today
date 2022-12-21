import uuid
import os
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    send_from_directory,
    abort,
)
from flask import current_app as app
from flask_login import login_required, current_user

from together_today.forms.profile import EditForm
from together_today.utils.crypto import hash_password, verify_password
from together_today.utils.decorators.admin import admin_required

from together_today.models import db, Profile, User

profile_blueprint = Blueprint("profile", __name__)



@profile_blueprint.route("/profile/<username>", methods=["GET"])
@login_required
def single_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template(
        "profile/profile.html",
        user=user,
    )




@profile_blueprint.route("/profile/uploads/<path:filename>")
@login_required
def profile_picture(filename):
    return send_from_directory(app.config["UPLOADS_FOLDER"], filename)


@profile_blueprint.route("/profile/<profile_id>/edit", methods=["GET", "POST"])
@login_required
def edit(profile_id):
    profile = Profile.query.filter_by(id=profile_id).first_or_404()

    if current_user == profile.user or current_user.is_admin:
        edit_form = EditForm(
            first_name=profile.first_name,
            last_name=profile.last_name,
            username=profile.user.username,
        )

        if request.method == "POST":
            if edit_form.validate_on_submit():
                username = edit_form.data["username"]
                first_name = edit_form.data["first_name"]
                last_name = edit_form.data["last_name"]
                picture = edit_form.data["picture"]
                new_password = edit_form.data["new_password"]

                if username:
                    username_taken = User.query.filter_by(username=username).first()
                    if username_taken:
                        if username_taken.username != profile.user.username:
                            flash(
                                "User with this username already exists",
                                category="form_error",
                            )
                            return render_template(
                                "profile/edit.html", form=edit_form, profile=profile
                            )
                    else:
                        profile.user.username = username

                if last_name:
                    profile.last_name = last_name

                if first_name:
                    profile.first_name = first_name

                if new_password:
                    if verify_password(new_password, profile.user.password):
                        flash(
                            "New password can not be the same as current password",
                            category="form_error",
                        )
                        return render_template(
                            "profile/edit.html", form=edit_form, profile=profile
                        )

                    profile.user.password = hash_password(new_password)

                if picture:
                    extension = os.path.splitext(picture.filename)[1]
                    picture_name = f"{uuid.uuid4()}{extension}"
                    picture.save(
                        os.path.join(app.config["UPLOADS_FOLDER"], picture_name)
                    )
                    profile.picture = picture_name

                db.session.commit()

                return redirect(
                    url_for("profile.single_profile", username=profile.user.username)
                )

        # GET request or invalid POST request
        return render_template("profile/edit.html", form=edit_form, profile=profile)

    return abort(403)


@profile_blueprint.route("/profile/<profile_id>/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_profile(profile_id):
    # delete_profile in reality deletes profile with the user and all the data
    profile = Profile.query.filter_by(id=profile_id).first_or_404()
    db.session.delete(profile.user)
    db.session.commit()

    return jsonify({"status": "OK"}), 200


@profile_blueprint.route("/picture/<profile_id>/delete", methods=["DELETE"])
@login_required
def delete_profile_picture(profile_id):
    profile = Profile.query.filter_by(id=profile_id).first_or_404()

    if current_user == profile.user:
        profile.picture = "default.png"
        db.session.commit()
        return jsonify({"status": "OK"}), 200

    return jsonify({"status": "OK"}), 200