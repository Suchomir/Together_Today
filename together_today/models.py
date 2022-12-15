from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()




class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    profile = db.relationship(
        "Profile", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    posts = db.relationship(
        "Post", backref="author", uselist=True, cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="author", uselist=True, cascade="all, delete-orphan"
    )

    registered_at = db.Column(db.DateTime(timezone=False), server_default=func.now())
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"


