import socket
import threading
import sys

global ports_open_list
global threads_finished_list
global finish_nr_threads

ports_open_list = []
threads_finished_list = []
finish_nr_threads = 0

def create_socket(host,port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(0.5)
	try:
		sock.connect((host, port))
		return True
	except:
		return False

def generate_all_ips(ip1,ip2):
	ip_list_1 = []
	ip_list_2 = []
	ip_list_1 = ip1.split(".")
	ip_list_2 = ip2.split(".")
	for x in range(len(ip_list_1)):
		ip_list_1[x] = int(ip_list_1[x])
		ip_list_2[x] = int(ip_list_2[x])
	for x1 in range(ip_list_1[0],ip_list_2[0]+1):
		for x2 in range(ip_list_2[1],ip_list_2[1]+1):
			for x3 in range(ip_list_1[2],ip_list_2[2]+1):
				for x4 in range(ip_list_1[3],ip_list_2[3]+1):
					print(str(x1)+"."+str(x2)+"."+str(x3)+"."+str(x4))

def scan_port_range(ip_address,start,finish):
	for x in range(start,finish+1):
		open_socket = create_socket(ip_address,x)
		if(open_socket):
			print("Port " + str(x) + " is open.")
			ports_open_list.append(x)
	threads_finished_list.append(1)

def scan_ports(ip_address,threads_nr,port_range_1,port_range_2):
	print("Started looking for open ports on ip: "+ip_address)
	print("")
	threads_list = []
	thread_jump = int((port_range_2-port_range_1)/threads_nr)
	ok_finish = 0
	for y in range(port_range_1,port_range_2,thread_jump):
		threads_list.append(threading.Thread(target=scan_port_range, args=(ip_address,y,y+thread_jump,)))
		threads_list[ len(threads_list) - 1 ].start()
	'''for q in threads_list:
		q.start()'''
	
	#freeze to wait for threads to finish
	while (ok_finish == 0):
		if(len(threads_finished_list) == threads_nr):
			ok_finish = 1

	ports_open_list.sort()

def print_ports(arr):
	print("")
	print("Port scanning results are: ")
	for x in arr:
		print("Port " + str(x) + " is open.")

target_ip = "127.0.0.1"
number_of_threads = 100
port_range_1 = 0
port_range_2 = 1000

for x in range(1,len(sys.argv)):
	t = sys.argv[x]
	cmd = t.split("=")
	cmd_target = cmd[0]
	cmd_val = cmd[1]
	if(cmd_target == "ip"):
		target_ip = cmd_val
	elif(cmd_target == "number_of_threads"):
		number_of_threads = int(cmd_val)
	elif(cmd_target == "port_range"):
		q = cmd_val.split("-")
		port_range_1 = int(q[0])
		port_range_2 = int(q[1])

#print(target_ip)

scan_ports(target_ip,number_of_threads,port_range_1,port_range_2)
print_ports(ports_open_list)
