import my_ping
import my_tracert


ip = input("Please enter your ip address: ")
cidr = input("Please enter your cidr: ")

result_message = my_ping.multi_ping(ip, cidr)
lst=[]
rtr_list=[]
for i in result_message[0]:
    ls = my_tracert.route(i)
    print(f"{i}: {ls}")
    lst.append(ls)
    print(lst)
# Find the shortest array
sho = min(lst, key=len)

# Print the last value
rtr=sho[-1]
print(f'this is shortest: {rtr}')




