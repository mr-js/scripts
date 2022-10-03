## obfuscate files:
##
## IMG_64790832_02.JPG -> GPFA5JYM.jpg
## MyBirthday_2008.mp4 -> CT6LQSFG.mp4
## AllPasswords_01.doc -> S6P45UHJ.doc
##
## all files names in folder (subfolders) are obfuscated
## save file names sorting order by fist letters (option)
## all files extentions are converted to lowercase (force)
## folder (subfolders) names are NOT obfuscated
## all changes are applied immediately

import os
import random
import string
import hashlib

bits = 8
    
def obfuscate(path, save_order = True, write_changes = True):
    for path, folders, files in os.walk(path):
        files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or -1))
        index = 0
        total = len(files)
        if total > 10 ** bits:
            print('PASSED: low bits for a lot of files')
            continue
        else:
            print(f'{path} files total: {total}')
        for file in files:
            name, ext = os.path.splitext(os.path.join(path, file))
            if not save_order:
                mask = string.digits + string.ascii_uppercase
                target = ''.join(random.choice(mask) for i in range(bits)) + str(ext).lower()
            else:
                mask = string.ascii_uppercase
                prefix_width = len(str(total))
                target = f'{index:0{prefix_width}d}' + ''.join(random.choice(mask) for i in range(bits-prefix_width)) + str(ext).lower()
            print(f'{file[:24]:<24} -> {target}')
            if write_changes:
                os.rename(os.path.join(path, file), os.path.join(path, target))
            index += 1
    return 0

def check_dublicates(path):
    dublicate_counter = 0
    files = []
    for path, folders, files in os.walk(path):
        files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or -1))
    digests = dict()
    for file in files:
        with open(os.path.join(path, file), 'rb') as f:
            digest = hashlib.md5(f.read()).hexdigest()
            if digest in digests.values():
                print(f'{file} == {[k for k, v in digests.items() if v == digest][0]}')
                dublicate_counter += 1
            digests[file] = digest
    return dublicate_counter
    

path = input('Input Path and press Enter to continue...\n')
##path = r'C:\Test\files'
if check_dublicates(path) == 0:
    obfuscate(path, save_order = True, write_changes = False)
