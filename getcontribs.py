from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timezone
import requests, sys, time

totalcontribs = {}

# List of modes:
# num: number of edits
# abt: number of bytes (absolute value)
# sbt: number of bytes (signed value)

display = 50
final = 0

othernumbers = ['०০੦૦೦༠',
                '१১੧૧೧༡',
                '२২੨૨೨༢',
                '३৩੩૩೩༣',
                '४৪੪૪೪༤',
                '५৫੫૫೫༥',
                '६৬੬૬೬༦',
                '७৭੭૭೭༧',
                '८৮੮૮೮༨',
                '९৯੯૯೯༩']

othervalues = {'commons':['commons', 'wikimedia'],
               'incubator':['incubator', 'wikimedia'],
               'mediawiki':['www', 'mediawiki'],
               'meta':['meta', 'wikimedia'],
               'species':['species', 'wikimedia'],
               'wikidata':['www', 'wikidata']}

def readUser():
    file = open('userdata.txt', 'r')
    username = file.readline()
    username = username[:len(username) - 1]
    st = file.readline()
    st = st[:len(st) - 1] + '+00:00'
    et = file.readline()
    et = et[:len(et) - 1] + '+00:00'
    sdate = datetime.fromisoformat(st)
    edate = datetime.fromisoformat(et)
    langlist = file.readline().split(', ')
    if langlist[len(langlist) - 1][len(langlist[len(langlist) - 1]) - 1] == '\n':
        langlist[len(langlist) - 1] = langlist[len(langlist) - 1][:len(langlist[len(langlist) - 1]) - 1]
    wikilist = file.readline().split(', ')
    if wikilist[len(wikilist) - 1][len(wikilist[len(wikilist) - 1]) - 1] == '\n':
        wikilist[len(wikilist) - 1] = wikilist[len(wikilist) - 1][:len(wikilist[len(wikilist) - 1]) - 1]
    wikilist2 = file.readline().split(', ')
    if wikilist2[len(wikilist2) - 1][len(wikilist2[len(wikilist2) - 1]) - 1] == '\n':
        wikilist2[len(wikilist2) - 1] = wikilist2[len(wikilist2) - 1][:len(wikilist2[len(wikilist2) - 1]) - 1]
    file.close()
    return [username, sdate, edate, langlist, wikilist, wikilist2]

def getOneWiki(mode, lang, wiki, offset, mindate, maxdate, oldid):
    global ud
    global display
    final = 0
    webpage = BeautifulSoup(get('https://'+lang+'.'+wiki+'.org/w/index.php?title=Special:Contributions/' + ud[0] + '&offset=' + offset + '&limit='+str(display)+'&target=' + ud[0]).content, 'html.parser')
    try:
        nli = webpage.find('a', {'class':'mw-nextlink'})['href']
        pos = 19
        while nli[pos:pos + len(ud[0]) + 1] != '/' + ud[0]:
            pos += 1
        npo = nli[len(ud[0])*2+pos+17:len(ud[0])*2+pos+31]
    except TypeError:
        npo = ''
    listof_meta = webpage.find_all('ul', {'class':'mw-contributions-list'})
    if len(listof_meta) == 0:
        return 0
    if oldid == '':
        try:
            webpage_o = BeautifulSoup(get('https://'+lang+'.'+wiki+'.org/w/index.php?title=Special:Contributions/' + ud[0] + '&offset=' + sd.strftime('%Y%m%d%H%M%S') + '&limit=1&target=' + ud[0]).content, 'html.parser')
            oldid = webpage_o.find('ul', {'class':'mw-contributions-list'}).find('li')['data-mw-revid']
        except AttributeError:
            pass
    listof = []
    for ul in listof_meta:
        for li in ul.find_all('li'):
            listof.append(li)
    surpassed = False
    for a in listof:
        if a['data-mw-revid'] == oldid:
            surpassed = True
            break
        if mode == 'num':
            final += 1
        elif mode == 'abt':
            nb = a.find('span', {'class': 'mw-plusminus-pos mw-diff-bytes'})
            if nb == None:
                nb = a.find('span', {'class': 'mw-plusminus-neg mw-diff-bytes'})
                if nb == None:
                    nb = a.find('span', {'class': 'mw-plusminus-null mw-diff-bytes'})
                    if nb == None:
                        nb = a.find('strong', {'class': 'mw-plusminus-pos mw-diff-bytes'})
                        if nb == None:
                            nb = a.find('strong', {'class': 'mw-plusminus-neg mw-diff-bytes'})
            fstr1 = nb.getText()
            if fstr1 == '0':
                continue
            fstr1 = fstr1[1:]
            mp = 0
            while mp < len(fstr1):
                nos = 0
                while nos < 10:
                    if fstr1[mp] in othernumbers[nos]:
                        try:
                            fstr1 = datetext[:mp] + str(nos) + fstr1[mp + 1:]
                        except ValueError:
                            fstr1 = datetext[:mp] + str(nos)
                        break
                    nos += 1
                mp += 1
            fstr = ''
            for g in fstr1:
                if g in '0123456789':
                    fstr += g
            final += int(fstr)
        elif mode == 'sbt':
            nb = a.find('span', {'class': 'mw-plusminus-pos mw-diff-bytes'})
            if nb == None:
                nb = a.find('span', {'class': 'mw-plusminus-neg mw-diff-bytes'})
                if nb == None:
                    nb = a.find('span', {'class': 'mw-plusminus-null mw-diff-bytes'})
                    if nb == None:
                        nb = a.find('strong', {'class': 'mw-plusminus-pos mw-diff-bytes'})
                        if nb == None:
                            nb = a.find('strong', {'class': 'mw-plusminus-neg mw-diff-bytes'})
            fstr1 = nb.getText()
            if fstr1 == '0':
                continue
            mp = 0
            while mp < len(fstr1):
                nos = 0
                while nos < 10:
                    if fstr1[mp] in othernumbers[nos]:
                        try:
                            fstr1 = datetext[:mp] + str(nos) + fstr1[mp + 1:]
                        except ValueError:
                            fstr1 = datetext[:mp] + str(nos)
                        break
                    nos += 1
                mp += 1
            fstr = ''
            for g in fstr1:
                if g == '−':
                    fstr += '-'
                elif g in '+0123456789':
                    fstr += g
            final += int(fstr)
    if offset == ud[2].strftime('%Y%m%d%H%M%S') and npo != '':
        listdate = datetime.strptime(npo + '+0000', '%Y%m%d%H%M%S%z')
        firstpage = ud[2] - listdate
        tlen = ud[2] - ud[1]
        if firstpage * 10 < tlen:
            display = 500
        elif firstpage * 4 < tlen:
            display = 200
        elif firstpage * 2 < tlen:
            display = 100
    if npo != '' and not surpassed:
        final += getOneWiki(mode, lang, wiki, npo, mindate, maxdate, oldid)
    return final

