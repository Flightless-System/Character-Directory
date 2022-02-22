# ---------------------------------------------------------------------------------
# - IMPORT -
from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - LOGIN & REGISTRATION PAGE -
@app.route('/')
def registration_and_login():
    return render_template('reg_and_log.html')

# - VALIDATE & PROCESS REGISTRATION -
@app.route('/register', methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect(f'/edit/{user_id}')

# - VALIDATE & PROCESS LOGIN -
@app.route('/login', methods=["POST"])
def login():
    data = {"username" : request.form['username']}
    user_in_db = User.get_by_username(data)
    if not user_in_db:
        flash("No account with that username!")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Incorrect password!")
        return redirect('/')
    session['user_id'] = user_in_db.id
    user_id = session['user_id']
    return redirect(f'/profile/{user_id}')
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - BROWSE USERS -
@app.route('/users')
def users():
    users = User.get_all()
    return render_template('users.html', all_users = users)

# - VIEW USER -
@app.route('/profile/<int:user_id>')
def user(user_id):
    data = {
        "user_id" : user_id
    }
    show_user = User.get_by_id(data)
    return render_template('user_prof.html', show_user = show_user)
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - EDIT USER -
@app.route('/edit/<int:user_id>')
def edit_user(user_id):
    if "user_id" not in session:
        flash("Please register or login before continuing!")
        return redirect('/')
    if  not session['user_id'] == user_id:
        flash("You don't have access to that page!")
        return redirect(f'/profile/{user_id}')
    data = {
        "user_id" : user_id
    }
    show_user = User.get_by_id(data)
    return render_template('edit_user.html', show_user = show_user)

# - VALIDATE AND PROCESS USER EDIT -
@app.route('/update_user/<int:user_id>', methods=["POST"])
def update_user(user_id):
    if not User.validate_profile(request.form):
        return redirect(f'/edit/{user_id}')
    data = {
        "name" : request.form['name'],
        "pronouns" : request.form['pronouns'],
        "birthday" : request.form['birthday'],
        "twitter" : request.form['twitter'],
        "about_me" : request.form['about_me'],
        "user_id" : user_id
    }
    User.edit_user(data)
    return redirect(f'/profile/{user_id}')
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - SHOW USER'S CHARACTERS -
@app.route('/characters/<int:user_id>')
def character_list(user_id):
    data = {
        "user_id" : user_id
    }
    user_charas= User.get_all_characters(data)
    return render_template('character_list.html', user_charas = user_charas)

# - FAVORITE CHARACTER -
@app.route('/save_favorite/<int:character_id>', methods=["POST"])
def favorite(character_id):
    if not User.validate_fave(request.form):
        return redirect(f'/character/{character_id}')
    data = {
        "user_id" : request.form['user_id'],
        "character_id" : request.form['character_id']
    }
    User.favorite_character(data)
    flash("Successfully favorited!")
    return redirect(f'/character/{character_id}')

# - SHOW USER'S FAVORITES -
@app.route('/favorites/<int:user_id>')
def favorites_list(user_id):
    data = {
        "user_id" : user_id
    }
    user_faves = User.get_all_favorites(data)
    return render_template('fave_list.html', user_faves = user_faves)
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - LOGOUT -
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
# ---------------------------------------------------------------------------------