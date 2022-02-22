# ---------------------------------------------------------------------------------
# - IMPORT -
from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.character import Character
from flask_app.models.user import User
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - CREATE NEW CHARACTER -
@app.route('/add_character')
def add_character():
    if "user_id" not in session:
        flash("Please register or login before continuing!")
        return redirect('/')
    data = {
        "user_id" : session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('add_character.html', user = user)

# - VALIDATE & PROCESS CHARACTER -
@app.route('/save_character', methods=["POST"])
def save_character():
    if not Character.validate_character(request.form):
        return redirect('/add_character')
    data = {
        "name" : request.form['name'],
        "age" : request.form['age'],
        "gender" : request.form['gender'],
        "pronouns" : request.form['pronouns'],
        "species" : request.form['species'],
        "alignment" : request.form['alignment'],
        "description" : request.form['description'],
        "user_id" : request.form['user_id']
    }
    character_id = Character.save(data)
    return redirect(f'/character/{character_id}')
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - VIEW CHARACTER PROFILE -
@app.route('/character/<int:character_id>')
def show_character(character_id):
    data = {
        "character_id" : character_id
    }
    character = Character.show_character(data)
    return render_template('character.html', character = character)
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
# - EDIT CHARACTER -
@app.route('/edit_character/<int:character_id>/<int:user_id>')
def edit_character(character_id, user_id):
    if "user_id" not in session:
        flash("Please register or login before continuing!")
        return redirect('/')
    if not session['user_id'] == user_id:
        flash("You don't have access to that page!")
        return redirect(f'/character/{character_id}')
    data = {
        "character_id" : character_id,
    }
    character = Character.show_character(data)
    return render_template('edit_character.html', character = character)

# - VALIDATE & PROCESS CHARACTER EDIT -
@app.route('/update_character/<int:character_id>/<int:user_id>', methods=["POST"])
def update_character(character_id, user_id):
    if not Character.validate_character(request.form):
        return redirect(f'/edit_character/{character_id}/{user_id}')
    data = {
        "name" : request.form['name'],
        "age" : request.form['age'],
        "gender" : request.form['gender'],
        "pronouns" : request.form['pronouns'],
        "species" : request.form['species'],
        "alignment" : request.form['alignment'],
        "description" : request.form['description'],
        "character_id" : character_id
    }
    Character.edit_character(data)
    return redirect(f'/character/{character_id}')
    # ---------------------------------------------------------------------------------