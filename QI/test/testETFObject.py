import QI.datatypes.datatypes as dt
def testDayData():
    dd:dt.ObjectDayData = dt.ObjectDayData('1996-11-18',\
        17.5, 55.0, 17.5, 50.0, 47.5, 31780)
    dd.printData()

testDayData()

