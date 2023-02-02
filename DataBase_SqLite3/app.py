# Copyright 2023 Oussama EL-FIGHA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_artists(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM artiste")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_album_by_id_artist(conn, id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT titre FROM album WHERE artiste_id=?", (id,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def insert_album(nom_artiste, nom_album, annee, conn):
    cur = conn.cursor()
    cur.execute("SELECT id FROM artiste WHERE nom LIKE ?", ('%' + nom_artiste + '%',))
    # On fetch les id des artistes qui matchent (si ils existent)
    existe = cur.fetchall()
    # print(existe)
    if existe:
        # On récupere l'id
        # Decommentez la trace (les prints) pour une explication un peu plus "visuelle" :)
        id_artiste = existe[0][0]
        # print(id_artiste)
        # On update les donnees de l'artiste correspondant a artiste_id en ajoutant le nouvel album à la table album
        cur.execute("INSERT INTO album (titre, annee, artiste_id)" "VALUES(?,?,?)", (nom_album, annee, id_artiste))
    else:
        # On insère le nouvel artiste dans la table artiste
        cur.execute("INSERT INTO artiste (nom, est_solo, nombre_individus)" "VALUES(?, ?, ?)", (nom_artiste, 0, 1))
        # On récupere l'id du dernier artiste ajouté
        cur.execute("SELECT last_insert_rowid()")
        last_id = cur.fetchone()[0]
        # A partir de l'id du dernier artiste ajouté on ajoute son album a la table album
        cur.execute("INSERT INTO album (titre, annee, artiste_id)" "VALUES(?, ?, ?)", (nom_album, annee, last_id))


def main():
    database = r"musique.db"

    # create a database connection
    conn = create_connection(database)

    id_artist = int(input("enter an id of the artist :"))

    with conn:
        print("\n\n1. Query album_by_id_artist:")
        select_album_by_id_artist(conn, id_artist)

        print("\n\n2. Query all tasks")
        select_all_artists(conn)

        print("\n\n3. insert album")
        with open("input.txt", "r") as infile:
            for line in infile:
                splitted_line = line.split('|')
                insert_album(splitted_line[0], splitted_line[1], splitted_line[2], conn)
            # Par mesure de sécurité toujours fermer les fichiers après traitement
            infile.close()

            # Pour visualiser les changemets ayant été faits sur la base de données
            print("\n\nvisualiser les changemets ayant été faits sur la base de données")
            select_all_artists(conn)


if __name__ == '__main__':
    main()
