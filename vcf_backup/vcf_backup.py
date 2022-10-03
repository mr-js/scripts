import quopri
import codecs
import re


class VcfBackup:
    cards = []
    total = 0    
    
    def load(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            filedata = quopri.decodestring(f.read().encode('utf-8')).decode('utf-8', errors='ignore')
            pattern = re.compile(r'(BEGIN:VCARD)(.*?)(END:VCARD)', re.MULTILINE | re.DOTALL)
            for item in pattern.findall(filedata):
                self.cards.append(self.VcfCard(item))
            self.total = len(self.cards)
            print('records: {}'.format(self.total))

    def view(self):
        for i in range(self.total):
            print('{0:*<32}'.format(i+1))
            print(self.cards[i].format())

    def backup(self, filename):
        with codecs.open(filename, 'w', 'utf-8') as f:
            for i in range(self.total):
                f.write('{0:*<32}\r\n'.format(i+1))
                f.write(self.cards[i].format())

    class VcfCard:
        raw = ''
        name = ''
        tels = []

        def __init__(self, raw):
            self.raw = str(raw)
            pattern = re.compile(r'(?:FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:)(.*?)(?:\\r\\n)', re.MULTILINE | re.DOTALL)
            try:
                self.name = pattern.findall(self.raw)[0]
            except:
                self.name = 'ERROR'
            pattern = re.compile(r'(?:.*?)(?:TEL;.*?:)(.*?)(?:\\r\\n)', re.MULTILINE | re.DOTALL)            
            try:
                self.tels = pattern.findall(self.raw)
            except:
                self.tels = ['ERROR']
            

        def format(self):
            record = '{}\r\n'.format(self.name)
            for tel in self.tels:
                record += '{}\r\n'.format(tel)
            return record


vcf = VcfBackup()
vcf.load('input.vcf')
vcf.view()
vcf.backup('output.txt')
