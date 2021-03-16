import requests

def downloader():
    list_of_files = str(requests.get('https://10.32.223.253/ept/all_ept_read.php', verify = False).content)
    last_filename = list_of_files[list_of_files.find('EPT_ATT_'):list_of_files.find('.zip')]

    ept_file = requests.get('https://10.32.223.253/ept/download.php?archivo=' + last_filename + '.zip', verify = False)

    with open(last_filename + '.zip', 'wb') as f:
        f.write(ept_file.content) 
        return last_filename

if __name__ == "__main__":
    downloader()