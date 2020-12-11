#import系

import Prof			#プロフィールのテキストファイル
import cv2 as cv	#Opencv2
import tkinter		#GUIのやつ
import sys,os 		#パスとかをいじるため
import numpy as np	#numpy
import tkinter.font as font			#font
from tkinter import filedialog		#GUIでパスを指定するためのファイルダイアログのやつ
from tkinter import ttk				#tk拡張
from PIL import Image, ImageTk		#GUIにいろんな画像貼り付けるため
import webbrowser					#ブラウザ操作用
import tensorflow as tf 			#機械学習
import pathlib						#パス操作用
from pixiv.example import vone
import json
import time		#時間計測用
import timeit	

#文字コードをUTF-8で指定して日本語ファイルを開けるようにする
import io

#いろんなとこで使う変数宣言 ＆ GC回避
img = None
filepath = ''
picturename = None
i = 0
hanbetu_frame = None
img_pil = None
paths = None

#Cascade分類器のパス指定
cas_dir_hubuki = "./cascade_files/hubuki.xml"	#ふぶき
cas_dir_korone = "./cascade_files/korone.xml"	#ころね
cas_dir_akua = "./cascade_files/akua.xml"		#あくあ
cas_dir_pekora = "./cascade_files/pekora.xml"	#ふぶき
cas_dir_koko = "./cascade_files/koko.xml"		#ここ
cas_dir_marin = "./cascade_files/marin.xml"		#まりん
cas_dir_maturi = "./cascade_files/maturi.xml"	#まつり
cas_dir_haato = "./cascade_files/haato.xml"		#はあと
cas_dir_noeru = "./cascade_files/noeru.xml"		#のえる
cas_dir_rusia = "./cascade_files/rusia.xml"		#るしあ

#cascade読み込み
cas_hubuki = cv.CascadeClassifier(cas_dir_hubuki)
cas_korone = cv.CascadeClassifier(cas_dir_korone)
cas_akua = cv.CascadeClassifier(cas_dir_akua)
cas_pekora = cv.CascadeClassifier(cas_dir_pekora)
cas_koko = cv.CascadeClassifier(cas_dir_koko)
cas_marin = cv.CascadeClassifier(cas_dir_marin)
cas_maturi = cv.CascadeClassifier(cas_dir_maturi)
cas_haato = cv.CascadeClassifier(cas_dir_haato)
cas_noeru = cv.CascadeClassifier(cas_dir_noeru)
cas_rusia = cv.CascadeClassifier(cas_dir_rusia )
cascades = [cas_hubuki,cas_korone,cas_akua,cas_pekora,cas_koko,cas_marin,cas_maturi,cas_haato,cas_noeru,cas_rusia]

#キャラの辞書型変数
chara_id = {'1':'hubuki','2':'korone','3':'akua','4':'pekora','5':'koko','6':'marin','7':'maturi','8':'haato','9':'noeru','10':'rusia'}
chara_id2 = {'0':'sirakami','1':'inugami','2':'minato','3':'usada','4':'kiryu','5':'housyou','6':'natuiro','7':'akai','8':'sirogane','9':'uruha'}
chara_dict = {'hubuki':0,'korone':0,'akua':0,'pekora':0,'koko':0,'marin':0,'maturi':0,'haato':0,'noeru':0,'rusia':0}

#キャラクタ紹介の個人ページ(フレーム)作成
def create_intro(a):
	exit = ttk.Frame(root)
	exit.grid(row=0, column=0, sticky='news')
	global chara_img
	chara_img = tkinter.PhotoImage(file = Prof.img_return(a))
	imgs = ttk.Label(exit,image = chara_img)
	imgs.grid(row=0,column=0,padx=20, pady=25)
	txt = ttk.Label(exit,text=Prof.prof_return(a),font=("", 10,),background='#dcdcdc',padding=(5))
	txt.grid(row=0,column=1,padx=25, pady=25)
	back = ttk.Button(exit, text='戻る',command=lambda:destr_page(exit))
	back.grid(row=1, column=0,padx=30, pady=25)
	b=Prof.url_return(a)
	chr_link = ttk.Button(exit, text='キャラ公式ページ',command=lambda:link(b))
	chr_link.grid(row=1, column=1,padx=30, pady=25)

#画面遷移(進む用
def changePage(page):
	page.tkraise()

#画面遷移(戻る用
def back(page):
	page.lower()

#動的画面遷移
def destr_page(exit):
	exit.lower()
	exit.forget()

