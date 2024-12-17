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
class Document(db.Model):
    __tablename__ = 'document'
    IDDOC = db.Column(db.Integer, primary_key=True)
    TITRE = db.Column(db.String(50), nullable=False)
    ANNEEPUB = db.Column(db.Integer, nullable=False)
    EDITEUR = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Document {self.TITRE}>"

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    ID_UTIL = db.Column(db.Integer, primary_key=True)
    NOM_U = db.Column(db.String(50), nullable=False)
    PRENOM_U = db.Column(db.String(50), nullable=False)
    CATEGORIE = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Utilisateur {self.ID_UTIL}>"

class Exemplaire(db.Model):
    __tablename__ = 'exemplaire'
    ID_EXM = db.Column(db.Integer, primary_key=True)
    IDDOC = db.Column(db.Integer, nullable=False)
    NUMERO_ORD = db.Column(db.Integer, nullable=False)
    DATE_ACHAT = db.Column(db.Date, nullable=False)
    STATUT = db.Column(db.String(50), nullable=False)
    ETAT = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Exemplaire {self.ID_EXM}>"

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/documents')
def list_documents():
    documents = Document.query.all()
    return render_template('document.html', documents=documents)


@app.route('/add-document')
def add_document():
    return render_template('ajouterDoc.html', action='Ajouter')

@app.route('/save-document', methods=['POST'])
def save_document():
    #iddoc = request.form['IDDOC']
    titre = request.form['TITRE']
    annee_pub = request.form['ANNEEPUB']
    editeur = request.form['EDITEUR']
    
    # Crée une instance du modèle document
    new_document = Document(TITRE=titre, ANNEEPUB=annee_pub, EDITEUR=editeur)
    
    # Ajoute à la base de données
    db.session.add(new_document)
    db.session.commit()
    
    return redirect(url_for('list_documents'))


@app.route('/edit-document/<int:document_id>', methods=['GET', 'POST'])
def edit_document(document_id):
    document = Document.query.get_or_404(document_id)

    if request.method == 'POST':
        document.TITRE = request.form['titre']
        document.ANNEEPUB = request.form['annee']
        document.EDITEUR = request.form['editeur']

        db.session.commit()
        return redirect(url_for('list_documents'))

    return render_template('edit_document.html', document=document, action='Modifier')


# Supprimer un document
@app.route('/delete-document/<int:document_id>')
def delete_document(document_id):
    document_obj = Document.query.get_or_404(document_id)
    db.session.delete(document_obj)
    db.session.commit()
    return redirect(url_for('list_documents'))


if __name__ == '__main__':
    app.run(debug=True)