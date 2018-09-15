import datetime
import enum

from sqlalchemy.orm import validates

from pxa import db
from pxa.utils.validators import is_valid_url


class Website(db.Model):

    __tablename__ = 'website'

    class Status(enum.Enum):
        NEW = "NEW"
        PROCESSING = "PROCESSING"
        DONE = "DONE"
        ERROR = "ERROR"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(2083), index=True, nullable=False)
    status = db.Column(db.Enum(Status), index=True, nullable=False)
    status_desc = db.Column(db.String(255), nullable=True)
    created_dt = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           nullable=False)
    updated_dt = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow,
                           nullable=False)

    @validates('url')
    def validate_url(self, key, value):
        if not is_valid_url(value):
            raise ValueError("Url need be a valid url")

        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in [e for e in self.Status]:
            raise ValueError('Invalid Status')
        return value