#プレビュー画像のリサイズと拡張子変換の関数
INTERPOLATIONS = [cv.INTER_LINEAR, cv.INTER_AREA, cv.INTER_NEAREST, cv.INTER_CUBIC, cv.INTER_LANCZOS4]
def resize(size=300, interpolations=INTERPOLATIONS):
	global filepath
	global img
	global img_pil
	img = cv.imread(filepath)
	y, x = img.shape[0:2]
	max_len = max(x, y)
	interpolation = np.random.choice(interpolations)
	if max_len > size:
		scale = max_len / size
		x, y = round(x / scale), round(y / scale)
		img = cv.resize(img, (x, y), interpolation=interpolation)
	im_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	Image.fromarray(im_rgb).save('data/rgb_pillow.jpg')
	img_read = Image.open('./data/rgb_pillow.jpg')
	img_pil = ImageTk.PhotoImage(img_read)
	resized = tkinter.Label(hanbetu_frame,image=img_pil)
	resized.place(x=320,y=150,height=300,width=300)
	Image.fromarray(im_rgb).save('data/rgb_pillow.jpg')
	png_jpg = Image.open(filepath)
	png_jpg = png_jpg.convert('RGB')
	png_jpg.save('./data/png_to_jpg.jpg', quality=95)
	

#ファイルダイアログを開く関数
def file_select():
	global filepath
	global picturename
	global paths
	fTyp = [("画像ファイル","*.png;*.jpg;*.gif;*.jpeg")]				#参照可能なファイル形式指定
	iDir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Pictures"					#デフォルトで開くパス指定
	filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)	#ファイルダイアログを開く
	filepathvar.set(filepath)
	picturename = str(os.path.splitext(os.path.basename(filepath))[0])			#取得したアドレスから画像の名前を保存
	paths = pathlib.Path(filepath)
	if filepath is not '':
		resize()	#画像のプレビューを配置

#キャラ判別
def gazou():
	global filepath
	global img
	global paths
	img = cv.imread(filepath)
	img_g = cv.imread(filepath,0)
	
#	start = time.perf_counter()
	a = vone.loobe('./data/png_to_jpg.jpg')
#	end = time.perf_counter()
#	print(f"実行時間: {end - start}")
	
	b = [k for k, v in chara_id2.items() if v == a]
	create_intro(int(b[0]))

	''' 旧バージョン
	for i in range(len(cascades)):		#cascadeファイルの数だけ実行
		chara_dict[list(chara_dict.keys())[i]]=len((cascades[i].detectMultiScale(img_g,scaleFactor=1.11,minNeighbors=0,minSize=(int(img.shape[0]*0.05),int(img.shape[1]*0.05)))))		#キャラごとに画像認識してそのスコアを記録
	a = sorted(chara_dict.items(), key=lambda x: x[1])[::-1]	#スコア順に並べ替え
	b = [k for k, v in chara_id.items() if v == a[0][0]]		#名前を取ってくる
	create_intro(int(b[0])-1)									#名前でプロフ表示
	'''

	''' デバッグ用の認識したエリア表示
	face = cas_akua.detectMultiScale(img_g,scaleFactor=1.11,minNeighbors = 0,minSize=(int(img.shape[0]*0.1),int(img.shape[1]*0.1)) )
	print(face)
	if face is not None:			#顔認識できたら実行
		for x,y,w,h in face:		#白枠で顔を囲む(デバッグ用)
			cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
		cv.imshow("face_area",img)
		print(len(face))
	'''

#URLを開く
def link(url):
	webbrowser.open(str(url))

#GUIのコード

root = tkinter.Tk()
root.title('Prototype')
root.geometry('640x480')
root.resizable(width=0, height=0)
filepathvar=tkinter.StringVar()
filepathvar.set(filepath)

#font作成
title_font = font.Font(family="Hiragino Kaku Gothic ProN", size=40, weight="bold",underline=True, slant="italic")

#Style作成
BGStyle = ttk.Style()
BGStyle.theme_use('classic')
BGStyle.configure('gray.TFrame', background='FFFFFF')

#プロフ画像読み込み
chara_img = tkinter.PhotoImage(file = Prof.img_return(0))

#図鑑フレーム
index = ttk.Frame(root)
index.grid(row=0, column=0, sticky='news')

