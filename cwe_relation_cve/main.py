"""
1. Pobierz wszystkie kody CWE, pobierz wszsytkie opisy słabości - ich id oraz opis, zapisz je do pliku json


"""
import json
import time
from datetime import datetime

from cwe_ids_saving import CWEIdsSaving
from cve_ids_saving import CVEIdsSaving
from cve_nist_scrapper import NISTCVEScraper


def save_all_cwe():
    """
    1. Grabs data from official mitre file "https://cwe.mitre.org/data/published/cwe_latest.pdf".
    2. Scrap description by cwe ids from  "https://cwe.mitre.org/"
    3. Saves data to json.file "cwe_all.json" 
    """
    pass
    # cwe_ids_saving = CWEIdsSaving()
    # cwe_ids_saving.save_to_file()


def save_all_cve_ids():
    """
    Zapisuje dane do pliku "cve_all.json" potrzebnego do funcji save_all_cve_ids_details
    """
    # cve_all_saving = CVEIdsSaving()
    # cve_all_saving.save_all_cve_ids_to_file()
    pass


def save_all_cve_ids_details():
    starting_time = time.perf_counter()

    with open("cve_all.json") as json_file:
        data = json.load(json_file)

    cve_all = data["cve_all"]

    # ilosc partów na które dzielę dane do plików
    PARTS = (len(cve_all) // 100) + 1

    for part in range(PARTS):
        result = []
        start_idx = part*100
        end_idx = (part+1) * 100

        for cve in cve_all[start_idx:end_idx]:
            cve_data = NISTCVEScraper(
                cve["cve_code"]).values  # dane ze scrapera
            cve_data.update({"year": cve["year"]})
            cve_data.update({"month": cve["month"]})
            result.append(cve_data)

        # zapisywanie danych w partycja po 100 ale ze wszystkimi szczegółami
        with open(f'all_cve/cve_all_details_{start_idx}_{end_idx}.json', 'w') as fp:
            json.dump(result, fp,  indent=4)

    performance = ending_time = time.perf_counter()
    print("PERFORMANCE: ",  performance)
    return performance


if __name__ == "__main__":
    # save_all_cwe()
    # save_all_cve_ids()
    save_all_cve_ids_details()
