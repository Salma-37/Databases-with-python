import streamlit as st
import mysql.connector
maBase="cinema"
def AccederBD(maBase):
    try:
        conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database=maBase
        )
        c=conn.cursor(dictionary=True)
        return conn,c
    except mysql.connector.connect as error:
        print(f"Erreur de connexion à Wamp {error}")
        return None
conn,c=AccederBD(maBase)
def rech_personne(nom,prenom):
    if conn:
        c.execute("""SELECT nom,prenom FROM film WHERE nom=%s AND prenom=%s""",(nom,prenom))
        pers=c.fetchall()
        return pers
    else:
        return None
def insert_acteur(c,id,nom,prenom):
    c.execute("""SELECT * FROM acteur WHERE idActeur=%s AND nom=%s AND prenom=%s""",(id,nom,prenom))
    pers=c.fetchone()
    if not c:
        c.execute("""INSERT INTO acteur(idActeur,nom,prenom) VALUES (%d,%s,%s)""",(id,nom,prenom))
        conn.commit()
def affiche_table(c,nomTable):
    requete=f"SELECT * FROM {nomTable}"
    c.execute(requete)
    return c.fetchall()
def affiche_film(c,id):
    c.execute("""SELECT * FROM film WHERE idFilm=%s""",(id,))
    return c.fetchone()
def supr_film(c,id):
    c.execute("""DELETE FROM film WHERE idFilm=%s""",(id,))
    conn.commit()
def modif_FILMOGRAPHIE(c,id1,id2,val):
    c.execute("""UPDATE filmographie
               SET salaire=%s
              WHERE idActeur=%s AND idFilm=%s""",(val,id1,id2))
    c.commit()
def Nbr_acteurs(c,nomFilm):
    c.execute("""SELECT COUNT(idActeur) AS Nbr_acteurs
              FROM film natural join acteur
              WHERE titre=%s""",(nomFilm,))
    return c.fetchone()
def ActuersSansFilm(c):
    c.execute("""SELECT nom FROM acteur
              WHERE idActeur not in (SELECT idActeur FROM filmographie)""")
    return c.fetchall()
def ActeursDebutants(c):
    c.execute("""SELECT nom,AVG(salaire) AS moy_salaire
              FROM acteur natural join filmographie
              GROUP BY idActeur,nom
              HAVING coubt(idFilm)>=1""")
    c.fetchall()
    return c
def ActeursMemeSalaire(c):
    c.execute("""SELECT a.nom,b.nom,a.salaire
              FROM acteur a
              JOIN acteur b ON a.salaire=b.salaire
              WHERE a.idActeur<b.idActeur""")
    c.fetchall()
    return c
def SalaireDollarToDirham(c):
    c.execute("""SELECT idActeur,idFilm,role,(salaire*9) AS salaire_en_DH
              FROM filmographie""")
    c.fetchall()
    return c
def ValiderTrans(c):
    try:
        conn.commit()
        print("Toutes les requêtes ont été validées avec succès")
    except Exception as error:
        print(f"Une erreur s'est produite lors de la validation!")
        conn.rollback
def TableToFile(Fich,c,nomTable):
    requete=f'SELECT * FROM {nomTable}'
    c.execute(requete)
    lignes=c.fetchall()
    with open(Fich,"w",encoding="utf-8") as fich:
        for ligne in lignes:
            fich.write(str(ligne)+'\n')
def FileToTable(Fich,c,nomTable):
    with open(Fich,"r",encoding='utf-8') as file:
        for ligne in file:
            data=eval(ligne.strip())
            values=','.join(['%s']*len(data))
            requete=f'INSERT INTO {nomTable} VALUES ({values})'
            c.execute(requete,data)
def FermerConnex(c):
    connexion=c.connection
    c.close()
    connexion.close()
    print("Connexion fermée avec succès.")