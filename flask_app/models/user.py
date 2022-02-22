# ---------------------------------------------------------------------------------
# - IMPORT -
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import character

# - EMAIL & NAME FORMATTING -
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# - USER CLASS -
class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.name = data['name']
        self.pronouns = data['pronouns']
        self.birthday = data['birthday']
        self.twitter = data['twitter']
        self.about_me = data['about_me']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.characters = []
        self.favorites = []
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - CREATE NEW ACCOUNT -
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('character_directory').query_db(query, data)

    # - VALIDATE REGISTRATION INPUT -
    @staticmethod
    def validate_register(form_data):
        is_valid = True
        # email can't already be in db
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('character_directory').query_db(query,form_data)
        if len(results) >= 1:
            flash("Email already taken!")
            is_valid=False
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL('character_directory').query_db(query, form_data)
        if len(results) >= 1:
            flash("Username already taken!")
        if len(form_data['username']) < 3:
            flash("Username must be at least 3 characters!")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters!")
            is_valid = False
        elif form_data['password'] != form_data['confirm_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - EDIT USER -
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET name = %(name)s, pronouns = %(pronouns)s, birthday = %(birthday)s, twitter = %(twitter)s, about_me = %(about_me)s, updated_at = NOW() WHERE id = %(user_id)s;"
        results = connectToMySQL('character_directory').query_db(query, data)
        return

    # - VALIDATE PROFILE -
    @staticmethod
    def validate_profile(form_data):
        is_valid = True
        if not NAME_REGEX.match(form_data['name']):
            flash("Invalid name!")
            is_valid = False
        if len(form_data['pronouns']) > 10:
            flash("Pronoun field can only hold up to 10 characters!")
            is_valid = False
        if len(form_data['about_me']) > 255:
            flash("About Me section can not be more than 255 characters!")
            is_valid = False
        if form_data['birthday'] == "":
            flash("Please fill out your birthday!")
            is_valid = False
        return is_valid
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - LOGIN METHOD -
    @classmethod
    def get_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL('character_directory').query_db(query, data)
        # didn't find a matching account
        if len(result) < 1:
            return False
        return cls(result[0])
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - GET ALL USERS -
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('character_directory').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    # - GET SPECIFIC USER BY ID -
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL('character_directory').query_db(query, data)
        return cls(result[0])
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - FAVORITE CHARACTER -
    @classmethod
    def favorite_character(cls, data):
        query = "INSERT INTO favorites (user_id, character_id, created_at) VALUES (%(user_id)s, %(character_id)s, NOW());"
        return connectToMySQL('character_directory').query_db(query, data)

    # - VALIDATE FAVE -
    @staticmethod
    def validate_fave(form_data):
        is_valid = True
        query = "SELECT * FROM favorites WHERE user_id = %(user_id)s AND character_id = %(character_id)s;"
        results = connectToMySQL('character_directory').query_db(query,form_data)
        if len(results) >= 1:
            flash("Character already faved!")
            is_valid=False
        return is_valid
# ---------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------
    # - GET ALL CHARACTERS BASED ON USER -
    @classmethod
    def get_all_characters(cls, data):
        query = "SELECT * FROM users LEFT JOIN characters ON users.id = characters.user_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL('character_directory').query_db(query, data)
        user = cls(results[0])
        for row in results:
            character_data = {
                "id" : row['characters.id'],
                "name" : row['characters.name'],
                "age" : row['age'],
                "gender" : row['gender'],
                "pronouns" : row['characters.pronouns'],
                "species" : row['species'],
                "alignment" : row['alignment'],
                "description" : row['description'],
                "created_at" : row['characters.created_at'],
                "updated_at" : row['characters.updated_at']
            }
            user.characters.append(character.Character(character_data))
        return user

    # - GET ALL FAVORITES BASED ON USER -
    @classmethod
    def get_all_favorites(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN characters ON favorites.character_id = characters.id WHERE users.id = %(user_id)s;"
        results = connectToMySQL('character_directory').query_db(query, data)
        user = cls(results[0])
        for row in results:
            character_data = {
                "id" : row['characters.id'],
                "name" : row['characters.name'],
                "age" : row['age'],
                "gender" : row['gender'],
                "pronouns" : row['characters.pronouns'],
                "species" : row['species'],
                "alignment" : row['alignment'],
                "description" : row['description'],
                "created_at" : row['characters.created_at'],
                "updated_at" : row['characters.updated_at']
            }
            user.favorites.append(character.Character(character_data))
        return user
# ---------------------------------------------------------------------------------