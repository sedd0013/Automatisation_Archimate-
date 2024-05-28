
from imports import *
from Controller import Controller


def job() -> None:

    date_actuelle = datetime.datetime.now().strftime("%Y-%m-%d")
    format_chaine = '%Y-%m-%d %H:%M:%S'

    with open("Scripts/config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    path_file_archiExports = config['path_file_archiExports'] + f"/elements_{date_actuelle}.csv"
    path_gitlab_downloads = config['path_gitlab_downloads'] + f"/model_{date_actuelle}"

    variables = [
        'path_file_archiElemImports','path_file_archiPropImports',
        'path_file_events','bd_file_export','path_bd_exports',
        'file_prop','path_file_lastSeen','bd_prod_config',
        'bd_dev_config','git_config','smtp_server','smtp_port',
        'smtp_username','smtp_password','from_email','to_email'
    ]

    for var in variables:
        globals()[var] = config[var][0] if isinstance(config[var], list) else config[var]

    controller = Controller()
    controller.process(bd_prod_config, format_chaine, bd_dev_config, git_config, bd_file_export, path_bd_exports, path_file_archiExports, path_gitlab_downloads, path_file_events, date_actuelle,path_file_archiElemImports, file_prop, path_file_archiPropImports, path_file_lastSeen)
    controller.sendMail(smtp_server, smtp_port, smtp_username, smtp_password, from_email, to_email, date_actuelle)


job()

# schedule.every().hour.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)