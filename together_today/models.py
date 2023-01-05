from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()




class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    profile = db.relationship(
        "Profile", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    registered_at = db.Column(db.DateTime(timezone=False), server_default=func.now())
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    picture = db.Column(db.String(), nullable=True)


    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)

    def __repr__(self):
        return f"<Profile {self.last_name}>"

class Photo_and_Message(db.Model):
    __tablename__ = "photos_and_messages"

    id = db.Column(db.Integer, primary_key=True)

    photo_name = db.Column(db.String(128), nullable=True)
    message = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f"<Photo {self.id}>"



class Current_Photo(db.Model):
    __tablename__ = "current_photos"

    id = db.Column(db.Integer, primary_key=True)

    counter = db.Column(db.Integer, nullable=True)
    current_date = db.Column(db.String(128), nullable=True)
    current_photo = db.Column(db.String(128), nullable=True)
    current_message = db.Column(db.String(256), nullable=True)


    def __repr__(self):
        return f"<Current photo ID {self.current_date}>"


class Register_Code(db.Model):
    __tablename__ = "register_codes"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(8), nullable=True)


    def __repr__(self):
        return f"<Code {self.code}>"



