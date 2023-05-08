#******************* IMPORTS *************************
import os
from datetime import datetime
from flask import Flask, abort, flash, redirect, \
    render_template, request, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, BooleanField, SelectField, SubmitField, DateField, PasswordField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
# from forms import *
# from models import *
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from config import Config

#************************** SETUP ******************************

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'cache')
# app.config['SESSION_FILE_THRESHOLD'] = 1000
print(f"Get DB params in main: {os.getenv('MYSQL_DATABASE_URL')}")
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)


# ***************** Configurations *********************
# basedir = os.path.abspath(os.path.dirname(__file__))
# upload_folder = os.path.join(basedir, 'vgcsc/static/images/uploads')


# class Config(object):
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vgcsc_sqlite.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOAD_FOLDER = upload_folder
#     ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     APP_SETTINGS = os.environ.get('APP_SETTINGS')
#     FLASKS3_BUCKET_NAME = 'awsogcicerobucket'


# class ProductionConfig(Config):
#     'Production specific config'
#     DEBUG = False


# class StagingConfig(Config):
#     'Staging specific config'
#     DEBUG = True


# class DevelopmentConfig(Config):
#     DEBUG = False
#     TESTING = True
#     SECRET_KEY = 'The Quick Brown Fox Jumps Over The Lazy Dog'

@app.context_processor
def getCurrentYear():
    year = datetime.now().year
    return dict(year=year)

#*********************** MODELS ********************
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


class GalleryOptions(db.Model):
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

#***************** END MODELS *****************************************************

#******************* FORMS *******************************************************
class ExecutiveSetupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    post = SelectField("Select Post", validators=[DataRequired()], choices=[])
    date_elect = DateField("Elected Date", validators=[DataRequired], format='%d/%m/%Y')
    alias = SelectField("Alias", validators=[DataRequired()], choices=[])
    arm = SelectField("Where", validators=[DataRequired()], choices=[('KSM', 'KSM'), ('LSM','LSM'), ('Zone1', 'Zone1'),('Zone2', 'Zone2')]) #
    submit = SubmitField("Save Entry")

class OfficeSetupForm(FlaskForm):
    post = StringField("Name", validators=[DataRequired()])
    alias = StringField("Alias", validators=[DataRequired()])
    arm = SelectField("Where", validators=[DataRequired()], choices=[('KSM', 'KSM'), ('LSM','LSM'), ('Zone1', 'Zone1'),('Zone2', 'Zone2')]) #
    submit = SubmitField("Save Entry")

