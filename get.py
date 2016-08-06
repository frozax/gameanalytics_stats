import os

file_with_raw_links = "../../dl.txt.txt"
for line in open(file_with_raw_links).readlines():
    line = line.strip()
    dest_name = line.split('/')[-1].split('?')[0]
    cmd_curl = "curl -o %s \"%s\"" % (dest_name, line)
    cmd_wget = "wget -O %s \"%s\"" % (dest_name, line)
    os.system(cmd_wget)
    os.system("gunzip %s" % dest_name)
    break