#図鑑フレーム_キャラ用のボタン
button1 = ttk.Button(index, text='白上フブキ',command=lambda:create_intro(0),padding= (40,20))
button1.grid(row=0, column=0,padx=30, pady=25)
button2 = ttk.Button(index, text='戌神ころね',command=lambda:create_intro(1),padding= (40,20))
button2.grid(row=0, column=1,padx=30, pady=25)
button3 = ttk.Button(index, text='湊あくあ',command=lambda:create_intro(2),padding= (40,20))
button3.grid(row=0, column=2,padx=30, pady=25)
button4 = ttk.Button(index, text='兎田ぺこら',command=lambda:create_intro(3),padding= (40,20))
button4.grid(row=1, column=0,padx=30, pady=25)
button5 = ttk.Button(index, text='桐生ココ',command=lambda:create_intro(4),padding= (40,20))
button5.grid(row=1, column=1,padx=30, pady=25)
button6 = ttk.Button(index, text='宝鐘マリン',command=lambda:create_intro(5),padding= (40,20))
button6.grid(row=1, column=2,padx=30, pady=25)
button7 = ttk.Button(index, text='夏色まつり',command=lambda:create_intro(6),padding= (40,20))
button7.grid(row=2, column=0,padx=30, pady=25)
button8 = ttk.Button(index, text='赤井はあと',command=lambda:create_intro(7),padding= (40,20))
button8.grid(row=2, column=1,padx=30, pady=25)
button9 = ttk.Button(index, text='白銀ノエル',command=lambda:create_intro(8),padding= (40,20))
button9.grid(row=2, column=2,padx=30, pady=25)
button10 = ttk.Button(index, text='潤羽るしあ',command=lambda:create_intro(9),padding= (40,20))
button10.grid(row=3, column=0,padx=30, pady=25)

#ここまで 下は戻るボタン
button11 = ttk.Button(index, text='homeへ',padding= (40,20),command=lambda:changePage(main_frame)) #本来はここにホーム画面
button11.grid(row=3, column=2,padx=30, pady=25)

#メイン_フレーム ウィジット作成
main_frame = ttk.Frame(root)
titletext = ttk.Label(main_frame,text=u'hololive AI',font=title_font,foreground='#5050FF')
hanbetu_button = ttk.Button(main_frame,text=u'キャラ判別',command=lambda:changePage(hanbetu_frame))
ziten_button = ttk.Button(main_frame,text=u'キャラ辞典',command=lambda:changePage(index))
ofi_button = ttk.Button(main_frame,text=u'ホロライブ公式HP',command=lambda:link('https://www.hololive.tv/'))

#	背景画像を追加しようとしていたがすべてのフレームで適応するのに時間がかかりそうなためコメントアウト
#メイン_背景 
img_read = Image.open('./img/backg.png')
img_bg = ImageTk.PhotoImage(img_read)
bg = ttk.Label(main_frame,image=img_bg)


#キャラ判別_フレーム ウィジット作成
hanbetu_frame = ttk.Frame(root)
keikoku_label = ttk.Label(hanbetu_frame,text=u'注意\n対応している拡張子は\n以下のみです。\npng、jpg、gif、jpeg\n',font=("", 16,),background='#dcdcdc',padding=(5))
sansyou_button = ttk.Button(hanbetu_frame,text=u'画像選択',command=file_select)
zikkou_button = ttk.Button(hanbetu_frame,text=u'実行',command=gazou)
back_button = ttk.Button(hanbetu_frame,text=u'戻る',command=lambda:changePage(main_frame))
img_dir_entry = ttk.Label(hanbetu_frame,textvariable=filepathvar)

#メインフレーム ウィジット配置
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.propagate(0)
bg.place()
titletext.place(height=100,width=300,x=170,y=120)
hanbetu_button.place(height=50,width=200,x=220,y=280)
ziten_button.place(height=50,width=200,x=220,y=340)
ofi_button.place(height=50,width=200,x=220,y=400)

#キャラ判別フレーム ウィジット配置
hanbetu_frame.grid(row=0, column=0, sticky="nsew")
hanbetu_frame.propagate(0)
keikoku_label.place(x=80,y=225,height=150,width=220)
sansyou_button.place(x=80,y=90,height=50,width=100)
zikkou_button.place(x=190,y=150,height=50,width=100)
back_button.place(x=80,y=150,height=50,width=100)
img_dir_entry.place(x=190,y=95,height=40,width=400)

#メインフレームを前に出す
main_frame.tkraise()

#GUI ループ
root.mainloop()
