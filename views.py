from app import *
from models import User, Project,Comment,db
import config
from werkzeug.utils import secure_filename
import os
from services import comment_count


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route('/')
# @cache.cached(timeout=50)
def index():
    projects = Project.query.all()
    if len(projects) >= 4:
        return render_template('index.html', title="Antony Injila | Home", projects=projects[:4])

    return render_template('index.html', title="Antony Injila | Home", projects=projects)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    projects = Project.query.all()
    if request.form and request.files:
        name = request.form.get('name')
        email = request.form.get('email')
        about = request.form.get('about')

        f = request.files['image-file']
        filename = secure_filename(f.filename)
        # location for storing images: Portfolio/static/images/name_of_image
        image_file = "{}/{}/{}".format("static", "images/uploads", filename)
        # image upload
        f.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/uploads", filename))

        user = User(name=name,email=email,about=about,image_file=image_file)
        db.session.add(user)
        db.session.commit()
        user = User.query.get(1)
        return render_template('dashboard.html',title="Antony Injila | Dashboard",user=user )
    user = User.query.get(1)
    count = len(projects)

    return render_template('dashboard.html', title="Antony Injila | Dashboard", user=user,count=count, projects=projects)


@app.route('/dashboard/update', methods=['GET','POST'])
def dashboard_update():
    projects = Project.query.all()
    user = User.query.get(1)
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        about = request.form.get('about')
        technical_experience = request.form.get('technical_experience')
        current_job = request.form.get('current_job')
        educational_background = request.form.get('educational_background')
        profession = request.form.get('profession')
        python = request.form.get('python')
        javascript = request.form.get('javascript')
        java = request.form.get('java')
        django = request.form.get('django')
        flask = request.form.get('flask')
        nodejs = request.form.get('nodejs')
        android = request.form.get('android')

        image_file_old = request.form.get('image-file-old')
        f = request.files['image-file']
        filename = secure_filename(f.filename)

        print()
        if filename:
            # location for storing images: Portfolio/static/images/name_of_image
            image_file = "{}/{}/{}".format("static", "images/uploads", filename)

            # image upload
            f.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/uploads", filename))
            user.image_file = image_file
            db.session.commit()
        else:
            user.name = name
            user.email = email
            user.about = about
            user.technical_experience = technical_experience
            user.current_job = current_job
            user.educational_background = educational_background
            user.profession = profession
            user.python = python
            user.javascript = javascript
            user.java = java
            user.django = django
            user.flask = flask
            user.nodejs = nodejs
            user.android = android
            user.image_file = image_file_old

        # save the new changes
            db.session.commit()
        # return redirect('/project/update/{}/'.format(project_id))
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', title="Antony Injila | Dashboard update", user=user, projects=projects)


@app.route('/about')
def about():
    user = User.query.get(1)
    return render_template('about.html', title='Antony Injila | About page', user=user)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == config.EMAIL and password == config.PASSWORD:
            user = User.query.get(1)
            login_user(user)
            flash(u'login successfully', 'alert alert-success')
            return redirect(url_for('index'))
        else:
            flash(u'login unsuccessfully', 'alert alert-danger')
            return render_template('login.html')

    return render_template('login.html', title = "login | Antony")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logout successful', 'alert alert-success')
    return redirect('/')


@app.route('/project/post',methods=['GET','POST'])
def project():
    if request.method == 'POST' and request.files:
        name = request.form.get('name')
        description = request.form.get('description')
        f = request.files['image-file']

        filename = secure_filename(f.filename)

        # location for storing images: Portfolio/static/images/name_of_image
        image_file = "{}/{}/{}".format("static", "images/uploads", filename)

        # image upload

        f.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/uploads", filename))

        project = Project(name=name,description=description,image_file=image_file)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_project.html', title="Antony Injila | Upload Project")


@app.route('/project/detail/<int:project_id>')
def project_detail(project_id):
    """
    Get details of a project given the project_id
    Get comments posted for this project
    """
    # List out the latest comments
    the_comments = Comment.query.filter_by(project_id=project_id).all()
    count = len(the_comments)
    comments =[]
    for i in range(count):
        comments.append(the_comments[count-1-i])
    project = Project.query.get(project_id)
    return render_template('detail.html', title="Antony Injila | Project details", project=project,comments=comments)


@app.route('/project/update/<int:project_id>', methods=['GET','POST'])
def project_update(project_id):
    project = Project.query.get(project_id)
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        image_file_old = request.form.get('image-file-old')
        f = request.files['image-file']
        filename = secure_filename(f.filename)

        if filename:
            # location for storing images: Portfolio/static/images/name_of_image
            image_file = "{}/{}/{}".format("static", "images/uploads", filename)
            # image upload
            f.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/uploads", filename))
            project.image_file = image_file
            db.session.commit()
        else:
            project.name = name
            project.description = description
            project.image_file = image_file_old
            # save the new changes
            db.session.commit()
            # return redirect('/project/update/{}/'.format(project_id))
            return redirect('/project/update/{}'.format(project.id))


    return render_template('detail.html', title="Antony Injila | Project update", project=project, )


@app.route('/projects')
def project_list():
    projects = Project.query.all()
    return render_template('projects.html', title="Antony Injila | Home Project", projects=projects)


@app.route('/project/delete/<int:project_id>', methods=['GET','POST'])
def project_delete(project_id):
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('project_list'))


@app.route('/comment/project/', methods=['GET','POST'])
def comment():
    if request.method == 'POST':
        comment = request.form.get('comment')
        project_id = request.form.get('project_id')

        new_comment = Comment(project_id=project_id,comment=comment)
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/project/detail/{}'.format(project_id))
    return render_template('detail.html', title="Antony Injila | Project details", project=project)
