from flask import Flask ,render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from datetime import datetime


# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Create an instance of the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'amalamal20'

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
    STATUT = db.Column(db.Enum('En rayon', 'En prêt', 'En retard', 'En réserve', 'En travaux'), nullable=False)
    ETAT = db.Column(db.Enum('neuf', 'tres bon etat', 'bon etat', 'usage', 'endommage'), nullable=False)

    
    def __repr__(self):
        return f"<Exemplaire {self.NUMERO_ORD}>"

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

from sqlalchemy import text

@app.route('/documents', methods=['GET'])
def list_documents():
    query = request.args.get('query', '')  # Get the search query from the URL
    if query:
        # Wrap the raw SQL query with text(), searching across multiple fields
        sql = text("""
            SELECT * FROM document 
            WHERE TITRE LIKE :query 
            OR EDITEUR LIKE :query 
            OR IDDOC LIKE :query 
            OR ANNEEPUB LIKE :query
        """)
        
        # Execute the raw SQL query and pass the query parameter as a bind value
        documents = db.session.execute(sql, {'query': f'%{query}%'}).fetchall()
    else:
        documents = Document.query.all()  # If no query, return all documents

    return render_template('document.html', documents=documents, query=query)



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

@app.route('/exemplaires', methods=['GET'])
def list_exemplaires():
    query = request.args.get('query', '')  # Get the search query from the URL
    if query:
        # Wrap the raw SQL query with text(), searching across multiple fields
        sql = text("""
            SELECT * FROM exemplaire 
            WHERE ID_EXM LIKE :query 
            OR IDDOC LIKE :query 
            OR NUMERO_ORD LIKE :query 
            OR DATE_ACHAT LIKE :query
            OR STATUT LIKE :query 
            OR ETAT LIKE :query
        """)
        
        # Execute the raw SQL query and pass the query parameter as a bind value
        exemplaires = db.session.execute(sql, {'query': f'%{query}%'}).fetchall()
    else:
        exemplaires = Exemplaire.query.all()  # If no query, return all exemplaires

    return render_template('exemplaire.html', exemplaires=exemplaires, query=query)

@app.route('/add-exemplaire')
def add_exemplaire():
    documents = Document.query.all()
    return render_template('ajouterExm.html', documents=documents)
   # return render_template('ajouterExm.html', action='Ajouter')

@app.route('/save-exemplaire', methods=['POST'])
def save_exemplaire():
    iddocu = request.form['IDDOC']
    Numero_ordre = request.form['NUMERO_ORD']
    Date_achat = request.form['DATE_ACHAT']
    statut = request.form['STATUT']  # Assurez-vous que les valeurs envoyées correspondent aux valeurs ENUM définies
    etat = request.form['ETAT']
    
    new_exemplaire = Exemplaire(IDDOC=iddocu,NUMERO_ORD=Numero_ordre, DATE_ACHAT=Date_achat, STATUT=statut ,ETAT=etat)
    
    db.session.add(new_exemplaire)
    db.session.commit()

    # Redirection ou message de succès
    flash('Exemplaire ajouté avec succès !')
    return redirect(url_for('list_exemplaires'))

@app.route('/edit-exemplaire/<int:exemplaire_id>', methods=['GET', 'POST'])
def edit_exemplaire(exemplaire_id):
    exemplaire = Exemplaire.query.get_or_404(exemplaire_id)

    if request.method == 'POST':
        exemplaire.NUMERO_ORD = request.form['numero']
        exemplaire.DATE_ACHAT= request.form['date']
        exemplaire.STATUT = request.form['statut']
        exemplaire.ETAT= request.form['etat']

        db.session.commit()
        return redirect(url_for('list_exemplaires'))

    return render_template('edit_exemplaire.html', exemplaire=exemplaire, action='Modifier')


# Supprimer un document
@app.route('/delete-exemplaire/<int:exemplaire_id>')
def delete_exemplaire(exemplaire_id):
    exemplaire_obj = Exemplaire.query.get_or_404(exemplaire_id)
    db.session.delete( exemplaire_obj)
    db.session.commit()
    return redirect(url_for('list_exemplaires'))

if __name__ == '__main__':
    app.run(debug=True)