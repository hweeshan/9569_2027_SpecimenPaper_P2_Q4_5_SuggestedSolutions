### NOTE: need to run this off local jupyter notebook for the flask app to work
# index.html (Task 4.4) must be placed in subfolder 'templates'
# style.css (Task 4.3) must be placed in subfolder 'static'

import flask
import sqlite3

app = flask.Flask(__name__)

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/process_form/', methods=['POST'])
def process_form():
    # accesses the form group entered in the text box on index.html when the submit button is pressed
    form_data = flask.request.form # dictionary
    formgroup = form_data['formgroup']

    # uses SQL to search the database you created in Task 4.1 to retrieve the quantity of students in
    # the form group from index.html, the year group of the form group and the form tutor ID
    db = sqlite3.connect('task4.db')

    cursor = db.execute('''
    SELECT COUNT(StudentID), Year, TutorID
    FROM Student
    INNER JOIN Form ON Student.FormGroupID = Form.FormGroupID
    WHERE Form.FormGroupID = ?
    ''', (formgroup,))
    
    # we're only expecting one row of result
    # so use fetchone() instead of fetchall() so that the output is a single tuple, instead of a list of tuples
    result = cursor.fetchone()

    # result is a tuple (<student count>, <year>, <tutorID>)
    
    db.close()

    # formats the retrieved data into a sentence that follows the structure:
    # There are <quantity> students in form <form group ID>. The form is in year group <year group> with the form tutor <form tutor ID>
    
    # returns a HTML document that displays the created sentence
    # shortcut: can just return the statement wrapped in <p> tag:
    # return '<p>There are {} students in form {}. The form is in year group {} with the form tutor {}</p>'.format(result[0], formgroup, result[1], result[2])

    # or, create an extra HTML document and pass the necessary variables in
    return flask.render_template('result.html', formgroup=formgroup, count=result[0], year=result[1], tutorID = result[2])

# app.run()
