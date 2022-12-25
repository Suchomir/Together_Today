import uuid
import os
from flask import current_app as app
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user

from together_today.forms.auth import RegisterForm, LoginForm
from together_today.models import User, Profile, Register_Code ,db
from together_today.utils.crypto import hash_password, verify_password

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if request.method == "POST":
        if login_form.validate_on_submit():
            username = login_form.data["username"]
            password = login_form.data["password"]

            user = User.query.filter_by(username=username).first()

            if not user:
                flash("Invalid username and/or password", category="form_error")
                return render_template("auth/login.html", form=login_form)

            if verify_password(password, user.password):
                flash("Successfully logged-in!", category="success")
                login_user(user)

                nxt = login_form.data.get("next", None)
                if nxt and nxt.startswith("/"):
                    return redirect(nxt)


                return redirect(
                    url_for(
                        "profile.single_profile",
                        username=username
                    )
                )

            flash("Invalid username and/or password", category="form_error")
            return render_template("auth/login.html", form=login_form)

    nxt = request.args.get("next", None)
    if nxt and nxt.startswith("/"):
        login_form.next.data = nxt

    return render_template("auth/login.html", form=login_form)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if request.method == "POST":
        if register_form.validate_on_submit():
            username = register_form.data["username"]
            first_name = register_form.data["first_name"]
            last_name = register_form.data["last_name"]
            picture = register_form.data["picture"]
            register_code = register_form.data["register_code"]
            password = hash_password(register_form.data["password"])

            username_taken = User.query.filter_by(username=username).first()

            is_valid_code = False

            if username_taken:
                flash("User with this username already exists!", category="form_error")
                return render_template("auth/register.html", form=register_form)

            register_codes = Register_Code.query.all()

            for valid_register_code in register_codes:
                if register_code == valid_register_code.code:
                    is_valid_code = True
                    db.session.delete(valid_register_code)
                    db.session.commit()
                    break

            if not is_valid_code:
                flash("Wrong registration code!", category="form_error")
                return render_template("auth/register.html", form=register_form)


            if picture:
                extension = os.path.splitext(picture.filename)[1]
                picture_name = f"{uuid.uuid4()}{extension}"
                picture.save(os.path.join(app.config["UPLOADS_FOLDER"], picture_name))
            else:
                picture_name = "default.png"

            user = User(
                username=username,
                password=password,
            )

            profile = Profile(
                first_name=first_name,
                last_name=last_name,
                user=user,
                picture=picture_name,
            )

            db.session.add_all([user, profile])
            db.session.commit()

            flash("Successfully registered, you can now log in!", category="success")
            return redirect(url_for("auth.login"))

    # GET request or invalid POST request
    return render_template("auth/register.html", form=register_form)


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out!", category="success")
    return redirect(url_for("general.index"))
