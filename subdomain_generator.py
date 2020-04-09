import requests
import threading
import sys

global subdomain_choice
global subdomain_file
global file
global content
global content_split
global threads_nr
global thread_list

def check_subdomain(sub):
	random_subdomain = sub + "." + subdomain_choice
	random_subdomain = "http://" + random_subdomain
	try:
		r = requests.get(random_subdomain,timeout=1)
		subdomain_file.write(random_subdomain+"\n")
		print(random_subdomain)
	except:
		do_nothing = 0

def subdomain_range_generator(start,finish,content_split):
	if( finish > len(content_split) ):
		finish = len(content_split)
	for x in range(start,finish):
		check_subdomain(content_split[x])

def generate_subdomains(threads_nr):
	file = open(target_subdomain_text_file,"r")
	content = file.read()
	content_split = content.split("\n")
	jmp_nr = int(len(content_split)/threads_nr)
	for y in range(0,len(content_split),jmp_nr):
		thread_list.append(threading.Thread( target=subdomain_range_generator, args=(y,y+jmp_nr,content_split,)) )
		thread_list[ len(thread_list) - 1 ].start()

thread_list = []

target_subdomain_text_file = "subdomain_word_list_500.txt"
subdomain_file = "full_subdomain.txt"
subdomain_choice = "historia.ro"

threads_nr = 100

#file = open(target_subdomain_text_file,"r")
#content = file.read()
#content_split = content.split("\n")

for x in range(1,len(sys.argv)):
	t = sys.argv[x]
	cmd = t.split("=")
	cmd_target = cmd[0]
	cmd_val = cmd[1]
	if(cmd_target == "target_subdomain_text_file"):
		target_subdomain_text_file = str(cmd_val)
	elif(cmd_target == "subdomain_file"):
		subdomain_file = str(cmd_val)
	elif(cmd_target == "subdomain_choice"):
		subdomain_choice = str(cmd_val)
	elif(cmd_target == "threads_nr"):
		threads_nr = int(cmd_val)

subdomain_file = open(subdomain_file,"w+")

generate_subdomains(threads_nr)

#check_subdomain("admin")
