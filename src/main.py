from manager import DataManager
from config.settings import ES_HOST

if __name__ == "__main__":
    manager = DataManager(
        csv_path="../data_files/tweets_injected 3.csv",
        es_host=ES_HOST,
        index_name="tweets_index",
        weapons_file="../data_files/weapon_list.txt"
    )
    manager.run()