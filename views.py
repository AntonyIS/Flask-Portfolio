from app import *
from models import User, Project,Comment,db

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))



@app.route('/')
@cache.cached(timeout=50)
def index():
    projects = Project.query.all()[:4]
    return render_template('index.html', title="Antony Injila | Home", projects=projects)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
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
    return render_template('dashboard.html', title="Antony Injila | Dashboard", user=user)


@app.route('/dashboard/update', methods=['GET','POST'])
def dashboard_update():
    user = User.query.get(1)
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        about = request.form.get('about')

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
            user.name = name
            user.email = email
            user.about = about
            user.image_file = image_file_old

        # save the new changes
            db.session.commit()
        # return redirect('/project/update/{}/'.format(project_id))
            return redirect(url_for('dashboard'))

    return render_template('detail.html', title="Antony Injila | Project update", project=project)


@app.route('/about')
def about():
    return render_template('about.html', title='Antony Injila | About page')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == 'admin@example.com' and password == 'pass1234':
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
    comments = Comment.query.filter_by(project_id=project_id).all()
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
    return redirect('/')


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
