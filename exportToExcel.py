import pandas as pd
import json
def showD2T(data):
    print("showD2T")
    datas_df = pd.DataFrame(data)
    print(datas_df)
def export2Excel(data,name = "我幫你取"):
    print('Load data...')
    with open('{}.json'.format(name),'w',encoding="utf-8") as opJsonAction:
        opJsonAction.write(json.dumps(data, ensure_ascii=False))
        opJsonAction.close()
    for i,d in enumerate(data):
        del data[i]['detail']
        del data[i]['totalPictures']
    datas_df = pd.DataFrame(data)
    datas_df.to_excel("{}搜尋資訊.xlsx".format(name))
    print('D2E done!')