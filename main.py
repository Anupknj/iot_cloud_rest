import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
# from werkzeug.security import generate_password_hash, check_password_hash

#Adding a new user is handled via POST request
@app.route('/add', methods=['POST'])
def add_student():
    #For testing purpose only. To compare POST request data with inserted DB values
    #print(request.json)
    try:
        #Fetching the POST request data
        _json = request.json
        print(_json)
        _name = _json['name']
        _subject = _json['subject']
    
        #validating the received POST request values
        if _name and _subject and request.method == 'POST':
            
            sql = "INSERT INTO student(name, subject) VALUES(%s, %s)"
            data = (_name, _subject)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('student added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#Fetching the existing users data
@app.route('/students')
def users():
    print("inside get fn")
    try:
        print("inside try")
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print("inside exception")
        print(e)
    finally:
        cursor.close() 
        conn.close()

#Fetching the details of a particular user using id via GET request
@app.route('/student/<string:id>', methods = ['GET'])
def user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student WHERE id=%d", int(id))
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#Updating the data of a respective user via PUT request
@app.route('/update', methods=['PUT'])
def update_user():
    try:
        _json = request.json
        _student_id = int(_json['id'])
        _name = _json['name']
        _subject = _json['subject']
        # validatng the received PUT values
        if _name and _subject  and _student_id and request.method == 'PUT': 
          
            #Storing the POST request data into the DB using SQL query
            sql = "UPDATE student SET name=%s, subject=%s WHERE id=%d"
            data = (_name, _subject,_student_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Student updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#Deleting a user data is handled via DELETE request
@app.route('/delete/<string:id>', methods=['DELETE'])
def delete_user(id):
    try:
        id = int(id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id=%d", (id,))
        conn.commit()
        resp = jsonify('Student deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#Handling the error in the application
@app.errorhandler(404)
def not_found(error=None):
    message = {
    'status': 404,
    'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    #to connect to ec2 from post man 
    app.run(host='0.0.0.0', port=5000, debug=True)
