from flask import Flask, session
import os
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

logging.basicConfig(filename = 'record.log', level = logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
@app.route('/blogs')
def blog():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return f"Welcome to the Blog" 