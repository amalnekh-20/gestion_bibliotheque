from flask import Flask ,render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Create an instance of the Flask application
app = Flask(__name__)

# Configuration of the database using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://amalnekh:amalsalma@localhost/gestion_Bibliothèque')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize SQLAlchemy
db = SQLAlchemy(app)
class document(db.Model):
    __tablename__ = 'document'
    IDDOC = db.Column(db.Integer, primary_key=True)
    TITRE = db.Column(db.String(50), nullable=False)
    ANNEEPUB = db.Column(db.Integer, nullable=False)
    EDITEUR = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<document {self.TITRE}>"

@app.route('/')
def home():
    return """
    <h1>Bienvenue à la Gestion Bibliothèque</h1>
    <p><a href='/documents'>Voir les Documents</a></p>
    """

# Route for listing documents
@app.route('/documents')
def list_documents():
    documents = document.query.all()
    return render_template('document.html', documents=documents)
@app.route('/add-document')
def add_document():
    return render_template('edit_document.html', action='Ajouter')

# Page de modification de document
@app.route('/edit-document/<int:document_id>', methods=['GET', 'POST'])
def edit_document(document_id):
    document = document.query.get_or_404(document_id)

    if request.method == 'POST':
        document.TITRE = request.form['titre']
        document.ANNEEPUB = request.form['annee']
        document.aEDITEUR = request.form['editeur']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_document.html', document=document, action='Modifier')

# Supprimer un document
@app.route('/delete-document/<int:document_id>')
def delete_document(document_id):
    document = document.query.get_or_404(document_id)
    db.session.delete(document)
    db.session.commit()
    return redirect(url_for('index'))

# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
