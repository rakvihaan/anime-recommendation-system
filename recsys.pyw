import tkinter as tk
from tkinter import font
import requests
from PIL import ImageTk, Image
import json
import pandas as pd
from io import BytesIO
import sys 
import os
sys.path.append(os.path.abspath("./"))
from main_recsys import *
import webbrowser

df = pd.read_csv("./database/anime_titles_cleaned.csv")
 
def view_results():
	global img10,img11,img12,img20,img21,img22,img30,img31,img32,img40,img41,img42,img50,img51,img52, link1, link2, link3, link4, link5
	with open('./results.json') as f:
		data = json.load(f)

	dict_items = data.items()
	for r in range(1,6):
		listOut = list(dict_items)[(r-1):r]
		
		for key, value in listOut:
			if key in df['title'].values:
				index = df.title[df.title == key].index.tolist()[0]
				imglink = df.loc[index, 'img_url']
				linkw = df.loc[index, 'link']
			response = requests.get(imglink)
			
			img1 = Image.open(BytesIO(response.content))
			img2 = img1.resize((84, 120), Image.ANTIALIAS)
			img = ImageTk.PhotoImage(img2)
			
			#print(listOut)
			link = linkw
			tttt = key
			if r == 1:
				img10 = Image.open(BytesIO(response.content))
				img11 = img10.resize((84, 120), Image.ANTIALIAS)
				img12 = ImageTk.PhotoImage(img11)

				labelr1['image'] = img12
				link1 = linkw
				labelr1.bind("<Button-1>", lambda e: webbrowser.open_new(link1))
				#print(tttt)
				#print(linkw)
			elif r == 2:
				img20 = Image.open(BytesIO(response.content))
				img21 = img20.resize((84, 120), Image.ANTIALIAS)
				img22 = ImageTk.PhotoImage(img21)

				labelr2['image'] = img22
				link2 = linkw
				labelr2.bind("<Button-1>", lambda e: webbrowser.open_new(link2))
				#print(tttt)
				#print(linkw)
			elif r == 3:
				img30 = Image.open(BytesIO(response.content))
				img31 = img30.resize((84, 120), Image.ANTIALIAS)
				img32 = ImageTk.PhotoImage(img31)
				
				labelr3['image'] = img32
				link3 = linkw
				labelr3.bind("<Button-1>", lambda e: webbrowser.open_new(link3))
				#print(tttt)
				#print(linkw)
			elif r == 4:
				img40 = Image.open(BytesIO(response.content))
				img41 = img40.resize((84, 120), Image.ANTIALIAS)
				img42 = ImageTk.PhotoImage(img41)
				
				labelr4['image'] = img42
				link4 = linkw
				labelr4.bind("<Button-1>", lambda e: webbrowser.open_new(link4))
				#print(tttt)
				#print(linkw)
			elif r == 5:
				img50 = Image.open(BytesIO(response.content))
				img51 = img50.resize((84, 120), Image.ANTIALIAS)
				img52 = ImageTk.PhotoImage(img51)
				
				labelr5['image'] = img52
				link5 = linkw
				labelr5.bind("<Button-1>", lambda e: webbrowser.open_new(link5))
				#print(tttt)
				#print(linkw)
			

def get_info():
	global info1, info2, info3,info4, info5
	with open('./results.json') as f:
		data = json.load(f)

	dict_items = data.items()
	for r in range(1,6):
		listOut = list(dict_items)[(r-1):r]
		
		for key, value in listOut:
			if key in df['title'].values:
				index = df.title[df.title == key].index.tolist()[0]
				name = df.loc[index, 'title']
				gen = df.loc[index, 'genre']
				sco = df.loc[index, 'score']
			#print(listOut)
			# outPut = img + "Anime"
			tttt = key
		
			if r == 1:
				info1 = 'Name: %s \nGenre: %s \nScore: %s' % (name, gen, sco)
				labelr1t['text'] = info1
				#print(tttt)
			elif r == 2:
				info2 = 'Name: %s \nGenre: %s \nScore: %s' % (name, gen, sco)	
				labelr2t['text'] = info2	
				
				#print(tttt)
			elif r == 3:
				info3 = 'Name: %s \nGenre: %s \nScore: %s' % (name, gen, sco)
				labelr3t['text'] = info3
				
				#print(tttt)
			elif r == 4:
				info4 = 'Name: %s \nGenre: %s \nScore: %s' % (name, gen, sco)
				labelr4t['text'] = info4
				
				#print(tttt)
			elif r == 5:
				info5 = 'Name: %s \nGenre: %s \nScore: %s' % (name, gen, sco)
				labelr5t['text'] = info5
				
				#print(tttt)
			

		
