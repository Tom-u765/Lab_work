# 表や計算式などは画像ではないため取得できない。なので性能としてはいまいち。テーブル名からその辺を取得することができれば強いか。
# 画像の自動取得とパワポの自動作成などを組み合わせればフォルダ内の画像をパワポテンプレ通りに配置することが可能になるので論文系のパワポ作成を効率化できるかもしれない。

#https://fastclassinfo.com/entry/python_pdf_get_all_image/

# プログラム1｜ライブラリ設定
import fitz
import os
from PIL import Image
import io
 
# プログラム2｜「.py」が保管されているフォルダを取得
curdir = os.getcwd()
 
# プログラム3｜取得した画像を保管するためのフォルダ作成
file = 'You_are_where_you_tweet.pdf'
filename = file.replace('.pdf','')
path = os.path.join(curdir, filename)
if not os.path.isdir(path):
    os.makedirs(path)
 
# プログラム4｜読み込んだ画像情報を格納するリスト
info = []
 
# プログラム5｜PDF読み込み
pdf_file = fitz.open(file)
 
# プログラム6｜PDFをページごとに読み込み
for pageNo in range(len(pdf_file)):
    page = pdf_file[pageNo]
 
    # プログラム7｜ページごとの画像を読み込む
    image_list = page.getImageList()
 
    # プログラム8｜ページごとの画像情報をリストに格納
    if len(image_list) > 0:
        info.append(f'{pageNo}ページには{len(image_list)}コの画像ファイル')
    else:
        info.append(f'{pageNo}ページには0コの画像ファイル')
 
    # プログラム9｜ページ内の画像情報を順々に処理
    for index, img in enumerate(image_list, start=1):
 
        # プログラム10｜画像を取得
        xref = img[0]
        base_image = pdf_file.extractImage(xref)
        image_ext = base_image['ext']
        image_bytes = base_image['image']
 
        # プログラム11｜PILライブラリで画像として取得
        image = Image.open(io.BytesIO(image_bytes))
 
        # プログラム12｜画像を保存する
        imagefilepath = os.path.join(path, f'image{pageNo+1}_{index}.{image_ext}')
        image.save(open(imagefilepath, 'wb'))
 
# プログラム13｜PDFの画像取得情報をテキストファイルとして保存
newfilename = os.path.join(path, f'{filename}.txt')
res = '\n'.join(info)
with open(newfilename, 'w') as f:
    f.write(res)