start_time = time.time()
mode = sys.argv[1]
ud = readUser()
sd = ud[1]
ed = ud[2]
mxdstr = ed.strftime('%Y%m%d%H%M%S')
for b in ud[3]:
    for a in ud[4]:
        display = 50
        try:
            f = getOneWiki(mode, b, a, mxdstr, sd, ed, '')
            if f != 0:
                try:
                    totalcontribs[a][b] = f
                except KeyError:
                    totalcontribs[a] = {}
                    totalcontribs[a][b] = f
                final += f
        except requests.exceptions.ConnectionError:
            print('Bad connection:', b, a)
            continue
        except AttributeError:
            continue
        except ValueError:
            print(b, a, 'ValueError')
totalcontribs['other'] = {}
for ow in ud[5]:
    display = 50
    if '.' in ow:
        dotow = ow.split('.')
        try:
            f = getOneWiki(mode, dotow[0], dotow[1], mxdstr, sd, ed, '')
            if f != 0:
                try:
                    totalcontribs[dotow[1]][dotow[0]] = f
                except KeyError:
                    totalcontribs[dotow[1]] = {}
                    totalcontribs[dotow[1]][dotow[0]] = f
            final += f
        except requests.exceptions.ConnectionError:
            print('Bad connection:', dotow[1], dotow[0])
        except AttributeError:
            pass
    else:
        try:
            f = getOneWiki(mode, othervalues[ow][0], othervalues[ow][1], mxdstr, sd, ed, '')
            if f != 0:
                totalcontribs['other'][ow] = f
            final += f
        except requests.exceptions.ConnectionError:
            print('Bad connection:', ow)
        except AttributeError:
            pass
    numdigits = len(str(final))
if mode == 'sbt':
    maxabs = 0
    for a in totalcontribs:
        for b in totalcontribs[a]:
            if abs(totalcontribs[a][b]) > maxabs:
                maxabs = abs(totalcontribs[a][b])
    if abs(final) > maxabs:
        maxabs = abs(final)
    for a in totalcontribs:
        for b in totalcontribs[a]:
            numstr = str(abs(totalcontribs[a][b]))
            while len(numstr) < len(str(maxabs)):
                numstr = ' ' + numstr
            if totalcontribs[a][b] < 0:
                numstr = '-' + numstr
            elif totalcontribs[a][b] > 0:
                numstr = '+' + numstr
            if a == 'other':
                if len(b) < 8:
                    print('', b + '\t', numstr, sep = '\t')
                else:
                    print('', b, numstr, sep = '\t')
            else:
                print(b, a, numstr, sep = '\t')
    finalstr = str(final)
    while len(finalstr) < len(str(maxabs)):
        finalstr = ' ' + finalstr
    if final < 0:
        finalstr = '-' + finalstr
    elif final > 0:
        finalstr = '+' + finalstr
    else:
        finalstr = ' ' + finalstr
    print('\t', '', finalstr, sep='\t')
else:
    for a in totalcontribs:
        for b in totalcontribs[a]:
            numstr = str(totalcontribs[a][b])
            while len(numstr) < numdigits:
                numstr = ' ' + numstr
            if a == 'other':
                if len(b) < 8:
                    print('', b + '\t', numstr, sep = '\t')
                else:
                    print('', b, numstr, sep = '\t')
            else:
                print(b, a, numstr, sep = '\t')
    print('\t', '', final, sep='\t')
print("--- %s s ---" % (round(time.time() - start_time, 3)))
