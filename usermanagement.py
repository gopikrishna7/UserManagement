from flask import Flask, request, redirect, render_template ,jsonify, url_for, session
from mysql.connector import connect, Error
import bcrypt

app = Flask(__name__)
app.secret_key = 'secret_key'

# Connect to the RDS instance
cnx = connect(user='gopikrishna',
              password='Mandadi@7',
              host='pythoncart.mysql.database.azure.com',
              database='mydb')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the user input
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']


        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        #with cnx.cursor() as cursor:
        cursor = cnx.cursor()
        sql_query = "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)"
        cursor.execute(sql_query, (email, hashed_password, name))
        cnx.commit()
        cursor.close()
                
        # Insert the user details into the database
        

        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get the user name and password from the request
    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']

        with cnx.cursor() as cursor:
            query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode(), user[3].encode()):
            #if user[3]==password:
                session['user_id']=user[0]
                #return redirect('/products')
                return render_template('login_success.html', user=user[1])

            else:
                error = "Incorrect username or password"
                return render_template('login.html', error=error)
        else:
            error = "Incorrect username or password"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)