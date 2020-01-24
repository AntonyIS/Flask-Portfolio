from app import *
db = SQLAlchemy(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    about = db.Column(db.String(50),nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    project = db.relationship('Project', backref='user', lazy=True)

    def __repr__(self):
        return  "User :{}".format(self.name)

    def __str__(self):
        return self.name


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='project.jpg')
    user_id = db.Column(db.ForeignKey(User.id))
    # backend_language

    def __repr__(self):
        return  "User :{}".format(self.name)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    frameworks = db.Column(db.String(50), nullable=False)
    project = db.Column(db.String(150), nullable=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id =db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
