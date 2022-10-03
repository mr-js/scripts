import os
import hashlib

def MD5Check(file):
    m = hashlib.md5()
    h = m.update(open(file, 'rb').read())
    return m.hexdigest()

def scan(target):
    table = [] # [name, type, path, md5]
    print('Scanning folder "{0}" ...'.format(target))
    for folder, subfolders, files in os.walk(target):
##        print('* Folder "{0}"'.format(folder))
        table.append([os.path.basename(folder), 'FOLDER', folder, ''])
##        print('** Subfolders "{0}"'.format(subfolders))
        for file in files:
##            print('*** File "{0}"'.format(file))
            table.append([file, 'FILE', os.path.join(folder, file), MD5Check(os.path.join(folder, file))])

##    print('--- Scanning result BEGIN ---')
##    for item in table:
##        print(item)
##    print('--- Scanning result END ---')
    return table

def analize(source, destination):
    print('Analizing "{0}" & "{1}" ...'.format(source[0][0], destination[0][0]))
    print('*** changes in file list: ***')
    src_names = set(item[0] for item in source[1:])
    dest_names = set(item[0] for item in destination[1:])
    diff_names = set.symmetric_difference(src_names, dest_names)
    if diff_names:
        for diff_name in diff_names:
            print(diff_name)
    else:
        print('<not detected>')
    print('*** changes in file content: ***')
    src_md5 = set(item[3] for item in source[1:])
    dest_md5 = set(item[3] for item in destination[1:])
    diff_md5 = set.symmetric_difference(src_md5, dest_md5)
    diff_names = set(item[0] for item in source[1:] if item[3] in diff_md5) | set(item[0] for item in destination[1:] if item[3] in diff_md5) - diff_names
    if diff_names:
        for diff_name in diff_names:
            print(diff_name)
    else:
        print('<not detected>')  

def compare():
    print('Source:')
    target = input()
    if target == '':
        target = 'source'
    src = scan(target)
    print('Destination:')
    target = input()
    if target == '':
        target = 'destination'
    dest = scan(target)
    analize(src, dest)

compare()
