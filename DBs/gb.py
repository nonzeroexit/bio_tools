#!/usr/bin/python3
import os
import sys
import time
import shlex
import subprocess
from tqdm import tqdm

class Download:
    def __init__(self, option):
        self.option = option

    def download(self, id_):
        match self.option:
            case 'genome':
                exit_code = os.system(f'efetch -db nuccore -id "{id_}" -format fasta > {id_}.genome')
            case 'proteome':
                exit_code = os.system(f'efetch -db nuccore -id "{id_}" -format fasta_cds_aa > {id_}.proteome')
            case 'orfeome':
                exit_code = os.system(f'efetch -db nuccore -id "{id_}" -format fasta_cds_na > {id_}.orfeome')
            case 'protein':
                exit_code = os.system(f'efetch -db protein -id "{id_}" -format fasta_cds_aa > {id_}.aa')
            case 'genbank':
                exit_code = os.system(f'efetch -db nuccore -id "{id_}" -format gb > {id_}.gb')

        return exit_code

def get_usr_input():
    if len(sys.argv) < 3 or sys.argv[1] not in ['genome', 'proteome', 'orfeome', 'protein', 'genbank', 'search']:
        print('usage:\n  gb genome/proteome/orfeome/protein/genbank/search ids/ids_file/query')
        sys.exit(0)
    usr_input = sys.argv[1:]
    return usr_input

def get_ids(usr_input):
    if os.path.isfile(usr_input[1]):
        with open(usr_input[1], 'r', encoding='utf-8') as f_handle:
            return [line.strip() for line in f_handle if line.strip()]
    return usr_input[1:]

def main():
    usr_input = get_usr_input()
    option = usr_input[0]

    if option == 'search':
        cmd = shlex.split(f'firefox https://www.ncbi.nlm.nih.gov/nuccore/?term={("+").join(usr_input[1:])}')
        p = subprocess.Popen(cmd, start_new_session=True)
    else:
        download = Download(option)
        ids = get_ids(usr_input)
        waiting_time = 2
        for id_ in tqdm(ids):
            while True:
                exit_code = download.download(id_)
                time.sleep(waiting_time)
                if exit_code == 0:
                    break
                waiting_time *= 2

if __name__ == '__main__':
    main()
