
# ______________ Import des bibliothéques ______________

import csv
from os import path
import datetime 

print("Bibliothèques importées avec succés [createELS.py]")

# ______________ Création du fichier de base des events avec dates ______________

def createlastLoggedEventsFile() -> None:

    file_name = 'EventsLastSeenDates.csv'
    path_file = f"Data_BD_Exports/{file_name}"

    if(not path.exists(path_file)):

        # data de base : data = {'posm_contracts': '2024-04-01 15:08:23','private_order': '2022-05-05 02:39:06','tiers': '2024-03-28 10:59:37','visits': '2024-04-02 08:05:18','loyalty_accounts': '2024-04-02 08:04:55','prices_conditions': '2024-04-02 07:28:02','sales_orders': '2024-04-02 07:55:44','comptes_rendus_pec': '2024-04-02 05:49:45','employees': '2024-04-02 00:13:06','loyalty_point_movements': '2024-04-02 08:04:56','sales': '2024-04-02 07:34:39','email_results': '2022-10-05 13:30:41','business_partners': '2024-04-02 07:18:55','echantillons': '2024-04-02 08:11:46','results': '2023-09-28 04:29:57','avancements_mec': '2024-03-29 18:25:35','goods_movements': '2024-04-02 08:13:08','loyalty_offers': '2024-03-11 16:20:21','cases': '2024-04-02 07:49:19','contacts': '2024-04-02 08:15:06','products': '2024-04-02 08:01:41','contracts': '2024-04-02 08:02:55','oaders': '2022-06-20 08:55:30','deliveries': '2024-02-29 14:08:58','returns': '2024-04-02 06:23:18','inventaires': '2024-04-02 04:00:49','achats_echantillons': '2024-04-02 07:36:34','optouts': '2024-04-02 07:49:29','loyalty_maxxing_offers': '2024-03-11 16:19:24','comptes_rendus_mec': '2024-03-29 18:37:11','sales_invoices': '2024-04-02 08:06:02','customers': '2024-04-02 07:33:18','2': '2022-10-19 13:47:03','events': '2024-04-01 12:12:53','email_messages': '2024-04-02 07:49:27','private_orders': '2024-04-02 01:26:10','loyalty_receipts': '2024-04-02 07:58:21','production_orders': '2024-04-02 08:13:14','private_accounts': '2024-04-01 22:17:59','vendors': '2024-04-02 08:03:35','citerne': '2024-04-02 07:46:39','touchpoints': '2023-06-22 09:56:54','purchases_invoices': '2024-04-02 08:08:08','ordres_fabrication': '2024-04-02 07:13:02','orders': '2024-04-02 08:14:31','loyalty_cards': '2024-04-02 07:28:51','production_orders_instructions': '2024-04-02 08:13:28','posm_orders_trackings': '2024-04-01 22:26:49','attributions_mec': '2024-03-29 16:19:18','prices_zcond_a04': '2024-04-01 10:02:32','quality_inspection_lots': '2024-04-02 08:13:38','loyalty_customers': '2024-04-02 07:38:22','avancements_pec': '2024-04-02 08:12:21','Tiers': '2024-04-02 07:57:37','sales_deliveries': '2024-04-02 08:14:53','global_trade_item_numbers': '2024-03-27 22:30:23','projects': '2024-04-01 16:09:03','order': '2022-07-14 07:49:41','loyalty_containers': '2023-11-08 09:19:33'}
        
        # for  key, value in data.items():
        #     if isinstance(value, datetime.datetime):
        #         data_LastViewdDates[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        # print(data_LastViewdDates)

        data_LastViewdDates = {'posm_contracts': datetime.datetime(2024, 4, 22, 12, 4, 33), 'private_order': datetime.datetime(2022, 5, 5, 2, 39, 6), 'tiers': datetime.datetime(2024, 4, 4, 18, 12, 1), 'visits': datetime.datetime(2024, 4, 22, 16, 25, 22), 'loyalty_accounts': datetime.datetime(2024, 4, 22, 16, 22, 24), 'prices_conditions': datetime.datetime(2024, 4, 22, 16, 26, 31), 'sales_orders': datetime.datetime(2024, 4, 22, 16, 25, 33), 'comptes_rendus_pec': datetime.datetime(2024, 4, 22, 15, 44, 55), 'employees': datetime.datetime(2024, 4, 22, 2, 5, 37), 'loyalty_point_movements': datetime.datetime(2024, 4, 22, 16, 29, 5), 'sales': datetime.datetime(2024, 4, 22, 15, 35, 26), 'email_results': datetime.datetime(2022, 10, 5, 13, 30, 41), 'business_partners': datetime.datetime(2024, 4, 22, 11, 11, 13), 'echantillons': datetime.datetime(2024, 4, 22, 16, 24, 19), 'results': datetime.datetime(2023, 9, 28, 4, 29, 57), 'avancements_mec': datetime.datetime(2024, 4, 22, 10, 29, 35), 'goods_movements': datetime.datetime(2024, 4, 22, 16, 28, 13), 'loyalty_offers': datetime.datetime(2024, 3, 11, 16, 20, 21), 'cases': datetime.datetime(2024, 4, 22, 16, 24, 46), 'contacts': datetime.datetime(2024, 4, 22, 16, 29, 6), 'products': datetime.datetime(2024, 4, 22, 16, 11, 22), 'contracts': datetime.datetime(2024, 4, 22, 16, 13, 31), 'oaders': datetime.datetime(2022, 6, 20, 8, 55, 30), 'deliveries': datetime.datetime(2024, 2, 29, 14, 8, 58), 'returns': datetime.datetime(2024, 4, 22, 16, 10, 49), 'inventaires': datetime.datetime(2024, 4, 22, 13, 18, 6), 'achats_echantillons': datetime.datetime(2024, 4, 22, 16, 29, 6), 'optouts': datetime.datetime(2024, 4, 22, 16, 25, 28), 'loyalty_maxxing_offers': datetime.datetime(2024, 3, 11, 16, 19, 24), 'comptes_rendus_mec': datetime.datetime(2024, 4, 22, 7, 4, 27), 'sales_invoices': datetime.datetime(2024, 4, 22, 16, 14, 28), 'customers': datetime.datetime(2024, 4, 22, 16, 10, 19), '2': datetime.datetime(2022, 10, 19, 13, 47, 3), 'events': datetime.datetime(2024, 4, 5, 15, 49, 31), 'email_messages': datetime.datetime(2024, 4, 22, 16, 25, 24), 'private_orders': datetime.datetime(2024, 4, 22, 15, 46, 40), 'loyalty_receipts': datetime.datetime(2024, 4, 22, 16, 29, 6), 'production_orders': datetime.datetime(2024, 4, 22, 16, 15, 48), 'private_accounts': datetime.datetime(2024, 4, 20, 1, 57, 53), 'vendors': datetime.datetime(2024, 4, 22, 16, 13, 40), 'citerne': datetime.datetime(2024, 4, 3, 9, 59, 14), 'touchpoints': datetime.datetime(2023, 6, 22, 9, 56, 54), 'purchases_invoices': datetime.datetime(2024, 4, 22, 16, 21, 41), 'ordres_fabrication': datetime.datetime(2024, 4, 22, 16, 17, 18), 'orders': datetime.datetime(2024, 4, 22, 16, 28, 12), 'loyalty_cards': datetime.datetime(2024, 4, 22, 15, 48, 50), 'production_orders_instructions': datetime.datetime(2024, 4, 22, 16, 28, 45), 'posm_orders_trackings': datetime.datetime(2024, 4, 22, 12, 3, 48), 'attributions_mec': datetime.datetime(2024, 4, 22, 11, 40, 3), 'prices_zcond_a04': datetime.datetime(2024, 4, 19, 17, 1, 56), 'quality_inspection_lots': datetime.datetime(2024, 4, 22, 16, 23, 23), 'loyalty_customers': datetime.datetime(2024, 4, 22, 16, 22, 24), 'avancements_pec': datetime.datetime(2024, 4, 22, 15, 44, 54), 'Tiers': datetime.datetime(2024, 4, 22, 15, 43, 23), 'sales_deliveries': datetime.datetime(2024, 4, 22, 16, 27, 19), 'global_trade_item_numbers': datetime.datetime(2024, 4, 19, 23, 30, 3), 'projects': datetime.datetime(2024, 4, 22, 9, 21, 4), 'order': datetime.datetime(2022, 7, 14, 12, 49, 40), 'loyalty_containers': datetime.datetime(2023, 11, 8, 9, 19, 33), 'loyalty_run_promos': datetime.datetime(2024, 4, 4, 3, 1, 48)}

        try:
            with open(path_file, "w", newline='') as file:

                writer = csv.writer(file, delimiter=',')
                writer.writerow(['OBJECT','MAX_TIMESTAMP'])

                for i in data_LastViewdDates:
                    row = [i, data_LastViewdDates[i]]
                    writer.writerow(row)

            print(f"fichier {file_name} crée avec succés")
        
        except csv.Error as e:
            print(f"Erreur lors de l'écriture dans le fichier CSV : {e}")
    
    print(f"Exécution du fichier 'createELS.py' terminée")

