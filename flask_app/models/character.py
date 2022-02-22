# ---------------------------------------------------------------------------------
# - IMPORT -
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

# - CHARACTER CLASS -
class Character:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.gender = data['gender']
        self.pronouns = data['pronouns']
        self.species = data['species']
        self.alignment = data['alignment']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = {}
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
  # - CREATE NEW CHARACTER -
    @classmethod
    def save(cls, data):
        query = "INSERT INTO characters (name, age, gender, pronouns, species, alignment, description, created_at, updated_at, user_id) VALUES (%(name)s, %(age)s, %(gender)s, %(pronouns)s, %(species)s, %(alignment)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL('character_directory').query_db(query, data)
        return results

    # - EDIT CHARACTER -
    @classmethod
    def edit_character(cls, data):
        query = "UPDATE characters SET name = %(name)s, age = %(age)s, gender = %(gender)s, pronouns = %(pronouns)s, species = %(species)s, alignment = %(alignment)s, description = %(description)s, updated_at = NOW() WHERE id = %(character_id)s;"
        results = connectToMySQL('character_directory').query_db(query, data)
        return

    # - VALIDATE CHARACTER -
    @staticmethod
    def validate_character(form_data):
        is_valid = True
        if form_data['name'] == '':
            flash("Character must have a name!")
            is_valid = False
        if len(form_data['pronouns']) > 10:
            flash("Pronoun field can't go over 10 characters!")
            is_valid = False
        if len(form_data['description']) > 255:
            flash("Description can't be over 255 characters!")
            is_valid = False
        return is_valid
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - GET ONE CHARACTER -
    @classmethod
    def show_character(cls, data):
        query = "SELECT * FROM characters LEFT JOIN users ON characters.user_id = users.id WHERE characters.id = %(character_id)s;"
        results = connectToMySQL('character_directory').query_db(query, data)
        character = cls(results[0])
        user_data = {
            "id" : results[0]['users.id'],
            "username" : results[0]['username'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "name" : results[0]['users.name'],
            "pronouns" : results[0]['users.pronouns'],
            "birthday" : results[0]['birthday'],
            "twitter" : results[0]['twitter'],
            "about_me" : results[0]['about_me'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at']
        }
        character.creator = user.User(user_data)
        return character
# ---------------------------------------------------------------------------------