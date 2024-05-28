from imports import * 
from createELS import createlastLoggedEventsFile


class Property :

    # ______________ Constructeur de la classe 'Property' ______________
    #
    # Initialise un nouvel objet de la classe 'Property' avec les informations fournies.
    #
    # @param ID    : id de la Propriété
    # @param Key   : nom dde la Propriété
    # @param Value : valeur de la Propriété
    #
    # @return : None
    #
    def __init__(self, ID, Key, Value):
        self.id = ID
        self.key = Key
        self.value = Value  


    # ______________ getter de l'id d'une propriété ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) L'id de la propriété 
    #
    @property
    def getId(self) -> str:
        return self.id
    

    # ______________ setter de l'id d'une propriété ______________
    #
    # @param self : L'instance de la classe en question
    # @param Name (str): Le nouvel ID de la propriété
    #
    # @return : None
    #
    @getId.setter
    def setId(self, ID: str) -> None:
        self.id = ID
    

    # ______________ getter du nom d'une propriété ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) Le nom de la propriété 
    #
    @property
    def getKey(self) -> str:
        return self.key
    

    # ______________ setter du nom d'une propriété ______________
    #
    # @param self : L'instance de la classe en question
    # @param Name (str): Le nouveau nom de la propriété
    #
    # @return : None
    #
    @getKey.setter
    def setKey(self, Key: str) -> None:
        self.key = Key
    

    # ______________ getter de la valeur d'une propriété ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) La valeur de la propriété 
    #
    @property
    def getValue(self) -> str:
        return self.value
    

    # ______________ setter de la valeur d'une propriété ______________
    #
    # @param self : L'instance de la classe en question
    # @param Name (str): La nouvelle valeur de la propriété
    #
    # @return : None
    #
    @getValue.setter
    def setValue(self, Value: str) -> None:
        self.value = Value


    # ______________ propriété to string ______________
    #
    # @param self : L'instance de la classe en question
    #
    # @return : (str) la propriété sous format string
    #
    @property
    def __str__(self) -> str:
        return f"{self.id} - {self.key} - {self.value}"
    

    # ______________ Recup de la DATA provenant de la BD DEV ______________
    #
    # @param bd_prod_config (dict): Données de connexion a la DB [PROD]
    #
    # @return : (list)
    #
    @staticmethod
    def getDataFromDataBase(bd_prod_config: dict) -> list:
    
        conn = mysql.connector.connect(**bd_prod_config)
        cur = conn.cursor()
        
        try:  
            with open('Scripts/getLastSeenDate.sql', 'r') as requete:
                query = requete.read()

            cur.execute(query)
            resultat = cur.fetchall()

            print("Les données 'getLastSeenDate' ont été chargées avec succès. [PROD]")
            return resultat
            
        except FileNotFoundError:
            print("Erreur : Le fichier SQL spécifié n'a pas été trouvé.")
        except mysql.connector.Error as err:
            print(f"Une erreur MySQL s'est produite : {err}")
        except PermissionError:
            print("Erreur : Vous n'avez pas les permissions nécessaires pour accéder au fichier SQL.")
        except SyntaxError:
            print("Erreur : Syntaxe SQL incorrecte dans le fichier.")
        except UnicodeError:
            print("Erreur : Problèmes d'encodage lors de la lecture du fichier SQL.")

        finally:
            cur.close()
            conn.close()


    # ______________ Extraction des données de mises a jours ______________
    #
    # @param bd_prod_config (dict) : Données de connexion a la DB [PROD]
    # @param format_chaine (str)   : Format de date a appliquer
    #
    # @return : (dict) dictionnaire contenant les "events" et leur dernière observation en BD
    #
    @staticmethod
    def compare_Update_Data(bd_prod_config: dict, format_chaine: str) -> dict:

        resultat = Property.getDataFromDataBase(bd_prod_config)

        try:
            reader = pd.read_csv('Data_BD_Exports/EventsLastSeenDates.csv')

            OBJECTS2LIST = reader["OBJECT"].values.tolist()
            MAXTIMESTAMPLIST = [datetime.datetime.strptime(value, format_chaine) for value in reader["MAX_TIMESTAMP"].values.tolist() ]

        except FileNotFoundError:
            print("Le fichier CSV n'a pas été trouvé.")
        except pd.errors.ParserError as e:
            print(f"Erreur lors de la lecture du fichier CSV : {e}")


        count=[0, 0]
        for element in resultat:
            if element[0] is not None and element[0] not in OBJECTS2LIST :
                print("\nNew element :",element)
                OBJECTS2LIST.append(element[0])
                MAXTIMESTAMPLIST.append(element[1])
                new_row = {'OBJECT': element[0], 'MAX_TIMESTAMP': element[1]}
                reader = pd.concat([reader, pd.DataFrame([new_row])], ignore_index=True)
                count[0] += 1
            else :
                if element[1] > MAXTIMESTAMPLIST[OBJECTS2LIST.index(element[0])]:
                    MAXTIMESTAMPLIST[OBJECTS2LIST.index(element[0])] = element[1]
                    reader.loc[reader['OBJECT'] == element[0], 'MAX_TIMESTAMP'] = element[1]
                    count[1] += 1

        reader.to_csv('Data_BD_Exports/EventsLastSeenDates.csv', index=False)

        print(f"\nLes données ont été mises à jour avec succès dans le fichier EventsLastSeenDates.csv !")
        print(f"\t- {count[0]} Ajouts\n\t- {count[1]} Mises a jours")

        # data_ObjectDates = {OBJECTS2LIST[i] : MAXTIMESTAMPLIST[i] for i in range(len(OBJECTS2LIST))}

        return {OBJECTS2LIST[i] : MAXTIMESTAMPLIST[i] for i in range(len(OBJECTS2LIST))}
    

    # ______________ Mise a jour du fichier cerateELS.py ______________
    #
    # @param data_ObjectDates (dict): Un dictionnaire contenant les "events" et leur dernière observation en BD
    #
    # @return : None
    #
    @staticmethod
    def update_createELS(data_ObjectDates: dict) -> None:

        path_createELS = 'Scripts/createELS.py'
        try:
            with open(path_createELS, 'r') as f:
                lignes = f.readlines()

            for i, ligne in enumerate(lignes):
                if 'data_ObjectDates = {' in ligne:
                    lignes[i] = textwrap.indent('data_ObjectDates = ' + str(data_ObjectDates) + '\n', '        ')
        
        except FileNotFoundError:
            print("Le fichier createELS.py n'a pas été trouvé.")
            return
        except IOError as e:
            print(f"Erreur lors de la lecture du fichier createELS.py : {e}")
            return

        try :
            with open(path_createELS, 'w') as f:
                f.writelines(lignes)
            print("\nLe fichier createELS.py a été mis à jour avec succès.")

        except IOError as e:
            print(f"Erreur lors de l'écriture dans le fichier createELS.py : {e}\n")


    # ______________ Lancement des processus de la classe Property ______________
    #
    # @return: (list) Liste contenant des instances de la classe Property
    #
    @staticmethod
    def properties_Process(bd_prod_config: str, format_chaine:str) -> list :

        # call createlastLoggedEventsFile
        createlastLoggedEventsFile()

        # call compare_Update_Data
        data_ObjectDates = Property.compare_Update_Data(bd_prod_config, format_chaine)

        # call update_createELS
        Property.update_createELS(data_ObjectDates)

        return [Property('', key, value) for key, value in data_ObjectDates.items()]