class NewsForm(FlaskForm):
    topic = StringField("Topic", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post News")
    # date_created = DateTimeField("Date/Time", format='%D/%m/%Y %H:%M:%S')
    # posted_by

class MemberForm(FlaskForm):
    ksmno  = StringField('KSM Number')
    firstname = StringField('First Name', validators=[DataRequired(message="First Name is required")])
    lastname = StringField('Last Name', validators=[DataRequired(message="Larst Name is required")])
    midname = StringField('Other Name', validators=[DataRequired(message="Othername is required")])
    address = TextAreaField('Address', validators=[DataRequired(message="Address is required")])
    gender = SelectField('Gender', validators=[DataRequired(message="Gender is required")], choices=[('M', 'Male'),('F','Female')])
    dob = DateField('Date of Birth', validators=[DataRequired(message="Date of Birth is required")], format='%d/%m/%Y')
    phone1 = StringField('Phone', validators=[DataRequired(message="Phone is required")])
    phone2 = StringField('Other Phone')
    email = StringField('Email', validators=[DataRequired(message="Email is required")])
    state_of_origin = StringField('State of Origin', validators=[DataRequired()])
    home_town = StringField('Home Town', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    # state_of_origin = SelectField('State of Origin', validators=[DataRequired(message="State of Origin is required")], choices=[])
    nationality = StringField('Nationality', validators=[DataRequired(message="Nationality is required")])
    degree_in_order  = StringField('Degree', validators=[DataRequired(message="Degree is required")])
    date_initiated = DateField('Date Initiated', validators=[DataRequired(message="Date Initiated is required")], format='%d/%m/%Y')
    lastInvested = DateField('Date of Investiture', validators=[DataRequired(message="Date Initiated is required")], format='%d/%m/%Y')
    place_initiated = StringField('Initiated At', validators=[DataRequired(message="Initiated Venue is required")])
    initiated_sc  = StringField('Initiated Sub-Council', validators=[DataRequired(message="Initiated Sub-Council is required")])
    # initiated_sc  = SelectField('Initiated Sub-Council', validators=[DataRequired()], choices=[], coerce=int)
    current_sc = StringField('Current Sub-Council', validators=[DataRequired()])
    # current_sc = SelectField('Current Sub-Council', validators=[DataRequired()], choices=[], coerce=int)
    membership_status = StringField('Status', validators=[DataRequired(message="Status is required")])
    submit = SubmitField('Submit')

#*********************** END FORMS ***********************************************


# ******************* ROUTES ********************
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# bp = Blueprint('routes', __name__)
def save_record(data):
    db.session.add(data)
    db.session.commit()
    return 1


def getGalleryOptions():
    gallery_options = GalleryOptions.query.all()
    return gallery_options


@app.route('/', methods=("GET", "POST"))
@app.route('/index', methods=("GET", "POST"))
def index():
    news_feed = News.query.order_by(News.date_created.desc()).limit(3)
    carousel = PhotoGallery.query.filter_by(display_type=1)
    # about = GlobalSetup.query.all()
    history = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\
                Suspendisse sed sem ut diam accumsan maximus sit amet eget risus.\
                Nulla maximus mollis venenatis. Maecenas sem leo, placerat id nisl placerat, pellentesque semper ante.\
                Pellentesque tincidunt finibus congue. Proin at odio vitae tortor consectetur fringilla id nec lacus.\
                Nunc pulvinar magna euismod lorem bibendum gravida. Ut pellentesque cursus nulla at varius.\
                Etiam fermentum enim egestas mi venenatis imperdiet. Nunc sed mi ac tortor condimentum porttitor in ut dolor.\
                Duis neque magna, tincidunt a elit nec, iaculis rhoncus nisi. Duis ac purus non diam lobortis rhoncus in eu urna.\
                Nulla sollicitudin metus non dapibus mollis. Etiam interdum ut augue sit amet tincidunt.\
                Vivamus ex metus, convallis vestibulum odio in, pharetra mattis ligula.\
                Proin mollis, est a consequat molestie, elit purus interdum est, sed luctus mauris lectus a tellus.\
                Morbi semper justo id mauris pretium elementum. Nunc venenatis convallis blandit.\
                Maecenas suscipit tortor eros, eget fringilla erat rutrum nec. Fusce viverra pretium eros,\
                ac vulputate ex convallis placerat. Donec non velit volutpat, pulvinar justo vel, ullamcorper orci.\
                Praesent malesuada dictum tellus, id imperdiet neque pulvinar non.\
                Fusce auctor, sapien vel pharetra iaculis, justo dui auctor felis,\
                nec pharetra tellus sapien at turpis. Nam sem mi, luctus sit amet ipsum vel, malesuada eleifend metus.\
                Cras vel tincidunt elit. Maecenas convallis faucibus nulla sed convallis. Cras vel est libero.\
                In laoreet mi posuere, rutrum lacus vitae, laoreet ante. Sed gravida lorem eu tellus laoreet volutpat.\
                Cras sed lorem sed enim bibendum iaculis a vel augue. Nullam finibus turpis justo,\
                eget euismod leo efficitur dictum. Curabitur egestas, mauris sed interdum scelerisque,\
                tortor odio convallis risus, sit amet ornare massa est eget lectus.\
                Phasellus convallis quam quis ligula efficitur euismod. Duis venenatis sed sapien ut blandit.\
                Nam sed felis ultrices, venenatis lorem ut, sollicitudin tortor. Curabitur pretium tristique lobortis."
    return render_template('vgcsc/index.html', news_feed=news_feed,
                          gallery_options=getGalleryOptions(), carousel=carousel, history=history)


@app.route('/login', methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('membership'))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = Access.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not is_safe_url(next_page):
            return abort(400)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        print(user)
        return redirect(next_page)

    return render_template('vgcsc/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/membership', methods=["GET", "POST"])
@login_required
def membership():
    if current_user.is_authenticated:
        if request.method == "POST":
            flash("Record saved")
        else:
            # print(f'Admin: {current_user.is_admin}')
            user_email = current_user.email
            if user_email == 'lead@devpro.org' and current_user.is_admin is True:
                memba = None
            else:
                # print(current_user.email)
                memberlisting = Member.query.all()
                for member in memberlisting:
                    member.email = member.email.strip().lower()
                    if member.email == user_email:
                        memba = member
                # print(f'Current user is {current_user.id}')
                # print(f'member is {member}')
            return render_template("vgcsc/members.html", member=memba)

    else:
        flash("You have to login in to access this page")
        return redirect(url_for('login'))


@app.route("/executives/<string:option>")
def exco(option):
    # print(f"{option}")
    # return f"{option}"
    excos = Executive.query.filter_by(where=f"{option}")
    return render_template('vgcsc/executives1.html', excos=excos, gallery_options=getGalleryOptions())


def allowed_file(filename):
    return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
# @login_required@app.route('/upload', methods=['GET', 'POST'])
def uploads():
    try:
        if request.method == 'POST':
            if 'form_photo_upload' in request.form:
                print(request.files)
                # check if the post request has the file part
                if 'file' not in request.files:
                    # if 'file' not in request.form.get('file'):
                    flash('No file (photo) selected', 'danger')
                    return redirect(request.url)
                upload_type = request.form.get('rdbtn_uploadtype')
                flash(str(upload_type), 'info')
                # return redirect(request.url)
                imglist = request.files.getlist('file')  # ['file']
                fototype = request.form.get('photoType')  # request.form['photoType']
                caption = request.form.get('filecaption')  # request.form['filecaption']
                galleryType = request.form.get('galleryOptions')  # request.form['galleryOptions']
                if galleryType == 0 or galleryType == '0':
                    if fototype == "2":
                        flash('Select an option', 'warning')
                        return redirect(request.url)
                    galleryType = None
                print(f" Photo Type: {fototype}")
                print(galleryType)
                print(f"caption {caption}")
                # return redirect(url_for('uploads'))
                # if user does not select file, browser also
                # submit an empty part without filename
                for img in imglist:
                    # filename.rsplit('.', 1)[1].lower()
                    # if len(img.filename.rsplit('.', 1)[1].lower()) <= 5:
                    #     flash('Image name is too short, rename and try again', "warning")
                    #     return redirect(request.url)
                    if img.filename == '':
                        flash('No selected file', "danger")
                        return redirect(request.url)
                    if img and allowed_file(img.filename):
                        filename = secure_filename(img.filename)
                        print(filename)
                        if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'])):
                            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER']))
                        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        if os.path.exists(path):
                            flash("File has been uploaded previously", "warning")
                            return redirect(url_for('uploads'))
                        img.save(path)
                        photo = PhotoGallery(name=filename, caption=caption, path=path, display_type=fototype,
                                             gallery_options=galleryType)
                        db.session.add(photo)
                        db.session.commit()
                        flash("Upload successful", "success")
                        return redirect(url_for('uploads'))

            if 'form_doc_upload' in request.form:
                flash('Document upload section', 'info')
                return redirect(request.url)
        photoType = DisplayPix.query.all()
        galleryOptions = GalleryOptions.query.all()
        # print(request.form['galleryOptions'])

        return render_template('vgcsc/uploads.html', photoType=photoType, galleryOptions=galleryOptions)
    except Exception as er:
        flash(er, 'error')
        return redirect(url_for('uploads'))

@app.route('/uploader', methods=["GET", "POST"])
def upload_screen():
    try:
        if request.method == 'POST':
            print(request.get_json())
            print(request.get_json()['txtChess'])

            return jsonify({'OK': 200})
    except Exception as ex:
        pass

@app.route('/uploadAjax', methods=['GET', 'POST'])
def uploads_ajax():
    if request.method == 'POST':

        fototype = request.form.get('fototype')  # request.form['photoType']
        caption = request.form.get('caption')  # request.form['filecaption']
        galleryType = request.form.get('galleryType')  # request.form['galleryOptions']
        if galleryType == 0 or galleryType == '0':
            if fototype == "2":
                flash('Select an option', 'warning')
                return jsonify({"success": False, "message": "Select an option"})
            galleryType = None
        myupload = request.form.get('file')
        print(type(myupload))
        print(len(myupload))
        print(myupload)

        # if user does not select file, browser also
        # submit an empty part without filename
        # check if the post request has the file part
        if 'file' not in request.files:
            # if 'file' not in request.form.get('file'):
            flash('No file (photo) selected', 'danger')
            return jsonify(code=1002,
                          result="File name can't be empty")  # {"success": False, "message": "No file (photo) selected "}
        imglist = request.files.getlist('file')  # ['file']
        for img in imglist:
            # filename.rsplit('.', 1)[1].lower()
            # if len(img.filename.rsplit('.', 1)[1].lower()) <= 5:
            #     flash('Image name is too short, rename and try again', "warning")
            #     return redirect(request.url)
            if img.filename == '':
                flash('No selected file', "danger")
                return jsonify({"success": False, "message": "No selected file"})
            if img and allowed_file(img.filename):
                filename = secure_filename(img.filename)
                print(filename)
                if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'])):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER']))
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(path):
                    flash("File has been uploaded previously", "warning")
                    return jsonify({"success": False, "message": "File has been uploaded previously"})
                img.save(path)
                photo = PhotoGallery(name=filename, caption=caption, path=path, display_type=fototype,
                                     gallery_options=galleryType)
                db.session.add(photo)
                db.session.commit()
                flash("Upload successful", "success")
                return jsonify({"success": True, "message": "Upload successful"})
    photoType = DisplayPix.query.all()
    galleryOptions = GalleryOptions.query.all()
    # print(request.form['galleryOptions'])

    return render_template('vgcsc/uploads.html', photoType=photoType, galleryOptions=galleryOptions)


