import zipfile
from ept_to_sql import parser
from get_ept import downloader


def ericsson_data():
    filename = downloader()
    with zipfile.ZipFile('EPT_ATT_UMTS_LTE_2021-03-12.zip', 'r') as zip_ref:
        zip_ref.extractall('EPT')
        parser('EPT/' + filename +'.xlsx')

if __name__ == "__main__":
    ericsson_data()