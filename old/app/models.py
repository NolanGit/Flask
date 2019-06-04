from . import db
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return 'User %r' % self.username


class System(db.Model):
    __tablename__ = 'system'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return 'System IP %r' % self.sys_ip


class SysDate(db.Model):
    __tablename__ = 'sysdate'
    id = db.Column(db.Integer, primary_key=True)
    sys_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    is_valid = db.Column(db.Integer)
    is_ordered = db.Column(db.Integer)
    remark = db.Column(db.Text)
    update_time = db.Column(db.DateTime)
