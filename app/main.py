from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, StoreForm
from app.models import User, Post, Inventory, InventorySchema, LastUpdate, UserLogins
from app.email import send_password_reset_email
import json
from datatables import DataTables
import subprocess
from subprocess import Popen, PIPE
import abcstore


import atexit
from apscheduler.scheduler import Scheduler

cron = Scheduler(daemon=True)
cron.start()

@cron.cron_schedule(day_of_week='mon-fri', hour='10', minute='15')
def ABCDataUpdate():
    # Scotch, Bourbon, Gin, Tequila, Irish Whisky
    urls = ["https://www.meckabc.com/Products/Product-Search?d=scotch&c=","https://www.meckabc.com/Products/Product-Search?d=bourbon&c=","https://www.meckabc.com/Products/Product-Search?d=gin&c=","https://www.meckabc.com/Products/Product-Search?d=tequila&c=", "https://www.meckabc.com/Products/Product-Search?d=Irish+Whisky&c="]
    #urlsTest = ["https://www.meckabc.com/Products/Product-Search?d=gin&c="]
    #urls = ["https://www.google.com"]
    executionTime = datetime.utcnow()
    print(urls)
    print('Starting up...... Transfer Data: ' + str(executionTime))
    try:
        abcstore.transferData()
    except: 
        print('Transfer Data Failed')
    print('Transfer Data done at: ' + str(datetime.utcnow()) + ' Updating Inventory now...........')
    try:
        abcstore.updateInventory(urls, executionTime)
    except:
        print('Update Inventory Failed')
    print('Inventory Data done at: ' + str(datetime.utcnow()) + ' Updating LastUpdate now...........')
    try:
        abcstore.updateLastUpdate(executionTime)
    except:
        print('Last Update Failed')
    
    completeTime = datetime.utcnow()
    timetaken = completeTime - executionTime
    print('Complete: ' + str(completeTime) + ' took this long: ' + str(timetaken) )

atexit.register(lambda: cron.shutdown(wait=False))

print(cron.get_jobs())


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    ## TEMP!! to redirect to inventory
    return redirect(url_for('inventory'))
    ## TEMPORARY ^^^^^^^

    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    print(current_user.followed_posts())
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@app.route('/Inventory',methods=['GET', 'POST'])
@login_required
def inventory():
    inventory = Inventory.query.filter(Inventory.wtype=='Bourbon / Rye Whisky')
    form = StoreForm()
    if form.validate_on_submit():
        store = form.stores.data
        types = form.types.data
        if (store == 'all' and types == 'All'):
            inventory = Inventory.query.all()
        elif (store == 'all' or types == 'All'):
            if (store=='all'):
                inventory = Inventory.query.filter(Inventory.wtype.contains(form.types.data))
            else:
                inventory = Inventory.query.filter(Inventory.store.contains(form.stores.data))
        else:
            inventory = Inventory.query.filter(Inventory.store.contains(form.stores.data)).filter(Inventory.wtype.contains(form.types.data))
        
        updateTime = LastUpdate.query.order_by(LastUpdate.completionTime.desc()).first()
        inventory_schema = InventorySchema(many=True)
        inventoryJSON = json.dumps(inventory_schema.dump(inventory))
        if store == 'all':
            if types == 'All':
                flash('Filtering on ' + form.types.data + ' at all stores. Loading will take longer than usual.')
            else:
                flash('Filtering on ' + form.types.data + ' at all stores.')
            
        else:
            storeAddress = Inventory.query.filter(Inventory.store.contains(form.stores.data)).first()
            flash('Filtering on ' + form.types.data + ' at ' + storeAddress.address)

        return render_template('inventory.html', inventory=inventory, inventoryJSON=inventoryJSON, updateTime=updateTime.completionTime, form=form)

    updateTime = LastUpdate.query.order_by(LastUpdate.completionTime.desc()).first()
    inventory_schema = InventorySchema(many=True)
    inventoryJSON = json.dumps(inventory_schema.dump(inventory))
    return render_template('inventory.html', inventory=inventory, inventoryJSON=inventoryJSON, updateTime=updateTime.completionTime, form=form)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    if current_user.username == 'sankeerth':
        print('Executing the update database scripts')
        ABCDataUpdate()
        return render_template('admin.html')
    else:
        return render_template('404.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        loginrecord = UserLogins(loginauthor=current_user)
        db.session.add(loginrecord)
        db.session.commit()
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        loginrecord = UserLogins(loginauthor=current_user)
        db.session.add(loginrecord)
        db.session.commit()
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


