from flask_app import app
from flask_app import views
from storage.database_tables import db

#db.create_all()
if __name__ == "__main__":
    app.run(debug=True)