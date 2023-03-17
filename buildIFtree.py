import requests
import re
import sys
#import time

session = requests.Session()

def pars_page ( address, level ):
    print(address, file=sys.stderr)
    #time.sleep(5)
    response = session.get(address)
    web_page = response.content.decode('windows-1252')
    address = re.sub("&pg=\d+$","",address)
    rows = web_page.split('\n')
    n_sp = 0
    next_page = 'none'
    for line in rows:
        #print(line)
        if line.startswith("<p></p><b>Name, Author, Year, (Current name), Parent taxon</b><p></p>"):
            sp_rows = line.split('<br>')
            for sp_line in sp_rows:
                if sp_line.startswith('<p>'):
                    #print(sp_line)
                    match = re.search("<a href='names.asp\?pg=\d+'>\[Next &gt;&gt;\]</a>",sp_line)
                    if match:
                        next_page = match.group()
                        next_page = next_page.lstrip("<a href='names.asp\?")
                        next_page = '&p' + next_page
                        next_page = next_page.rstrip("'>\[Next &gt;&gt;\]</a>")
                    sp_line = re.sub("<p>.*</p>","",sp_line)
                if sp_line.startswith("<a class='LinkColour4'"):
                    sp_line = re.sub("<a class='LinkColour4' href=GSDSpecies.asp\?RecordID=\d+ >",'',sp_line)
                    sp_line = re.sub("</a>[^<]+<a href='families.asp\?FamilyName=\w+'>\w+</a>",'',sp_line)
                    print("\t"*level+sp_line)
                    n_sp += 1
            if not next_page == 'none':
                n_sp += pars_page(address+next_page, level)
        elif re.search("<p><b>Pages: </b>.*<b>of \d+ records.</b></p><p></p><strong>\w+<br> in \w+ \w+", line):
            taxa_line = line.split('<br>')
            taxa_printed = False
            for taxa in taxa_line:
                if taxa.startswith(" in ") and not taxa_printed:
                    taxa = re.sub(" in \w+ ", "", taxa)
                    taxa = re.sub("</strong>", "", taxa)
                    taxa = re.sub(",$","", taxa)
                    print("\t"*level+taxa)
                    taxa_printed = True
                elif re.search("<a href='gsdquery.asp\?pg=\d+'>\[Next &gt;&gt;\]</a>",taxa):
                    match=re.search("<a href='gsdquery.asp\?pg=\d+'>\[Next &gt;&gt;\]</a>",taxa)
                    if match:
                        next_page = match.group()
                        next_page = next_page.lstrip("<a href='gsdquery.asp\?")
                        next_page = '&pg=' + next_page
                        next_page = next_page.rstrip("'>\[Next &gt;&gt;\]</a>")
                elif taxa.startswith("<a href="):
                    taxon_address = re.sub("<a href=","",taxa)
                    taxon_address = re.sub(" >[^<]+</a>","",taxon_address)
                    taxon_address = taxon_address.strip()
                    taxon_address = "http://www.speciesfungorum.org/GSD/" + taxon_address
                    n_sp += 1
                    pars_page(taxon_address, level+1)
            if not next_page == 'none':
                n_sp += pars_page(address+next_page, level)
        elif re.search("No records found", line):
            print("No records found", file=sys.stderr)
    print("\t"*level, n_sp, sep='')
    return n_sp 


#address = 'http://www.speciesfungorum.org/GSD/gsdquery.asp?RecordID=Boletales&Type=O'
address = 'http://www.speciesfungorum.org/GSD/gsdquery.asp?RecordID=Agaricales&Type=O'
pars_page(address, 0)