@app.route('/gallery/<int:id>')
def gallery(id):
    print(id)
    pixOptions = PhotoGallery.query.filter_by(gallery_options=id)
    gallery_options = getGalleryOptions()
    name = gallery_options[id - 1].name  # [name for name in gallery_options if name == gallery_options.name ]
    return render_template('vgcsc/gallery.html', photos=pixOptions, gallery_options=getGalleryOptions(), name=name)


@app.route('/zones')
def zones():
    return render_template('vgcsc/zones.html', gallery_options=getGalleryOptions())


@app.route('/personal')
def personal():
    return render_template('vgcsc/members.html')


@app.route('/directory')
@login_required
def directory():
    if current_user.is_authenticated:
        if request.method == "GET":
            members = Member.query.order_by(Member.id).all()
            # print(f'Current user is {current_user.id}')
            # print(f'member is {members}')
            return render_template('vgcsc/directory.html', members=members)

    else:
        flash("You have to login in to access this page")
        return redirect(url_for('login'))


@app.route('/directoryedit/<int:opt>', methods=["POST", "GET"])
@login_required
def editDirectory(opt):
    print(opt)
    # mc = getMetro()
    form = MemberForm()
    # form.initiated_sc.choices = [(sc.id, sc.descr.upper()) for sc in mc[6].subcouncils]
    # form.current_sc.choices = [(sc.id, sc.descr.upper()) for sc in mc[6].subcouncils]
    if current_user.is_authenticated:
        member_details = Member.query.get(opt)
        # member_details = Member.query.get_or_404(opt)
        if request.method == "POST":
            name = form.firstname.data
            member_details.first_name = form.firstname.data  # request.form.get('txt_fname')
            member_details.last_name = form.lastname.data  # request.form.get('txt_lname')
            member_details.other_names = form.midname.data  # request.form.get('txt_oname')
            member_details.ksmno = form.ksmno.data  # request.form.get('txt_ksmno')
            member_details.phone = form.phone1.data  # request.form.get('txt_phone1')
            member_details.phone2 = form.phone2.data  # request.form.get('txt_phone2')
            member_details.birth_date = form.dob.data
            member_details.email = form.email.data  # request.form.get('txt_email')
            member_details.nationality = form.nationality.data  # request.form.get('txt_country')
            member_details.state_of_origin = form.state_of_origin.data  # request.form.get('cmb_state')
            member_details.home_town = form.home_town.data  # request.form.get('cmb_state')
            member_details.occupation = form.occupation.data  # request.form.get('cmb_state')
            member_details.address = form.address.data  # request.form.get('address')
            member_details.degree = form.degree_in_order.data  # request.form.get('txt_degree')
            member_details.initiated_sc = form.initiated_sc.data  # request.form.get('txt_initiated_sc')
            member_details.initiation_date = form.date_initiated.data
            member_details.place_initiated = form.place_initiated.data
            member_details.investiture_date = form.lastInvested.data
            member_details.current_sc = form.current_sc.data  # request.form.get('txt_initiated_sc')
            member_details.status = form.membership_status.data  # request.form.get('txt_initiated_sc')
            db.session.commit()
            flash(f'Update successful.....{name}', 'success')

        return render_template('vgcsc/editdirectory.html', details=member_details, form=form)

