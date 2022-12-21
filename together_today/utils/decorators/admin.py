from functools import wraps

from flask import current_app, redirect, url_for, flash
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        if not current_user.is_admin:
            flash("You're not authorized to access that page", category="error")
            return redirect(
                url_for("profile.single_profile", username=current_user.username)
            )

        return func(*args, **kwargs)

    return decorated_view
