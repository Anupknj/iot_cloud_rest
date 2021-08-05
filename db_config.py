from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '5p&0y@TRqo4L'
app.config['MYSQL_DATABASE_DB'] = 'ECE531'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
