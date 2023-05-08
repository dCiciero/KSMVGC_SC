from datetime import datetime
from main import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# lead@devpro.org/goo123. patrick.soyombo@gmail.com/soyombop

class Access(UserMixin, db.Model):
    __tablename__="access"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}, Email {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return Access.query.get(int(id))


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50))
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))
    other_names=db.Column(db.String(75))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    phone1 = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    occupation = db.Column(db.String(150))
    work_place = db.Column(db.String(150))
    work_address = db.Column(db.String(200))

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    other_names=db.Column(db.String(75))
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    birth_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    initiation_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    investiture_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    place_initiated = db.Column(db.String(150))
    initiated_sc = db.Column(db.String(150))
    current_sc = db.Column(db.String(150))
    degree = db.Column(db.String(10))
    ksmno = db.Column(db.String(10))
    status = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
    state_of_origin = db.Column(db.String(20))
    home_town = db.Column(db.String(120))
    occupation = db.Column(db.String(150))
    work_title = db.Column(db.String(100))
    work_place = db.Column(db.String(150))
    work_address = db.Column(db.String(200))
    # access_id = db.Column(db.Integer, db.ForeignKey('access.id'), nullable=False)


class DisplayPix(db.Model):
    __tablename__ = "displaypix"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class PhotoGallery(db.Model):
    __tablename__ = "photo_gallery"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.String(120), nullable=True)
    path = db.Column(db.String(200), nullable=False)
    display_type = db.Column(db.Integer, db.ForeignKey('displaypix.id'), nullable=False)
    gallery_options = db.Column(db.Integer, db.ForeignKey('gallery_options.id'))


class GalleryOptions(db.Model): # This table defines the gallery, if it's Home page or the photo gallery section
    __tablename__ = "gallery_options"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # PhotoGallery = db.Column(db.Integer, db.ForeignKey('photo_gallery.id'), nullable=False)

class Offices(db.Model):
    __tablename__  = "offices"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(120))
    alias = db.Column(db.String(20))
    arm = db.Column(db.String(20))

class Executive(db.Model):
    __tablename__ = "executives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    post = db.Column(db.String(50), nullable=False)
    elected_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    where = db.Column(db.String(5), nullable=False)
    alias = db.Column(db.String(10), nullable=False, default="")
    display_order = db.Column(db.Integer)


class PastExecutive(db.Model):
    __tablename__ = "pastexecutives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    post = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    end_date = db.Column(db.Date, index=True, default=datetime.utcnow)
    where = db.Column(db.String(5))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Date, index=True, default=datetime.utcnow)
    posted_by = db.Column(db.Integer, db.ForeignKey('access.id'), nullable=False)

class GlobalSetup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about_ksmvgcscs = db.Column(db.String, nullable=False)

