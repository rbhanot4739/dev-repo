import argparse
import time
import zipfile
from multiprocessing import Process, Queue, current_process

parser = argparse.ArgumentParser(
    description=(
        "Unzips a password protected .zip by performing a "
        "brute-force attack using either a word list, password list or a"
        "dictionary."),
    usage="BruteZIP.py -z zip.zip -f file.txt")
parser.add_argument(
    "-z",
    "--zip",
    metavar="",
    # required=True,
    help="Location and the name of the .zip file.")  # Creates -z arg
parser.add_argument(
    "-f",
    "--file",
    metavar="",
    # required=True,
    help="Location and the name of the word list/password list/dictionary."
)  # Creates -f arg
args = parser.parse_args()


def extract_zip(zip_file, q):
    while True:
        pswd = q.get()
        if pswd is None:
            # print(count, current_process().name)
            return
        else:
            try:
                zip_file.extractall(pwd=pswd)
                print(
                    f'Password  is {pswd} - found by {current_process().name}')
            except Exception:
                pass


def main(inp_zip, file):
    if (inp_zip is None) | (file is None):
        print(
            parser.usage
        )  # If the args are not used, it displays how to use them to the user.
        exit(0)
    zip_file = zipfile.ZipFile(inp_zip, "r")
    q = Queue()
    with open(file) as ifile:
        for line in ifile:
            q.put(bytes(line.strip(), 'utf-8'))
    procs = []
    for _ in range(4):
        q.put(None)
        p = Process(
            target=extract_zip, args=(
                zip_file,
                q,
            ))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()


if __name__ == '__main__':
    t = time.time()
    main(args.zip, args.file)  # BruteZIP.py -z zip.zip -f file.txt
    print(time.time() - t)
