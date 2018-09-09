import logging
from logging.handlers import RotatingFileHandler
import os, re
from flask import Flask, request, Response, send_file, make_response
from werkzeug.utils import secure_filename

counter = 0
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024

@app.route('/index', methods=['GET'])
def index():
    return 'Welcome'

@app.route('/getfile', methods=['POST'])
def getfile():
    global counter
    counter = counter + 1
    
    file = request.files['file']

    if not(allowed_file(file.filename)):
        return ('Not acceptable filetype!')
    
    inputTextOrig = str(file.read())
    inputText = re.sub('b', '',inputTextOrig)
    inputText = re.sub('\'', '',inputText)
    words = inputText.split()
    path = 'Keyword.txt'
    companies = open(path,'r')
    company_list = companies.readlines()
    company_list = [x.strip() for x in company_list]  
    
    modified_company_list = []

    for company_name in company_list:
        updated_company_name = company_name + u'\N{REGISTERED SIGN}'
        inputText = re.sub(r"\b%s\b"%company_name, updated_company_name, inputText, flags=re.IGNORECASE)
        inputText = re.sub(r"\\n", '\\n', inputText, flags=re.IGNORECASE)
    app.logger.warning('I was called: ' + str(counter))
   
    return Response(inputText,
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;filename=Modified.txt"})

if __name__ == '__main__':
    handler = RotatingFileHandler('converter.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    app.run()