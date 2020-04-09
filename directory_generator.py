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
	random_subdomain = subdomain_choice
	if(random_subdomain[0:4] == "www."):
		random_subdomain = "http://" + subdomain_choice
	elif not( random_subdomain[0:7] == "http://" or random_subdomain[0:8] == "https://" ):
		random_subdomain = "http://" + subdomain_choice

	if(random_subdomain[ len(random_subdomain) - 1 ] != "/"):
		random_subdomain += "/"

	random_subdomain += sub

	#print(random_subdomain)

	try:
		r = requests.get(random_subdomain,timeout=1)
		if(r.status_code != 404):
			subdomain_file.write(random_subdomain+"\n")
			print(random_subdomain)
		else:
			print("Folder not present on server "+random_subdomain)
	except:
		print("Error with domain "+random_subdomain)
		do_nothing = 0

def domain_range_generator(start,finish,content_split):
	random_sum = 0
	if( finish > len(content_split) ):
		finish = len(content_split)
	for x in range(start,finish):
		check_subdomain(content_split[x])
		random_sum += 1
	print(random_sum)

def generate_subdomains(threads_nr):
	file = open(target_subdomain_text_file,"r")
	content = file.read()
	content_split = content.split("\n")
	jmp_nr = int(len(content_split)/threads_nr)
	for y in range(0,len(content_split),jmp_nr):
		thread_list.append(threading.Thread( target=domain_range_generator, args=(y,y+jmp_nr,content_split,)) )
		#print(str(y)+" "+str(y+jmp_nr))
		thread_list[ len(thread_list) - 1 ].start()

thread_list = []

target_subdomain_text_file = "directory_word_list_small.txt"
subdomain_file = "full_directory.txt"
subdomain_choice = "https://www.historia.ro"

threads_nr = 100

#file = open(target_subdomain_text_file,"r")
#content = file.read()
#content_split = content.split("\n")

for x in range(1,len(sys.argv)):
	t = sys.argv[x]
	cmd = t.split("=")
	cmd_target = cmd[0]
	cmd_val = cmd[1]
	if(cmd_target == "target_directory_text_file"):
		target_subdomain_text_file = str(cmd_val)
	elif(cmd_target == "directory_file"):
		subdomain_file = str(cmd_val)
	elif(cmd_target == "url_choice"):
		subdomain_choice = str(cmd_val)
	elif(cmd_target == "threads_nr"):
		threads_nr = int(cmd_val)

subdomain_file = open(subdomain_file,"w+")

generate_subdomains(threads_nr)

#check_subdomain("special")
