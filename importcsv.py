#!/usr/bin/python

from gnucash import Session, Account, Split
import gnucash
import datetime
import sys
import os
from fractions import Fraction

if len(sys.argv) != 3:
    print "Usage: %s your.gnucash data.csv" % os.path.basename(sys.argv[0])
    sys.exit(-1)

CsvFile = os.path.join(os.getcwd(), sys.argv[1])
if not os.path.exists(CsvFile):
    print "Error: %s not found" % CsvFile
    sys.exit(-1)
print "importing from %s" % CsvFile

GnuCashFile = os.path.join(os.getcwd(), sys.argv[2])
if not os.path.exists(GnuCashFile):
    print "Error: %s not found" % GnuCashFile
    sys.exit(-1)
print "importing into %s" % GnuCashFile


f = open(CsvFile)
f.readline()                    # skip header
stock_date = []
stock_price = []
for data in f:
    year = int(data.rsplit(',')[0].rsplit('/')[2])
    month = int(data.rsplit(',')[0].rsplit('/')[0])
    day = int(data.rsplit(',')[0].rsplit('/')[1])
    stock_date.append(datetime.datetime(year,month,day))
    stock_price.append(float(data.rsplit(',')[1]))

f.close()

# Initialize Gnucash session
url = "xml://"+GnuCashFile
session = Session(url, False, False, False)
root = session.book.get_root_account()
book = session.book
account = book.get_root_account()
pdb = book.get_price_db()
commod_table = book.get_table()
stock = commod_table.lookup('FUND', 'VAIIT')
cur = commod_table.lookup('CURRENCY', 'USD')
# Add the prices
pdb = book.get_price_db()
# Get stock data
pl = pdb.get_prices(stock,cur)
if len(pl)<1:
  print 'Error: need at least one database entry to clone ...'
  sys.exit(-1)

pl0 = pl[0]

for i in range(0,len(stock_date)):
  p_new = pl0.clone(book)
  p_new = gnucash.GncPrice(instance=p_new)
  print 'Adding',i,stock_date[i],stock_price[i]
  p_new.set_time(stock_date[i])
  v = p_new.get_value()
  v.num = int(Fraction.from_float(stock_price[i]).limit_denominator(100000).numerator)
  v.denom = int(Fraction.from_float(stock_price[i]).limit_denominator(100000).denominator)
  p_new.set_value(v)
  pdb.add_price(p_new)

# Clean up
session.save()
session.end()
session.destroy()