def get_reco(input_name):
	aName = input_name
	reco = get_recommendation(aName)
	view_results()
	get_info()




root = tk.Tk()

root.title('Anime Recommendation System')
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

bg_clr = '#0f083b'
frame_clr = '#5682c1'
but_clr = '#ff471a'
but_clicked_clr = '#ff8566'

canvas = tk.Canvas(root, bg=bg_clr, height=HEIGHT, width=WIDTH, highlightthickness=0) 
canvas.pack()


main_frame = tk.Frame(root, bg=bg_clr, bd=6)
main_frame.place(rely=0.07, relwidth=1, relheight=1)

path = Image.open("bg2.jpg")
bg_img = ImageTk.PhotoImage(path)

# background_image = tk.PhotoImage(file=img)
background_label = tk.Label(main_frame, image=bg_img)
background_label.place(relwidth=1, relheight=1)

title_x = WIDTH//2
title_y = int(HEIGHT*0.044)

canvas.create_text(title_x,title_y, text="Anime Recommendation", font=('Anime Ace', 25), fill='white')

frame = tk.Frame(main_frame, bg=frame_clr, bd=10)
frame.place(relx=0.5, rely=0.05, relwidth=0.6, relheight=0.06, anchor='n')

entry = tk.Entry(frame, font=('Ubuntu', '15'), bd=2)
entry.place(rely=0, relwidth=0.65, relheight=1)

button_frame = tk.Frame(frame, bg='black', bd=1.5)
button_frame.place(relx=0.7, relheight=1, relwidth=0.3)

button = tk.Button(button_frame, text="Get Recommendations", font=('Ubuntu', '11', ), fg='white', bg = but_clr, activebackground=but_clicked_clr, activeforeground='white', borderwidth=0, relief='solid', command=lambda: get_reco(entry.get()))
button.place(relheight=1, relwidth=1)


lower_frame = tk.Frame(main_frame, bg=frame_clr, bd=10)
lower_frame.place(relx=0.5, rely=0.15, relwidth=0.6, relheight=0.65, anchor='n')

rec1 = tk.Frame(lower_frame,)
rec1.place(relx=0, rely=0, relheight=0.198, relwidth=1)

rec2 = tk.Frame(lower_frame,)
rec2.place(relx=0, rely=0.2, relheight=0.198, relwidth=1)

rec3 = tk.Frame(lower_frame,)
rec3.place(relx=0, rely=0.4, relheight=0.198, relwidth=1)

rec4 = tk.Frame(lower_frame,)
rec4.place(relx=0, rely=0.6, relheight=0.198, relwidth=1)

rec5 = tk.Frame(lower_frame,)
rec5.place(relx=0, rely=0.8, relheight=0.198, relwidth=1)

# for picture
labelr1 = tk.Label(rec1, justify='left')
labelr1.place(relx=-0.43, relwidth=1, relheight=1)

labelr2 = tk.Label(rec2)
labelr2.place(relx=-0.43, relwidth=1, relheight=1)

labelr3 = tk.Label(rec3)
labelr3.place(relx=-0.43,relwidth=1, relheight=1)

labelr4 = tk.Label(rec4)
labelr4.place(relx=-0.43,relwidth=1, relheight=1)

labelr5 = tk.Label(rec5)
labelr5.place(relx=-0.43,relwidth=1, relheight=1)

# for info

labelr1t = tk.Label(rec1, anchor='w', justify='left', font=('Ubuntu', '13'))
labelr1t.place(relx=0.15, relwidth=0.8, relheight=1)

labelr2t = tk.Label(rec2, anchor='w', justify='left', font=('Ubuntu', '13'))
labelr2t.place(relx=0.15, relwidth=0.8, relheight=1)

labelr3t = tk.Label(rec3, anchor='w', justify='left', font=('Ubuntu', '13'))
labelr3t.place(relx=0.15,relwidth=0.8, relheight=1)

labelr4t = tk.Label(rec4, anchor='w', justify='left', font=('Ubuntu', '13'))
labelr4t.place(relx=0.15,relwidth=0.8, relheight=1)

labelr5t = tk.Label(rec5, anchor='w', justify='left', font=('Ubuntu', '13'))
labelr5t.place(relx=0.15,relwidth=0.8, relheight=1)


root.mainloop()

