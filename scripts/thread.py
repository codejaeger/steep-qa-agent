import time
from getkeys import key_check
from threading import Thread 
g = [] 
def keycomm_append(stop):
	while True:
		p = key_check()
		# print(p?)
		ch = ''
		if 'A' in p:
			ch = 'A'
		elif 'D' in p:
			# g.append('D')
			ch ='D'
		elif 'space' in p:
			# g.append('space')
			ch = 'space'
		if len(g)==0:
			g.append(ch)
		elif g[len(g)-1]!=ch:
			g.append(ch)
		if stop():
			break
def useit():
	f=0
	stop = False
	t = Thread(target = keycomm_append , args=(lambda : stop, ))
	t.start()
	while f<4:
		f+=1
		time.sleep(1)
		if len(g)!=0:
			print(g[0])
			del g[0]
	print("I am")
	stop=True
	t.join()
useit()