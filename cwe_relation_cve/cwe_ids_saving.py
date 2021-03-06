import json
import time
from datetime import datetime

from cwe_ids_extractor import CWEIdsExtractor
from cwe_mitre_scrapper import CWEMitreScraper
from cwe_wrapper import CWEWrapper


class CWEIdsSaving:
    def __init__(self):
        self.__cwe_ids_extractor = CWEIdsExtractor()

    @property
    def cwe_db_timestamp(self):
        return self.__cwe_ids_extractor.creation_date

    @property
    def all_cwes_ids(self):
        return self.__cwe_ids_extractor.cwe_ids_set

    def get_data(self):
        result = []
        for cwe_id in self.all_cwes_ids:
            result.append(
                CWEWrapper(
                    cwe_id=cwe_id,
                    description=CWEMitreScraper(cwe_id).get_description()
                )
            )

        return result

    def save_to_file(self):
        starting_time = time.perf_counter()

        cwe_all = []
        for cwe in self.get_data():
            cwe_all.append(cwe.values)

        ending_time = time.perf_counter()

        result = {
            "created_at": str(datetime.now()),
            "timestamp": self.cwe_db_timestamp,
            "performance": ending_time - starting_time,
            "cwe_all": cwe_all
        }

        with open('cwe_all.json', 'w') as fp:
            json.dump(result, fp,  indent=4)
