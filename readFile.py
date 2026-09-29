import pandas as p
import openpyxl as file


def read_data():
    df = p.read_excel(r"E:\\sase-automation\\data\\test_data\\github_pw\\test_github_uniquepolicy.xlsx")
    #print(df)
    yield df






data = next(read_data())
#print(data["testdata"])
testdata = p.DataFrame(data["testdata"])
#print(testdata)
for data in testdata:
    print(data)
