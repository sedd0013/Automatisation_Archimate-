from imports import * 


class Element:

    # ______________ Constructeur de la classe 'Element' ______________
    #
    # Initialise un nouvel objet de la classe 'Element' avec les informations fournies.
    #
    # @param ID   : id de l'élément
    # @param type : type de l'élément 
    # @param name : nom de l'élément
    #
    # @return : None
    #
    def __init__(self, ID, Name, Type) -> None:
        self.id = ID
        self.name = Name
        self.type = Type


    # ______________ getter de l'id d'un élément ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) L'id de l'objet 
    #
    @property
    def getId(self) -> str:
        return self.id


    # ______________ setter de l'id d'un élément ______________
    #
    # @param self : L'instance de la classe en question
    # @param Name (str): Le nouvel ID de l'élément
    #
    # @return : None
    #
    @getId.setter
    def setId(self, ID: str) -> None:
        self.id = ID


    # ______________ getter du type d'un élément ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) Le type de l'objet 
    #
    @property
    def getType(self) -> str:
        return self.type


    # ______________ setter du type d'un élément ______________
    #
    # @param self : L'instance de la classe en question
    # @param Name (str): Le nouveau type de l'élément
    #
    # @return : None
    #
    @getType.setter
    def setTye(self, Type: str) -> None:
        self.type = Type

    # ______________ getter du nom d'un élément ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) Le nom de l'objet 
    #
    @property
    def getName(self) -> str:
        return self.name
    
    # ______________ setter du nom d'un élément ______________
    #
    # @param self : L'instance de la classe en question
    # @param Name (str): Le nouvel intitulé de l'élément
    #
    # @return : None
    #
    @getName.setter
    def setName(self, Name: str) -> None:
        self.name = Name


    # ______________ élément to string ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : l'élément sous format string
    #
    @property
    def __str__(self) -> str:
        return f" Element {self.id} - {self.type} - {self.name}"


    # ______________ Recup de la DATA provenant de la BD PROD ______________
    #
    # @param bd_prod_config (dict): Données de connexion a la DB [PROD]
    #
    # @return : (list) liste contenant les données récupérées
    #
    @staticmethod
    def bd_PROD_connect_and_export(bd_prod_config: dict) -> list:

        conn = mysql.connector.connect(**bd_prod_config)
        cur = conn.cursor()

        try:
            with open('Scripts/getElements.sql', 'r') as requete:
                query = requete.read()

        except FileNotFoundError:
            print("Erreur : Le fichier SQL 'getElements.sql' n'a pas été trouvé. [Manip PROD]")
        except SyntaxError:
            print("Erreur : Syntaxe SQL incorrecte dans le fichier SQL 'getElements.sql'. [Manip PROD]")
        except UnicodeError:
            print("Erreur : Problèmes d'encodage lors de la lecture du fichier SQL 'getElements.sql'. [Manip PROD]")

        cur.execute(query)
        result = cur.fetchall()

        list_elements_prod = [list(row) for row in result]

        return list_elements_prod


    # ______________ Recup des 'events' provenant de la BD DEV ______________
    #
    # @param bd_dev_config (dict): Données de connexion a la DB [DEV]
    #
    # @return : (list) liste contenant les 'events' récupérées
    #
    @staticmethod
    def bd_DEV_connect_and_export(bd_dev_config: dict) -> list:
        
        conn = mysql.connector.connect(**bd_dev_config)
        cur = conn.cursor()
        try:
            with open('Scripts/getElements.sql', 'r') as requete:
                query = requete.read()

        except FileNotFoundError:
            print("Erreur : Le fichier SQL 'getElements.sql' n'a pas été trouvé. [Manip DEV]")
        except SyntaxError:
            print("Erreur : Syntaxe SQL incorrecte dans le fichier SQL 'getElements.sql'. [Manip DEV]")
        except UnicodeError:
            print("Erreur : Problèmes d'encodage lors de la lecture du fichier SQL 'getElements.sql'. [Manip PROD]")

        cur.execute(query)
        result = cur.fetchall()

        list_events_dev = [row[4] for row in result if row[4] is not None]

        return list_events_dev


    # ______________ Comparaison des données provenant des environnements [PROD et DEV] de BD  ______________
    #
    # @param bd_prod_config (dict): Données de connexion a la DB [PROD]
    # @param bd_dev_config (dict) : Données de connexion a la DB [DEV]
    # @param bd_file_export (str) : fichier .csv contenant les données de la BD.
    # @param path_bd_export (str) : Chemin vers le fichier .csv contenant les données de la BD.
    #
    # @return : None
    #
    @staticmethod
    def compare_bds(bd_prod_config: dict, bd_dev_config: dict, bd_file_export: str, path_bd_export: str) -> None:
        
        # Call bd_PROD_connect_and_export
        list_elements_prod = Element.bd_PROD_connect_and_export(bd_prod_config)
        # Call bd_DEV_connect_and_export
        list_events_dev = Element.bd_DEV_connect_and_export(bd_dev_config)

        _ = [[None, None, None, None, objet, 'ApplicationEvent'] for objet in list_events_dev if [None, None, None, None, objet, 'ApplicationEvent'] not in list_elements_prod]

        if(len(_) > 0):
            print("Des objets trouvés en Dev qui ne sont pas en Prod : ", len(_), ' -> ')
            print([i[4] for i in _], "\n")

        completeList = list_elements_prod + _
        try :
            with open(path_bd_export, "w", newline='') as file_db_export:
                writer = csv.writer(file_db_export, delimiter=',')
                writer.writerow(["API_NAME", "METHOD_NAME", "EDA_QUEUE_NAME", "UDG_OBJECT", "EVENTS", "ELEMENT"])  

                for row in completeList:
                    for i in range(len(row)):
                        if row[i] is None:
                            row[i] = ""
                    writer.writerow(row)
                    
        except csv.Error as e:
            print(f"Erreur lors de l'écriture dans le fichier {path_bd_export}: {e}")

        print(f"Création du fichier {bd_file_export} terminée.")


    # ______________ Recup de la DATA provenant du GitLab Archimate ______________
    #
    # @param path_gitlab_downloads (str): Chemin vers le dossier contenant les données. 
    # @param url (str)                  : url du git
    # @param branch (str)               : branche du git pour récupérer
    #
    # @return : None
    #
    @staticmethod
    def download_gitlab_folder(path_gitlab_downloads: str, url: str, branch: str, ) -> None:
        try:
            # Création du dossier local
            path_dossier_appli = path_gitlab_downloads
            os.mkdir(path_dossier_appli)
            # Clonage du dépôt Git
            try:
                repo = git.Repo.clone_from(url, "temp_repo", branch=branch)

            except git.exc.GitCommandError as e:
                print(f"Erreur lors du clonage du dépôt Git : {e}")
            
            path_repo_model = "temp_repo/model/application"

            for element in os.listdir(path_repo_model):
                path_element = os.path.join(path_repo_model, element)

                if os.path.isdir(path_element):
                    try:
                        shutil.move(path_element, path_dossier_appli)
                    except Exception as e:
                        print(f"Erreur lors du déplacement de {path_element} : {e}")
            try:
                os.system('rmdir /s /q "temp_repo"')
            except Exception as e:
                print(f"Erreur lors de la suppression du dossier temporaire 'temp_repo' : {e}")

            print("\nLe dossier application a bien été téléchargé\n")

        except Exception as e:
            print(f"Une erreur s'est produite dans 'download_gitlab_folder()' : {e}")


    # ______________ Création des fichiers d'exports a partir des données GitLab_Archimate ______________
    #
    # @param path_file_archiExports (str): Chemin vers le fichier de données .csv crée a partir des données ArchiMate
    # @param path_gitlab_downloads (str) : Chemin vers le dossier contenant les données. 
    #
    # @return : None
    #
    @staticmethod
    def create_export_archi_file(path_file_archiExports: str, path_gitlab_downloads: str) -> None:

        with open(path_file_archiExports, 'w', newline='') as import_csv:
            writer = csv.writer(import_csv, delimiter=',')
            writer.writerow(["ID","Type","Name","Documentation","Specialization"])  
            
            for dossier in os.listdir(path_gitlab_downloads):
                path_dossier_child = os.path.join(path_gitlab_downloads, dossier)

                for fichier in os.listdir(path_dossier_child):
                    composantes = []
                    match = re.match(r"([^_]*)", fichier)
                    type = match.group(1)
                    
                    path_fichier_data = minidom.parse(os.path.join(path_dossier_child, fichier))
                    comp_list = path_fichier_data.getElementsByTagName(f"archimate:{type}")
                    
                    if comp_list:
                        comp_list = comp_list[0]

                        id = comp_list.getAttribute("id")
                        name = comp_list.getAttribute("name")
                        documentation = comp_list.getAttribute("documentation").encode('utf-8')
                        specialization = comp_list.getAttribute("Specialization").encode('utf-8')
                            
                        composantes.extend([id, type, name, documentation, specialization])

                    else:
                        composantes.extend(['', '', '', '', ''])
                    
                    writer.writerow(composantes)

        # ___ Pour visualiser les données du fichier produit grace a la fonction GitLab_export_process(), il faut penser a les decoder avant !
        # ___ Exemple : 
        # ______   with open("votre_fichier.csv", 'r', encoding='utf-8') as file:
        #     ______   reader = csv.reader(file)
        #     ______   for row in reader:
        #         ______   # Décodez chaque élément de la ligne en UTF-8
        #         ______   decoded_row = [element.decode('utf-8') for element in row]
        #         ______   print(decoded_row)


    # ______________ Process d'export ______________
    #
    # @param git_config (args) : paramétres d'accées au git
    # @param path_file_archiExports (str): Chemin vers le fichier de données .csv crée a partir des données ArchiMate
    # @param path_gitlab_downloads (str) : Chemin vers le dossier contenant les données. 
    # @param date_actuelle (Datetime)    : date actuelle (jour, mois, année)
    #
    # @return : None
    #
    @staticmethod
    def GitLab_export_process(git_config: dict, path_file_archiExports: str, path_gitlab_downloads: str, date_actuelle) -> None:

        # Call download_gitlab_folder
        Element.download_gitlab_folder(path_gitlab_downloads, **git_config)
        # Call create_export_archi_file
        Element.create_export_archi_file(path_file_archiExports, path_gitlab_downloads)


    # ______________ Manip de la DATA provenant de la BD et gestion des Events ______________
    
    # @param path_bd_export (str)    : Chemin vers le fichier .csv contenant les données de la BD.
    # @param path_file_lastSeen (str): Chemin vers le fichier .csv contenant les events et leur dernière date d'apparitionen BD
    
    # @return : (dict) 
    
    @staticmethod
    def create_dict_db(path_bd_export: str, path_file_lastSeen: str) -> dict:

        dict_bd_export = {}
        path_bd_export = pd.read_csv(path_bd_export)

        for i, ligne in path_bd_export.iterrows():

            if(ligne['API_NAME']):
                dict_bd_export[str(ligne['API_NAME']) + "." + str(ligne['METHOD_NAME'])] = ligne["ELEMENT"]

            if(ligne['EDA_QUEUE_NAME']):
                dict_bd_export[ligne['EDA_QUEUE_NAME']] = ligne["ELEMENT"]

            if(ligne['UDG_OBJECT']):
                dict_bd_export["udg." + str(ligne['UDG_OBJECT'])] = ligne["ELEMENT"]
            
            if(ligne['EVENTS']):
                dict_bd_export[ligne['EVENTS']] = ligne["ELEMENT"]


        dict_bd_export = {str(cle):valeur for cle, valeur in dict_bd_export.items()}

        _ = [dict_bd_export.pop(key, None) for key in ["nan.nan", "nan", "udg.nan"]]

        with open(path_file_lastSeen, 'r') as liste_events:
            csv_reader = csv.reader(liste_events)
            Liste = list(csv_reader)

        Liste.pop(0)

        Liste = [Object[0] for Object in Liste]

        # Mise a jour du dictionnaire des données de BD dict_bd_export
        liste_ajout =  [Object for Object in Liste if Object not in dict_bd_export.keys()]

        for i in liste_ajout:
            dict_bd_export[str(i)] = 'ApplicationEvent'

        return dict_bd_export
    

    # ______________ Manip de la DATA provenant d'Archimate ______________
    #
    # @param path_fichier_export_archi (str): Fichier elements.csv contenant les données provenaant du gitlab ArchiMate
    # @param path_bd_export (str)           : Chemin vers le fichier .csv contenant les données de la BD.
    #
    # @return : (dict) 
    #
    @staticmethod
    def create_dict_Archi(path_fichier_export_archi: str, path_bd_export: str) -> dict:

        bd_export = pd.read_csv(path_bd_export)
        distinctsElements = bd_export['ELEMENT'].unique()

        fichier_export_archi = pd.read_csv(path_fichier_export_archi, encoding='latin-1')

        # print(fichier_export_archi.columns, fichier_export_archi.shape, sep="\n")

        fichier_export_archi.drop('ID', inplace=True, axis=1)
        fichier_export_archi.drop('Documentation', inplace=True, axis=1)
        fichier_export_archi.drop('Specialization', inplace=True, axis=1)


        fichier_export_archi = fichier_export_archi[fichier_export_archi['Type'].isin(distinctsElements)]
        fichier_export_archi['Name'] = fichier_export_archi['Name'].str.replace(r'^\*', '', regex=True).replace(" ", ".").replace("data_grabber", "udg")

        # print(data_archi.columns, data_archi.shape, sep="\n")

        dict_data_archi = {}
        for i, ligne in fichier_export_archi.iterrows():
            dict_data_archi[str(ligne["Name"]).lower()] = ligne["Type"]

        return [Element('', name, value) for name, value in dict_data_archi.items()]


    # ______________ Lancement des processus de la classe Element ______________
    #
    # @return : (list) Liste contenant des instances de la classe Element
    #
    staticmethod
    def elements_Process(bd_prod_config: dict, bd_dev_config: dict, git_config: dict, bd_file_export: str, path_bd_export: str, path_file_archiExports: str, path_gitlab_downloads: str, path_file_events: str, date_actuelle, path_file_lastSeen) -> list:
        
        # Call compare_bds
        Element.compare_bds(bd_prod_config, bd_dev_config, bd_file_export, path_bd_export)

        # Call GitLab_export_process
        Element.GitLab_export_process(git_config, path_file_archiExports, path_gitlab_downloads, date_actuelle)
        # os.system('rmdir /s /q "temp_repo"')
        
        #Call create_events
        dict_bd_export = Element.create_dict_db(path_bd_export, path_file_lastSeen)

        return [Element('', name.lower(), Type) for name, Type in dict_bd_export.items()]
