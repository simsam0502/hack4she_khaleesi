from flask import Flask, request, url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from sqlalchemy.orm.attributes import flag_modified
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc'}

app = Flask(__name__)
app.secret_key="12345678"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'#DBURI
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db=SQLAlchemy(app)
class courses(db.Model):
    ID=db.Column('ID',db.Integer,primary_key=True, autoincrement=True)
    headline=db.Column('headline',db.Text)
    loc1=db.Column('loc1',db.Text)
    loc2=db.Column('loc2',db.Text)
    cardtext=db.Column('cardtext',db.Text)
    link=db.Column('link',db.Text)
    field=db.Column('field',db.Text)
    def _init_(self,ID,headline,loc1,loc2,link,cardtext,field):
        self.ID=ID
        self.headline=headline
        self.loc1=loc1
        self.loc2=loc2
        self.link=link
        self.cardtext=cardtext
        self.field=field
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
username="admin"
password="kuchbhi@1234"
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/home')
def homee():
    return render_template('index.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/educourses')
def educourses():
    course = courses.query.filter_by(field="educourses")
    print(course)
    return render_template('educourses.html', courses=course)

@app.route('/edujobs')
def edujobs():
    course = courses.query.filter_by(field="edujobs")
    return render_template('edujobs.html', courses=course)


@app.route('/skillcourses')
def skillcourses():
    course = courses.query.filter_by(field="skillcourses")
    return render_template('skillcourses.html', courses=course)

@app.route('/skilljobs')
def skilljobs():
    course = courses.query.filter_by(field="skilljobs")
    return render_template('skilljobs.html', courses=course)


@app.route('/addcourse',methods=['POST'])
def addcourse():
    if request.method == 'POST':
        if 'img1' not in request.files:
            return render_template('index.html')
        if 'img2' not in request.files:
            return render_template('index.html')
            
        img1 = request.files['img1']
            
        if img1.filename == '':
            return render_template('index.html')
            
        if img1 and allowed_file(img1.filename) :
            filename = secure_filename(img1.filename)
            img1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loc1=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        img2 = request.files['img2']
            
        if img2.filename == '':
            return render_template('index.html')
            
        if img2 and allowed_file(img2.filename) :
            filename = secure_filename(img2.filename)
            img2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loc2=os.path.join(app.config['UPLOAD_FOLDER'], filename)


        headline=request.form.get("headline")
        cardtext=request.form.get("cardtext")
        link=request.form.get("link")        
        field=request.form.get("field")
        course=courses(headline=headline,loc1=loc1,loc2=loc2,link=link,cardtext=cardtext,field=field)
        db.session.add(course)
        db.session.commit()
        #print(intro)
    return render_template('index.html',message="Sucessfully added")

if __name__ == "__main__":
    app.run(debug=True)