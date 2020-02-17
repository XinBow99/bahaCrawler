import requests
import os


def download(title, postId, datas, word):
    title = title.replace('.', '').replace('|', '').replace('?', '').replace(
        '!', '').replace('..', '').replace('...', '').replace('\\', '').replace('/', '')
    folder_path = './bahaImage/' + word +'/'+ title

    if (os.path.exists(folder_path) == False):  # 判斷主資料夾是否存在
        os.makedirs(folder_path)  # Create folder

    for i, data in enumerate(datas):
        image = requests.get(data)

        img_path = folder_path + '/'

        if (os.path.exists(img_path) == False):  # 判斷副資料夾是否存在
            os.makedirs(img_path)  # Create folderＦ
            # 以byte的形式將圖片數據寫入
        with open(img_path + postId + "_" + data.split('/')[-1], 'wb') as file:
            file.write(image.content)
            file.flush()
        file.close()  # close file
        print("目前：第 {} 張照片，進度{}%".format(
            i + 1, int((i + 1) / len(datas) * 100)))
    print(("---------------\n"
           "{}-圖片下載完成\n"
           "準備下載下一張...").format(title))
