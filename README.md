<<<<<<< HEAD
# DHIS2_processing
=======
<h1 style="color:blue">UTILISATION DE DHIS2_MOD</h1>

Ce module vous permet d'effectuer plusieurs opérations depuis des fichiers de ***consultation*** et **hospitalisation** en format __json__ ou __csv__ avec la classe **dhis2**


Ainsi la classe est un objet fusionnant les données trackers (hospitalisation et consultaion) depuis des fichiers de type __.json__ ou __.csv__.

<!-- --- -->
**FONCIONS ou METHODES :**

---

<ul style="color:blue">
<li>display_head(n) :</li>
<span style="color:rgb(20,30,90)">Afficher quelques lignes de la base de données de consultation et hospitalisation</span>
<br>
<span style="color:rgb(20,30,90); text-decoration:underline">Exemple:</span>

    mydata.display_head(3) #Trois premieres lignes

<li> export_into_excel(location) </li>
<span style="color:rgb(20,30,90)">Exporter la base de données consolidées en format EXCEL</span>
<br>
<span style="color:rgb(20,30,90); text-decoration:underline">Exemple:</span>

    mydata.export_into_excel(location = './data/DonneesTracker2024.xlsx') #Enregister en Excel dans le dossier data

<li> get_all_records(byhospi, separated, death) </li>
<span style="color:rgb(20,30,90)">Obtenir un tableau du nombre des cas des 46 Affections du B5a par <em>Sexe</em> et <em>Tranche d'age</em>. Il est possible d'avoir tout ça par hopital, en constation ou en hospitalisation et pour les cas de décès</span>
<br>
<span style="color:rgb(20,30,90); text-decoration:underline">Exemple:</span>

    mydata.get_all_records(byhospi = True, separated = False, death = True) #Cas de décès 46 affections par hopital

</ul>

<br>

**ATTRIBUTS :**

---
<ul style="color:red">
<li>num_line_col</li>
<span style="color:rgb(20,30,90)">Renvoie le nombre de lignes et colonnes de la base de données consolidées (tuple)</span>
<br>
<span style="color:rgb(20,30,90); text-decoration:underline">Exemple:</span>

    mydata.num_line_col #Cas de décès 46 affections par hopital

<li>data_frame</li>
<span style="color:rgb(20,30,90)">Renvoie la base de données en DataFrame (pd.DataFrame)</span>
<br>
<span style="color:rgb(20,30,90); text-decoration:underline">Exemple:</span>

    base_df = mydata.data_frame #Stocker la base de données dans la variable base_df

</ul>
>>>>>>> 281e6b2 (Initialisation)
