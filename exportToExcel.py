import pandas as pd

def showD2T(data):
    print("showD2T")
    datas_df = pd.DataFrame(data)
    print(datas_df)
def export2Excel(data,name = "我幫你取"):
    print('Load data...')
    datas_df = pd.DataFrame(data)
    datas_df.to_excel("{}搜尋資訊.xlsx".format(name))
    print('D2E done!')