import sys
import sqlite3
from bs4 import BeautifulSoup

def main(fname):
    soup = BeautifulSoup(open(fname))
    conn = sqlite3.connect('nordpool.sqlite')
    conn.execute('''CREATE TABLE IF NOT EXISTS
        elspot (date TEXT NOT NULL,
        hour TEXT NOT NULL,
        area TEXT NOT NULL,
        price REAL NOT NULL,
        PRIMARY KEY (date, hour, area))''')
    header = [cell.get_text().strip().encode('ascii', 'ignore') for cell in
        soup.find('thead').find_all('tr')[-1].find_all('td')]
    data = [[cell.get_text().strip().replace(',', '.') for cell in row.find_all('td')]
           for row in soup.find('tbody').find_all('tr')]
    data2 = []
    for row in data:
        date = row[0][-4:] + '-' + row[0][:5]
        hour = row[1][:2]
        for (i, price) in enumerate(row[2:]):
            data2.append((date, hour, header[i+2], price))

    conn.executemany('''INSERT OR REPLACE INTO elspot VALUES (?, ?, ?, ?)''',
        data2)
    conn.commit()

if __name__ == "__main__":
    main(sys.argv[1])
