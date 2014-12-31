#!/usr/bin/env python

import random, sys

# check for the right # of args
if len(sys.argv) != 3:
    print "USAGE: " + sys.argv[0], " [output file] [# of cards]"
    print "Example: " + sys.argv[0] + " bingo.html 20"
    sys.exit(1)

# read in the bingo terms

pull_div = "left"

def left_or_right():
    global pull_div
    if pull_div == "left":
        pull_div = "right"
    else:
        pull_div = "left"

    return pull_div

# XHTML4 Strict, y'all!
head = ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">\n"
        "<html lang=\"en\">\n<head>\n"
        "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n"
        "<title>Bingo Cards</title>\n"
        "<style type=\"text/css\">\n"
        "\tbody { font-size: 10px; }\n"
        "\ttable { margin: 20px auto; border-spacing: 2px; }\n"
        "\t.newpage { page-break-after:always; }\n"
        "\ttr { height: 60px; }\n"
        "\ttd { text-align: center; border: thin black solid; padding: 5px; width: 60px; }\n"
        "</style>\n</head>\n<body>\n")

def getRandom(low, high, used):
    i = 0
    while i in used:
        i = random.randint(low, high)

    used.append(i)

    return str(i)

used_tables = list()

def check_unique_table(table):
    global used_tables
    
    if len(used_tables) > 1:
        for used_table in used_tables:
            for i in range(0, 25):
                if used_table[i] != table[i]:
                    used_tables.append(table)
                    return True

    else:
        used_tables.append(table)
        return True

    return False

def generateNumbers():
    used = list()
    used.append(0)

    while True:
        l = list()
        for i in range(0, 5):
            l.append([None] * 5)

        for row in range(0, 5):
            for column in range(0, 5):
                if column == 0:
                    l[row][column] = getRandom(1, 15, used)
                if column == 1:
                    l[row][column] = getRandom(16, 30, used) #random.randint(16, 30)
                if column == 2:
                    l[row][column] = getRandom(31, 45, used) #random.randint(31, 45)
                if column == 3:
                    l[row][column] = getRandom(46, 60, used) #random.randint(46, 60)
                if column == 4:
                    l[row][column] = getRandom(61, 75, used) #random.randint(61, 75)


        l2 = list()
        for row in range(0, 5):
            for column in range(0, 5):
                l2.append(l[row][column])

        if check_unique_table(l2):
            return l2
        else:
            print "Wow, found a duplicate table!"
            continue

# Generates an HTML table representation of the bingo card for terms
def generateTable():
    res = "<div align=\"center\" style=\"width:50%%; height:50%%; float:%s\">\n" % (left_or_right())
    terms = generateNumbers()
    ts = terms
    ts[12] = 'FREE SPACE'
    res += "<table>\n"

    bingo = "BINGO"

    res += "\t<tr>\n"
    for i in range(0, len(bingo)):
        res += "\t\t<td><font size=\"24\">%s</font></td>\n" % (bingo[i])
    res += "\t</tr>\n"

    for i, term in enumerate(ts):
        if i % 5 == 0:
            res += "\t<tr>\n"
        res += "\t\t<td>" + term + "</td>\n"
        if i % 5 == 4:
            res += "\t</tr>\n"
    res += "</table>\n"
    res += "</div>\n"
    return res

out_file = open(sys.argv[1], 'w')
out_file.write(head)
cards = int(sys.argv[2])
for i in range(cards):
    if i % 4 == 0 and i != 0:
        out_file.write("<table class=\"newpage\"></table>")
    out_file.write(generateTable())

out_file.write("</body></html>")

out_file.close()
