from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timezone
import requests, sys, time, csv

totalcontribs = {}

# List of modes:
# num: number of edits
# abt: number of bytes (absolute value)
# sbt: number of bytes (signed value)

display = 100 # Change this
final = 0

othernumbers = ['༠', '༡', '༢', '༣', '༤', '༥', '༦', '༧', '༨', '༩']

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

def readDateFormat():
    file = open('dates.csv')
    lesari = csv.reader(file, delimiter = ',')
    dic = {}
    for row in lesari:
        if row[0] == 'lang':
            continue
        lc = row[0]
        del row[0]
        dic[lc] = row
    return dic

def getOneWiki(mode, lang, wiki, offset, mindate, maxdate, df):
    global ud
    if lang == 'www' or wiki == 'wikimedia':
        mul = True
    else:
        mul = False
    final = 0
    webpage = BeautifulSoup(get('https://'+lang+'.'+wiki+'.org/w/index.php?title=Special:Contributions/' + ud[0] + '&offset=' + offset + '&limit='+str(display)+'&target=' + ud[0]).content, 'html.parser')
    try:
        npo = webpage.find('a', {'class':'mw-nextlink'})['href'][len(ud[0])+49:len(ud[0])+63]
    except TypeError:
        npo = ''
    listof_meta = webpage.find_all('ul', {'class':'mw-contributions-list'})
    if len(listof_meta) == 0:
    	return 0
    listof = []
    for ul in listof_meta:
        for li in ul.find_all('li'):
            listof.append(li)
    dfp = df[0].split('%')
    if len(dfp[0]) == 0:
        del dfp[0]
    datelist = [0, 0, 0, 0, 0]
    surpassed = False
    for a in listof:
        datetext = a.find('a').getText()
        mp = 0
        while mp < len(datetext):
            nos = 0
            while nos < 10:
                if datetext[mp] in othernumbers[nos]:
                    datetext[mp] = str(nos)
                    break
                nos += 1
            mp += 1
        ptr = 0
        for ts in dfp:
            if ts[0] == 'y':
                datelist[0] = int(datetext[ptr:ptr + 4])
                ptr += 3 + len(ts)
            elif ts[0] == 't':
                datelist[3] = int(datetext[ptr:ptr + 2])
                datelist[4] = int(datetext[ptr + 3:ptr + 5])
                ptr += 4 + len(ts)
            elif ts[0] == 'd':
                if datetext[ptr + 1] in '0123456789':
                    datelist[2] = int(datetext[ptr:ptr + 2])
                    ptr += len(ts) + 1
                else:
                    datelist[2] = int(datetext[ptr:ptr + 1])
                    ptr += len(ts)
            elif ts[0] == 'm':
                nc = ptr
                while datetext[nc] != ts[1]:
                    nc += 1
                mname = datetext[ptr:nc]
                ptr = nc
                ne = 1
                while ne < 13:
                    if df[ne] == mname:
                        break
                    ne += 1
                datelist[1] = ne
                ptr += len(ts) - 1
        datestr = str(datelist[0]) + '-'
        if datelist[1] < 10:
            datestr += '0'
        datestr += str(datelist[1]) + '-'
        if datelist[2] < 10:
            datestr += '0'
        datestr += str(datelist[2]) + 'T'
        if datelist[3] < 10:
            datestr += '0'
        datestr += str(datelist[3]) + ':'
        if datelist[4] < 10:
            datestr += '0'
        datestr += str(datelist[4]) + ':00+00:00'
        date = datetime.fromisoformat(datestr)
        if date > maxdate:
            continue
        elif date < mindate:
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
            fstr = ''
            for g in fstr1:
                if g == '−':
                    fstr += '-'
                elif g in '+0123456789':
                    fstr += g
            final += int(fstr)
    if not surpassed:
        final += getOneWiki(mode, lang, wiki, npo, mindate, maxdate, df)
    return final

start_time = time.time()
mode = sys.argv[1]
ud = readUser()
dateformat = readDateFormat()
sd = ud[1]
ed = ud[2]
mxdstr = ed.strftime('%Y%m%d%H%M%S')
for b in ud[3]:
    for a in ud[4]:
        try:
            dfb = dateformat[b]
        except KeyError:
            print('Error: missing date format for language ' + b + '.')
        try:
            f = getOneWiki(mode, b, a, mxdstr, sd, ed, dfb)
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
    try:
        f = getOneWiki(mode, othervalues[ow][0], othervalues[ow][1], mxdstr, sd, ed, dateformat['mul'])
        if f != 0:
            totalcontribs['other'][ow] = f
        final += f
    except requests.exceptions.ConnectionError:
        print('Bad connection: commons')
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
