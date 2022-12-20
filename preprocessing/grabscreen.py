import pytesseract as pt
import time
from matplotlib import pyplot as plt
from PIL import Image
import PIL.ImageGrab
import pytesseract as pt
import numpy as np
import cv2

"""
This function grabs the whole screen.
"""
def grab_screen():
	im = PIL.ImageGrab.grab()
	mg = np.array(im)
	# vertices = np.array([[],[],[],[]],dtype=np.int32)
	return mg
"""
This function captures the relevant part of the screen a.k.a the region of interest.
"""
def rel_mg(img):
	mg = img[80:760,580:1070]
	return mg
	"""
	This fucntion captures portion of screen that has the total score , and applies OCR on it . 
	"""
def get_scoretot(img,rew):
	# mg = np.array(image)
	mg = img[740:760,175:243]
	ret,thresh1 = cv2.threshold(mg,180,255,cv2.THRESH_BINARY)          #thresholding the numbers using their distinct color
	# mgg = cv2.GaussianBlur(thresh1,(5,5),0)
	th2 = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)                   #rgb to grayscale
	ret,thr2 = cv2.threshold(th2,180,255,cv2.THRESH_BINARY_INV)        #getting the numbers in black and background white
	# mg = cv2.GaussianBlur(mg,(5,5),0)
	mgi = cv2.resize(thr2 , None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)    #this resizes the image
	ii = Image.fromarray(mgi)
	ocr = pt.image_to_string(ii, lang='eng',config='--psm 10 tessedit_char_whitelist=0123456789')      #this is the OCR filtering step , the config parameter improves results 
	t=""
	"""some hacks based on common places of misreadings
	"""
	if ocr!='':
		for i in ocr:
			if i!=' ':
				t+=i
			elif i=='Q' or i=='O':
				t+='0'
			elif t=='B':
				t+='8'
			elif t=='&':
				t+='6'
		try:
			return int(t)
		except:
			return rew
	else:
		return rew
# def get_tempscore(img):
# 	# mg = np.array(image)
# 	mg = img[610:640,84:117]
# 	mg = cv2.resize(mg, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# 	mg = cv2.GaussianBlur(mg, (5, 5), 0)
# 	img = Image.fromarray(mg)
# 	ocr = pt.image_to_string(img,config='digits')
# 	t=""
# 	if ocr=='':
# 		return 0
# 	else:
# 		for i in ocr:
# 			if i!=' ':
# 				if t=='B':
# 					t+='8'
# 				elif t=='O':
# 					t+='0'
# 				else:
# 					t+=i
# 		try:
# 			st=int(t)
# 			return st
# 		except ValueError:
# 			return 0
# def roi(img, vertices):
#     mask = np.zeros_like(img)
#     cv2.fillPoly(mask, vertices, 255)
#     masked = cv2.bitwise_and(img, mask)
#     return masked
def temp_score(img,rew):
	mg = img[778:810,178:240]
	hsv = cv2.cvtColor(mg, cv2.COLOR_BGR2HSV)
	lower = np.array([90,110,100])
	upper = np.array([140,255,255])
	mask = cv2.inRange(hsv, lower, upper)
	res = cv2.bitwise_and(mg,mg, mask= mask)
	mg = cv2.resize(res, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
	# mg = cv2.GaussianBlur(mg, (5, 5), 0)
	ret,thr2 = cv2.threshold(mg,180,255,cv2.THRESH_BINARY_INV)
	ii = Image.fromarray(thr2)
	ocr = pt.image_to_string(ii , lang='eng',config='--psm 10 tessedit_char_whitelist=0123456789')
	if ocr!='':
		try:
			return int(t)
		except:
			return rew
	else:
		return rew
	"""
	some hack to check whether the player is knocked out or not
	"""
def checkko(img):
    # im = PIL.ImageGrab.grab(bbox=(0,0,800,860)) 
    # img = np.array(im)
	mg = img[650:670,1420:1480]
#     mg = cv2.GaussianBlur(mg, (5, 5), 0)
    # img = Image.fromarray(mg)
    # img.show()
	ret,thresh1 = cv2.threshold(mg,180,255,cv2.THRESH_BINARY)
# mgg = cv2.GaussianBlur(thresh1,(5,5),0)
	th2 = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
	ret,thr2 = cv2.threshold(th2,180,255,cv2.THRESH_BINARY_INV)
	ii = Image.fromarray(thr2)
	ocr = pt.image_to_string(ii , lang='eng',config='--psm 10 tessedit_char_whitelist=0123456789')
    # print(ocr+"Hi")
    # time.sleep(2)
	if ocr=="Zoom":
		return True
	else:
		return False
	"""
	Function to aggregate all the data into one and return to the call Steep.py
	"""
def getinfo(tot_reward,temp_reward):
	im = grab_screen()
	relim = rel_mg(im)
	tempscore = temp_reward
	totscore = get_scoretot(im,tot_reward)
	if totscore - tot_reward <= 0:
		tempscore = temp_score(im,temp_reward)
	# check = check_fall(im)
	check_ko = checkko(im)
	return relim,totscore,tempscore,check_ko
# while(True):
# 	relim,tempscore,totascore,check = getinfo()
# 	print(check,tempscore,totascore)
# 	time.sleep(0.1)