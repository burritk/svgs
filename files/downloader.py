import urllib2
import os

class Downloader:
    def __init__(self):
        self.size = 0
        self.max_size = 9.5e+8
        # self.max_size = 3e+7
        print self.max_size
        self.folder_num = 0

    def next_folder(self):
        self.size = 0
        self.folder_num += 1
        print 'NEW FOLDER: ' + str(self.folder_num)

    def download_file(self,url,file_name):
        file_route = 'files/{}/'.format(self.folder_num)
        if not os.path.exists(file_route):
            os.makedirs(file_route)
        file_name = file_route + file_name + '.rar'
        # file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        self.size += file_size

        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        print 'TOTAL: ' + str(self.size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            # print status,

        if self.size >= self.max_size:
            self.next_folder()

        f.close()


def download_file(url, file_name):
    file_name = 'files/' + file_name + '.rar'
    # file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        # print status,

    f.close()