@app.route('/memberdetails/<int:opt>', methods=["POST", "GET"])
@login_required
def memberdetails(opt):
    print(opt)
    # mc = getMetro()
    form = MemberForm()
    # form.initiated_sc.choices = [(sc.id, sc.descr.upper()) for sc in mc[6].subcouncils]
    # form.current_sc.choices = [(sc.id, sc.descr.upper()) for sc in mc[6].subcouncils]
    if current_user.is_authenticated:
        member_details = Member.query.get(opt)
        # member_details = Member.query.get_or_404(opt)


        return render_template('vgcsc/member_details.html', details=member_details, form=form)


@app.route('/setups/<string:option>', methods=["GET", "POST"])
def setups(option):
    office = Offices.query.all()
    success = 0
    excos = None
    news = None
    galleries = None
    form = ExecutiveSetupForm()
    form_office = OfficeSetupForm()
    news_form = NewsForm()
    form.post.choices = [(p.post, p.post) for p in office]
    form.alias.choices = [(p.alias, p.alias) for p in office]
    if request.method == "POST":
        if option.lower() == 'gallery':
            entry = request.form.get('descr')
            print(f"{entry} {option} dd")
            if entry == "":
                flash("Enter the name of the event", "warning")
                return redirect(url_for('setups', option=option))
            event_name = GalleryOptions(name=entry)
            success = save_record(event_name)
            # flash("Record saved successfully", "success")
            # return redirect(url_for('setups', option=option))
        elif option.lower() == 'sub_exco' or option.lower() == 'zonal_exco':
            officer = Executive(name=form.name.data, post=form.post.data, elected_date=form.date_elect.data,
                                where=form.arm.data, alias=form.alias.data)
            success = save_record(officer)
            # flash(f"Name: {form.name.data} Post: {form.post.data}", "success")
            # flash(f"Record saved successfully", "success")
            # if form.validate_on_submit():
            #     name = form.name.data
        elif option.lower() == 'office':
            post = Offices(post=form_office.post.data, alias=form_office.alias.data, arm=form_office.arm.data)
            success = save_record(post)
            # flash(f"Record saved successfully", "success")
        elif option.lower() == 'news':
            # flash(f"Current user: {current_user.id}", "success")
            news = News(topic=news_form.topic.data, content=news_form.content.data, posted_by=current_user.id)
            success = save_record(news)

        if success == 1:
            flash(f"Record saved successfully", "success")
            return redirect(url_for('setups', option=option))
    # descriptions = ["Gallery","Sub Council Executive", "Zonal Executive","Offices"]
    descriptions_dict = {"Gallery": "generic", "Sub Council Executive": form,
                         "Zonal Executive": form, "Office": form_office, "News": news_form}
    for descr, formName in descriptions_dict.items():
        if option[:3].lower() in descr.lower():
            option = descr
            form = formName
            break
    if option.lower() == "Sub Council Executive".lower():
        excos = Executive.query.filter(Executive.where.in_(['KSM', 'LSM'])).all()
    elif option.lower() == "zonal executive":
        excos = Executive.query.filter(Executive.where.like('%Zone%')).all()
    elif option.lower() == "news":
        news = News.query.all()  # News.query.order_by(News.id.desc()).limit(5).all()
    elif option.lower() == "gallery":
        galleries = GalleryOptions.query.all()
    # else:
    #     excos = None
    return render_template('vgcsc/setup.html', setup=option, form=form, office=office,
                          excos=excos, news=news, galleries=galleries)



@app.route('/contactus', methods=["GET", "POST"])
def contactus():
    return render_template('vgcsc/contact.html')

