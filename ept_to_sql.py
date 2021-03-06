import sqlite3
import xlrd
import sys

def unique_code(id_state=None, id_contry=None):
    if int(id_state) < 10:
        id_state = '0' + str(int(id_state))
    return str(id_state) + str(id_contry)


def parser(filename=None):

    conn = sqlite3.connect('db-ericsson.db')
    cur = conn.cursor()

    wb = xlrd.open_workbook(filename)
    sheet_names = ['EPT_3G_LTE_OUTDOOR','EPT_3G_LTE_INDOOR','PLAN_OUTDOOR','PLAN_INDOOR']

    # EPT Number of column
    node1 = 6
    node2 = 94
    node3 = 1
    rnc = 46
    vendor = 72
    tecnologia = 3
    id_state = 11
    id_contry = 13

    cur.execute('''
        CREATE TABLE IF NOT EXISTS ept(
            id integer PRIMARY KEY AUTOINCREMENT,
            node1 text,
            node2 text,
            node3 text,
            cvegeo text,
            rnc text,
            vendor text,
            tecnologia text,
            tab text
        );
    ''')

    conn.commit()

    for sheet in sheet_names: 
        ws = wb.sheet_by_name(sheet)
        for row in range(ws.nrows):
            if row != 0:
                cur.execute('''
                INSERT INTO ept (node1, node2, node3, cvegeo, rnc, vendor, tecnologia, tab)
                VALUES (?,?,?,?,?,?,?,?);
                ''',(ws.cell_value(row,node1), ws.cell_value(row,node2), ws.cell_value(row,node3), unique_code(id_state=ws.cell_value(row,id_state), id_contry=ws.cell_value(row,id_contry)), ws.cell_value(row,rnc), ws.cell_value(row,vendor), ws.cell_value(row,tecnologia), sheet))
                # print(f"{row} node 1: {ws.cell_value(row,node1)} node2: {ws.cell_value(row,node2)} node3: {ws.cell_value(row,node3)} cvegeo: {str(int(ws.cell_value(row,id_state))) + str(ws.cell_value(row,id_contry))} rnc: {ws.cell_value(row,rnc)} vendor: {ws.cell_value(row,vendor)} tecnologia: {ws.cell_value(row,tecnologia)} tab: {sheet} ")
                
    cur.execute('''DELETE FROM ept WHERE rowid NOT IN(SELECT min(rowid) FROM ept GROUP BY node1, node2, node3, tecnologia);''')
    conn.commit()
    conn.close()
    return "Parsed Complete"

if __name__ == "__main__":
    parser(sys.argv[1])