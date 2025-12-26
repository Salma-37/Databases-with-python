'''import streamlit as st
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
    '''

import streamlit as st
import mysql.connector
import pandas as pd
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
        st.error(f"Erreur de connexion à Wamp {error}")
        return None,None
conn,c=AccederBD(maBase)
def rech_personne(nom,prenom):
    if conn:
        c.execute("""SELECT idActeur,nom,prenom,titre as titre_film,salaire 
                  FROM acteur natural join filmographie natural join film
                  WHERE nom=%s AND prenom=%s""",(nom,prenom))
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
    c.execute("""SELECT titre , COUNT(idActeur) AS Nbr_acteurs
              FROM filmographie natural join film
              WHERE titre=%s
              GROUP BY titre""",(nomFilm,))
    return c.fetchone()
def ActuersSansFilm(c):
    c.execute("""SELECT nom,prenom FROM acteur
              WHERE idActeur not in (SELECT idActeur FROM filmographie)""")
    return c.fetchall()
def ActeursDebutants(c):
    c.execute("""SELECT nom,AVG(salaire) AS moy_salaire
              FROM acteur natural join filmographie
              GROUP BY idActeur,nom
              HAVING count(idFilm)>=1""")
    return c.fetchall()
def ActeursMemeSalaire(c):
    c.execute("""SELECT a.nom,b.nom,a.salaire
              FROM acteur a
              JOIN acteur b ON a.salaire=b.salaire
              WHERE a.idActeur<b.idActeur""")
    return c.fetchall()
def SalaireDollarToDirham(c):
    c.execute("""SELECT idActeur,idFilm,role,(salaire*9) AS salaire_en_DH
              FROM filmographie""")
    return c.fetchall()
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
    c.close()
    conn.close()
    st.success("Connexion à la base est fermée")
# STREAMLIT DASHBOARD
st.set_page_config(page_title="🎬 Cinema Dashboard", layout="wide")
st.title("🎬 Dashboard Cinéma")
st.markdown("Analyse des films, acteurs et filmographie")

if conn:
    films = affiche_table(c, "film")
    acteurs = affiche_table(c, "acteur")
    filmographie = affiche_table(c, "filmographie")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎞️ Films", len(films))
    col2.metric("🎭 Acteurs", len(acteurs))
    col3.metric("🎬 Rôles", len(filmographie))
    col4.metric("💰 Salaire moyen", f"{int(sum([f['salaire'] for f in filmographie])/len(filmographie)):,} $")

    st.subheader("🎞️ Liste des films")
    st.dataframe(pd.DataFrame(films))

    st.subheader("🚫 Acteurs sans film")
    acteurs_sans_film = ActuersSansFilm(c)
    if acteurs_sans_film:
        st.table(pd.DataFrame(acteurs_sans_film))
    else:
        st.info("Tous les acteurs ont au moins un film.")

    st.subheader("👥 Nombre d'acteurs par film")
    titres = [f['titre'] for f in films]
    film_select = st.selectbox("Choisir un film", titres)
    res = Nbr_acteurs(c, film_select)
    if res:
        st.success(f"Nombre d'acteurs : {res['Nbr_acteurs']}")

    st.subheader("💰 Salaires convertis en dirhams")
    salaires_dh = SalaireDollarToDirham(c)
    df_salaires = pd.DataFrame(salaires_dh)
    st.dataframe(df_salaires)

    st.subheader("👥 Acteurs débutants")
    acteur_deb=ActeursDebutants(c)
    st.table(pd.DataFrame(acteur_deb))

    st.subheader("✏️ Modifier un salaire")
    idActeur = st.number_input("ID Acteur", min_value=1, step=1)
    idFilm = st.number_input("ID Film", min_value=1, step=1)
    nouveau_salaire = st.number_input("Nouveau salaire ($)", min_value=0)
    if st.button("Modifier le salaire"):
        modif_FILMOGRAPHIE(c,idActeur,idFilm,nouveau_salaire)
        ValiderTrans(c)

    st.subheader("🗑️ Supprimer un film")
    id_supp = st.number_input("ID du film à supprimer", min_value=1, step=1, key='sup')
    if st.button("Supprimer le film"):
        supr_film(c,id_supp)
        ValiderTrans(c)

    st.subheader("📁 Exporter une table")
    table_export = st.selectbox("Choisir une table à exporter", ["film", "acteur", "filmographie"])
    nom_fichier = st.text_input("Nom du fichier", value="export.txt")
    if st.button("Exporter la table"):
        TableToFile(nom_fichier,c,table_export)

    st.subheader("🔎 Recherche d'une personne")
    nom = st.text_input("Nom de l'acteur")
    prenom = st.text_input("Prénom de l'acteur")
    if st.button("Rechercher"):
        res = rech_personne(nom,prenom)
        if res:
            st.table(pd.DataFrame(res))
        else:
            st.error("Personne introuvable")

    if st.button("❌ Fermer la connexion"):
        FermerConnex(c)
    if st.button("Quitter le dashboard"):
        c.close()
        conn.close()
        st.success("Connexion fermée ✅")
        st.stop()
else:
    st.error("Connexion à la base échouée.")
    
