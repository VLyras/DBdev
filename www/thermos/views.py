from flask import render_template, url_for, redirect, flash, request, abort

from __init__ import app, db, login_manager
from forms import BookmarkForm, LoginForm, SignupForm
from models import User, Bookmark, Tag
from flask_login import login_required, login_user, current_user, logout_user


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        destination = form.destination.data
        outbound_date = form.outbound_date.data
        outbound_time = form.outbound_time.data
        inbound_date = form.inbound_date.data
        inbound_time = form.inbound_time.data
        tags = form.tags.data
        bm = Bookmark(user=current_user, url=url, description=description, destination=destination,
                      tags=tags, outbound_date=outbound_date, outbound_time=outbound_time, inbound_date=inbound_date,
                      inbound_time=inbound_time)
        db.session.add(bm)
        db.session.commit()
        flash("Stored trip '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('bookmark_form.html', form=form, title="Add a Trip")

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}'".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title="Edit Trip")


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Signed in successfully as {}".format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Welcome, {}! Please Sign In.".format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html',tag=tag)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def no_permission(e):
    return render_template('403.html'), 403

@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)