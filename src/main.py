from manager import DataManager
from config.settings import ES_HOST,CSV_PATH,WEAPONS_FILE,INDEX_NAME

if __name__ == "__main__":
    manager = DataManager(
        csv_path = CSV_PATH,
        es_host = ES_HOST,
        index_name = INDEX_NAME,
        weapons_file = WEAPONS_FILE
    )
    manager.run()