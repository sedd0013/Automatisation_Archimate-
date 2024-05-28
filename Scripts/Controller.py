
from imports import *
from Element import Element
from Property import Property


class Controller:


    # ______________ Constructeur de la classe 'Controller' ______________
    #
    # Initialise un nouvel objet de la classe 'Controller' (Aucun paramètres n'est attendu).
    #
    # @return : None
    #
    def __init__(self) -> None:
        pass


    # ______________ Mise en place du projet et récupération des données ______________
    #
    # @return : None
    #
    @staticmethod
    def create_folders(bd_prod_config: str, format_chaine:str, bd_dev_config: dict, git_config: dict, bd_file_export: str, path_bd_export: str, path_file_archiExports: str, path_gitlab_downloads: str, path_file_events: str, date_actuelle, path_file_lastSeen) -> None:

        for i in ["Archimate_Exports", "Archimate_Imports", "Data_BD_Exports", "GitLab_Exports"]:
            if not os.path.exists(i):
                os.makedirs(i)

        global data_ObjectDates
        global dict_bd_export
        
        # call properties_Process from class Property
        data_ObjectDates = Property.properties_Process(bd_prod_config, format_chaine)

        # Call elements_Process from class Element
        dict_bd_export = Element.elements_Process(bd_prod_config, bd_dev_config, git_config, bd_file_export, path_bd_export, path_file_archiExports, path_gitlab_downloads, path_file_events, date_actuelle, path_file_lastSeen)

    
    # ______________ Génération du fichier d'import elements.csv ______________
    #
    #
    # @param path_file_archiElemImports (str): Chemin d'acces au fichier d'import elements.csv pour ArchiMate
    # @param path_file_archiExports (str)    : Chemin vers le fichier de données .csv crée a partir des données ArchiMate
    # @param path_bd_export  (str)           : Chemin vers le fichier .csv contenant les données de la BD.
    #
    # @return : None
    #
    @staticmethod
    def create_import_file(path_file_archiElemImports: str, path_file_archiExports: str, path_bd_export: str) -> None:
    
        #Call create_dict_Archi 
        dict_data_archi = Element.create_dict_Archi(path_file_archiExports, path_bd_export)

        res_list = []

        for element in dict_bd_export:

            if element.name not in [el.name for el in dict_data_archi]:
                res_list.append(element)
                
        print("\n\nlen data_bd :", len(dict_bd_export), " --- ", "len data_Archi",len(dict_data_archi))
        print("Elements existants en BD et NON dans Archimate : ", len(res_list))

        value = 1
        if(len(dict_data_archi) > 0):
            value = len(dict_data_archi)

        print("Rajout de : ", round((len(res_list) / value)*100, 2), "%\n")

        try:
            with open(path_file_archiElemImports, 'w', newline='') as import_csv:
                writer = csv.writer(import_csv, delimiter=',')
                writer.writerow(["ID","Type","Name","Documentation","Specialization"])  

                for element in res_list:
                    writer.writerow([element.id, element.type, element.name, "", ""])
        
        except csv.Error as e:
            print(f"Erreur lors de l'écriture dans le fichier CSV {path_file_archiElemImports} : {e}")

    
    # ______________ Création diu fichier d'import properties.csv ______________
    #
    #
    # @param path_gitlab_downloads (str)     : Chemin vers le dossier contenant les données. 
    # @param file_prop (str)                 : nom du fichier properties.csv
    # @param path_file_archiPropImports (str): Chemin d'acces au fichier d'import properties.csv pour ArchiMate
    # @param format_chaine (str)             : Format de la date a appliquer
    #
    # @return : None
    #
    @staticmethod
    def createPropertiesFile(path_gitlab_downloads: str, file_prop: str, path_file_archiPropImports: str, format_chaine: str) -> None:
        try:
            with open(path_file_archiPropImports, "w", newline='') as properties:
                writer = csv.writer(properties, delimiter=",")
                writer.writerow(["ID","Key","Value"]) 

                for dossier in os.listdir(path_gitlab_downloads):
                    path_dossier_child = os.path.join(path_gitlab_downloads, dossier)

                    xmlFolderFile = os.path.join(path_dossier_child, "folder.xml")

                    try:
                        if(minidom.parse(xmlFolderFile).getElementsByTagName("archimate:Folder")[0].getAttribute("name")=="Events"):

                            for fichier in os.listdir(path_dossier_child):
                                if fichier != "folder.xml":
                                    f = minidom.parse(os.path.join(path_dossier_child, fichier))
                                    objectNature = f.getElementsByTagName("archimate:ApplicationEvent")

                                    if objectNature:
                                        objectName = objectNature[0].getAttribute("name").lower()
                                        objectId = objectNature[0].getAttribute("id")

                                        objectProperties = objectNature[0].getElementsByTagName("properties")
                                        
                                        res = next((prop for prop in data_ObjectDates if prop.key == objectName), None)
                                    
                                        if(objectProperties):
                                            objectProperties = objectProperties[0]

                                            print(objectName ,"----- : ",objectProperties)

                                            if res is not None:

                                                try :
                                                    if objectProperties.hasAttribute("lastLogged"):
                                                        value = objectProperties.getAttribute('lastLogged')
                                                        
                                                        if res.value > datetime.datetime.strptime(value, format_chaine):
                                                            writer.writerow([objectId, "lastLogged", res.value])
                                                    else:
                                                        writer.writerow([objectId, "lastLogged", res.value])

                                                except ValueError as ve:
                                                    print(f"Erreur lors de la conversion de la date : {ve}")
                                            else:
                                                writer.writerow([objectId, "lastLogged", res.value])
                                        else :
                                            if res is not None :
                                                writer.writerow([objectId, "lastLogged", res.value])
                                            else :
                                                print(f"{objectName} : Aucun élément de ce nom en base de données !")
                                    else:
                                        print("Aucun élément 'archimate:ApplicationEvent' trouvé dans le fichier", fichier)
                    except IndexError:
                        print("Erreur : L'index n'a pas été trouvé dans le fichier XML.")
                        
            print(f"\nÉcriture dans le fichier '{file_prop}' terminée.\n")
        
        except FileNotFoundError:
            print("Erreur : Le fichier de propriétés n'a pas été trouvé.")
        except PermissionError:
            print("Erreur : Permission refusée pour écrire dans le fichier de propriétés.")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

    
    # ______________ Envoi de mail automatique à l'adresse spécifiée ______________
    #
    #
    # @param smtp_server (str)  : Serveur SMTP. 
    # @param smtp_port (int)    : port du serveur SMTP 
    # @param smtp_username (str): nom d'utilisateur SMTP
    # param smtp_password (str) : mot de passe SMTP
    # @param from_email (str)   : email de l'expéditeur
    # @param to_email (str)     : email du destinataire
    #
    # @return : None
    #
    def sendMail(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str, from_email: str, to_email: str, date_actuelle) -> None:

        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = 'Import Archimate, fichiers prêts !'

        body = """\
            <html>
            <body>
                <p>Bonjour,</p>
                <p>Nous avons ajouté de nouveaux documents à importer dans Archimate. Veuillez prendre les mesures nécessaires pour les importer dès que possible.</p>
                <p>Cordialement,<br>L'équipe data intégration</p>

                <br><br>
                <hr>
                <br><br>

                <p>Hello,</p>
                <p>We have added new documents to import into Archimate. Please take necessary actions to import them as soon as possible.</p>
                <p>Best regards,<br>Data integration team.</p>
            </body>
            </html>
        """

        message.attach(MIMEText(body, "html"))

        path = './Archimate_Imports'
        zip_file = 'ImportArchi_'+date_actuelle+'.zip'
        path_zip = f'{path}/{zip_file}'
        files = [f for f in os.listdir(path) if os.path.isfile(join(path, f)) and f.endswith('.csv')]


        with zipfile.ZipFile(path_zip, 'w') as zipf:
            for csv_file in files:
                csv_file_path = os.path.join(path, csv_file)
                zipf.write(csv_file_path, os.path.basename(csv_file))
                

        with open(path_zip, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {zip_file}'
        )
        message.attach(part)


        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Activer le chiffrement TLS
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, message.as_string())

            print("Email envoyé avec succès!")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")

        finally:
            server.quit()


    # ______________ Lancement de tous les processus ______________
    #
    # @return : None
    #
    def process(self, bd_prod_config: dict, format_chaine:str, bd_dev_config: dict, git_config: dict, bd_file_export: str, path_bd_exports: str, path_file_archiExports: str, path_gitlab_downloads: str, path_file_events: str, date_actuelle,path_file_archiElemImports, file_prop, path_file_archiPropImports, path_file_lastSeen) -> None:

        Controller.create_folders(bd_prod_config, format_chaine, bd_dev_config, git_config, bd_file_export, path_bd_exports, path_file_archiExports, path_gitlab_downloads, path_file_events, date_actuelle, path_file_lastSeen)
        Controller.create_import_file(path_file_archiElemImports, path_file_archiExports, path_bd_exports)
        Controller.createPropertiesFile(path_gitlab_downloads, file_prop, path_file_archiPropImports, format_chaine)
