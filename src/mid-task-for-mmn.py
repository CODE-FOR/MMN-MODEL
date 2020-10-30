# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import random
from tkinter import *
from tkinter import messagebox

customer_id = 0
server_id = 1
total_time = 0.0
average_customer_arrive_interval = 0.0
average_customer_need_serve_time = 0.0
customer_num = 0
queue_max_length = 0
server_num = 0
customer_queue = []
interval_list = []
need_serve_time_list = []
server_list = []
queue_head = 0
total_wait_time = 0.0
total_person_num = 0
wait_time_list = []
customer_log = open('customer-log.txt', 'w')

# get_input   use tkinter
root = Tk()
root.title('MMN-Model')
root.geometry('300x300')
Label(root, text='平均到达时间').pack()
get_interval_entry = Entry()
get_interval_entry.pack()
Label(root, text='平均服务时间').pack()
get_server_time_entry = Entry()
get_server_time_entry.pack()
Label(root, text='顾客数目').pack()
get_customer_num = Entry()
get_customer_num.pack()
Label(root, text='队列最大长度').pack()
get_length = Entry()
get_length.pack()
Label(root, text='服务台数目').pack()
get_server_num = Entry()
get_server_num.pack()


def get_average_message():
    global root, average_customer_need_serve_time, average_customer_arrive_interval, customer_num, \
        server_num, queue_max_length
    wig_get = root.focus_get()
    if wig_get == get_interval_entry:
        get_server_time_entry.focus_set()
    elif wig_get == get_server_time_entry:
        get_customer_num.focus_set()
    elif wig_get == get_customer_num:
        get_length.focus_set()
    elif wig_get == get_length:
        get_server_num.focus_set()
    else:
        try:
            average_customer_arrive_interval = float(get_interval_entry.get())
            average_customer_need_serve_time = float(get_server_time_entry.get())
            customer_num = int(get_customer_num.get())
            server_num = int(get_server_num.get())
            queue_max_length = int(get_length.get())
            root.quit()
            root.destroy()
        except:
            messagebox.askretrycancel(title='注意', message='检测输入数据的合法性，不能有空数据，而且要求平均到达时间和平均服务时间为浮点数，其余为整数')


confirm_button = Button(root, text='confirm', command=get_average_message)
confirm_button.pack()

root.bind('<Return>', lambda event=None: confirm_button.invoke())

root.mainloop()


# write header

class Customer:
    def __init__(self, arrive_time, need_serve_time):
        self.arrive_time = arrive_time
        self.need_serve_time = need_serve_time
        global customer_id
        self.customer_id = customer_id
        customer_id = customer_id + 1
        self.served = False
        self.wait_time = 0.0

    def be_served(self, serve_time):
        global total_wait_time, total_person_num
        print('person:' + '{:>10} {:>20} {:>20}'.format(str(self.customer_id), 'be served', '') + 'timestamp ' + str(
            total_time), file=customer_log)
        # print('person ' + str(self.customer_id) + " be served" + '%50s' % 'timestamp: ' + str(total_time))
        total_wait_time += serve_time - self.arrive_time - self.need_serve_time
        self.wait_time = serve_time - self.arrive_time - self.need_serve_time
        total_person_num += 1
        wait_time_list.append(serve_time - self.arrive_time - self.need_serve_time)

    def leave(self):
        # print('person ' + str(self.customer_id) + " leave" + '%50s' % 'timestamp: ' + str(total_time))
        print('person:' + '{:>10} {:>20} {:>20}'.format(str(self.customer_id), 'leave', '') + 'timestamp ' + str(
            total_time), file=customer_log)

    def arrive(self):
        global total_time
        # print('person ' + str(self.customer_id) + " arrive" + '%50s' % 'timestamp: ' + str(total_time))
        print('person:' + '{:>10} {:>20} {:>20}'.format(str(self.customer_id), 'arrive', '') + 'timestamp ' + str(
            total_time), file=customer_log)

    def chose_server(self, _server_id):
        global total_time
        print('person:' + '{:>10} {:>20} {:>20}'.format(str(self.customer_id), 'chose server ' + str(_server_id),
                                                        '') + 'timestamp ' + str(total_time), file=customer_log)


class Server:
    def __init__(self):
        self.has_customer = False
        global server_id, total_time
        self.sever_id = server_id
        server_id += 1
        self.next_free_time = 0.0
        self.customer_queue = []
        self.queue_head = 0
        self.queue_length = []
        self.queue_length_timestamp = []
        self.server_serve_time_in_total_time_list = []
        self.server_serve_time_in_total_time_timestamp = []
        self.total_serve_time = 0.0

    def serve_customer(self):
        self.customer_queue[self.queue_head].be_served(self.next_free_time)
        self.customer_queue[self.queue_head].leave()
        self.total_serve_time += self.customer_queue[self.queue_head].need_serve_time
        self.queue_head += 1
        self.queue_length.append(len(self.customer_queue) - self.queue_head)
        self.queue_length_timestamp.append(total_time)
        self.server_serve_time_in_total_time_list.append(self.total_serve_time / total_time)
        self.server_serve_time_in_total_time_timestamp.append(total_time)
        if self.queue_head < len(self.customer_queue):
            self.next_free_time += self.customer_queue[self.queue_head].need_serve_time
        else:
            self.has_customer = False

    def add_customer(self, customer):
        self.customer_queue.append(customer)
        self.queue_length.append(len(self.customer_queue) - self.queue_head)
        self.queue_length_timestamp.append(total_time)
        if not self.has_customer:
            self.has_customer = True
            self.next_free_time = total_time + customer.need_serve_time

    def draw_queue_length_pic(self):
        plt.xlabel('time')
        plt.ylabel('length')
        plt.plot(self.queue_length_timestamp, self.queue_length)
        plt.savefig('pic/server/queue-length/' + str(self.sever_id) + '.jpg')
        plt.close()

        plt.xlabel('time')
        plt.ylabel('usage-rate')
        plt.plot(self.server_serve_time_in_total_time_timestamp, self.server_serve_time_in_total_time_list)
        plt.savefig('pic/server/usage-percent/' + str(self.sever_id) + '.jpg')
        plt.close()

    def generate_html_code_part3(self, file_name):
        total_wait_time_in_this_server = 0.0
        for customer in self.customer_queue:
            total_wait_time_in_this_server += customer.wait_time
        average_queue_length = total_wait_time_in_this_server / total_time
        usage_percent = self.total_serve_time / total_time
        print('    <h5><a name="32' + str(self.sever_id) + '-服务台-' + str(self.sever_id)
              + '" class="md-header-anchor"></a><span>3.2.' + str(self.sever_id) + ' 服务台-' + str(
            self.sever_id) + '</span></h5>', file=file_name)
        print('    <ul>', file=file_name)
        print('        <li><span>平均队列长度：' + str(average_queue_length) + '</span></li>', file=file_name)
        print('        <li><span>利用率：' + str(100 * usage_percent) + '%</span></li>', file=file_name)
        print('    </ul>', file=file_name)

    def generate_html_code_part2(self, file_name):
        print('    <h5><a name="22' + str(self.sever_id) + '-服务台-' + str(self.sever_id)
              + '" class="md-header-anchor"></a><span>2.2.' + str(self.sever_id) + ' 服务台-' + str(
            self.sever_id) + '</span></h5>', file=file_name)
        print('    <ul>', file=file_name)
        print('        <li><p><span>队列长度-时间分布图</span></p>', file=file_name)
        print('            <p><img src="pic/server/queue-length/' + str(
            self.sever_id) + '.jpg" referrerpolicy="no-referrer"></p></li>', file=file_name)
        print('        <li><p><span>服务台利用率-时间分布图</span></p>', file=file_name)
        print('            <p><img src="pic/server/usage-percent/' + str(
            self.sever_id) + '.jpg" referrerpolicy="no-referrer"></p></li>', file=file_name)
        print('    </ul>', file=file_name)


def generate_customers():
    global total_time, interval_list, need_serve_time_list
    _max_interval = 0.0
    _max_need_serve_time = 0.0
    global customer_num
    # draw point pic
    for i in range(customer_num):
        interval = - average_customer_arrive_interval * np.log(1 - random.random())
        interval_list.append(interval)
        if interval > _max_interval:
            _max_interval = interval
        total_time += interval
        need_serve_time = - average_customer_need_serve_time * np.log(1 - random.random())
        need_serve_time_list.append(need_serve_time)
        if need_serve_time > _max_need_serve_time:
            _max_need_serve_time = need_serve_time
        customer_queue.append(Customer(total_time, need_serve_time))
    total_time = 0.0
    return _max_interval, _max_need_serve_time


def draw_interval(_max_interval):
    span = _max_interval / 100
    y = []
    x = []
    left = 0.0
    right = span
    for i in range(100):
        num = 0
        for interval in interval_list:
            if left <= interval < right:
                num += 1
        y.append(num)
        x.append(left)
        left += span
        right += span
    plt.xlabel('interval')
    plt.ylabel('person-num')
    plt.bar(x, y, width=span)
    plt.savefig('pic/customer/interval/interval.jpg')
    plt.close()


def draw_need_serve_time(_max_need_serve_time):
    span = _max_need_serve_time / 100
    y = []
    x = []
    left = 0.0
    right = span
    for i in range(100):
        num = 0
        for need_serve_time in need_serve_time_list:
            if left <= need_serve_time < right:
                num += 1
        y.append(num)
        x.append(left)
        left += span
        right += span
    plt.bar(x, y, width=span)
    plt.xlabel('serve-time')
    plt.ylabel('person-num')
    plt.savefig('pic/customer/need-serve-time/time.jpg')
    plt.close()


def generate_server():
    for i in range(server_num):
        server_list.append(Server())


def draw_wait_time_pic():
    _max_wait_time = 0.0
    for wait_time in wait_time_list:
        if wait_time > _max_wait_time:
            _max_wait_time = wait_time
    span = _max_wait_time / 100
    y = []
    x = []
    left = 0.0
    right = span
    for i in range(100):
        num = 0
        for wait_time in wait_time_list:
            if left <= wait_time < right:
                num += 1
        y.append(num)
        x.append(left)
        left += span
        right += span
    plt.bar(x, y, width=span)
    plt.xlabel('wait-time')
    plt.ylabel('person-num')
    plt.savefig('pic/customer/wait-time/time.jpg')
    plt.close()


def simulate():
    global total_time, queue_head, queue_max_length
    while True:
        earliest_time = float('inf')
        _server = server_list[0]
        continue_simulate = False
        serve = True
        for server_in_loop in server_list:
            if server_in_loop.has_customer and server_in_loop.next_free_time < earliest_time:
                _server = server_in_loop
                earliest_time = server_in_loop.next_free_time
                continue_simulate = True
        if queue_head < len(customer_queue) and customer_queue[queue_head].arrive_time < earliest_time:
            continue_simulate = True
            earliest_time = customer_queue[queue_head].arrive_time
            serve = False
        if not continue_simulate:
            break
        total_time = earliest_time
        if serve:
            _server.serve_customer()
        else:
            has_done = False
            min_queue_length = sys.maxsize
            for server_in_loop in server_list:
                if not server_in_loop.has_customer:
                    customer_queue[queue_head].arrive()
                    customer_queue[queue_head].chose_server(server_in_loop.sever_id)
                    server_in_loop.add_customer(customer_queue[queue_head])
                    queue_head += 1
                    has_done = True
                    break
                if len(server_in_loop.customer_queue) - server_in_loop.queue_head < min_queue_length:
                    _server = server_in_loop
                    min_queue_length = len(server_in_loop.customer_queue) - server_in_loop.queue_head
            if not has_done:
                customer_queue[queue_head].arrive()
                if min_queue_length < queue_max_length:
                    _server.add_customer(customer_queue[queue_head])
                    customer_queue[queue_head].chose_server(_server.sever_id)
                    queue_head += 1
                else:
                    customer_queue[queue_head].leave()
                    queue_head += 1


(max_interval, max_need_serve_time) = generate_customers()
draw_interval(max_interval)
draw_need_serve_time(max_need_serve_time)
generate_server()
simulate()
for server in server_list:
    server.draw_queue_length_pic()
draw_wait_time_pic()

with open('result.html', 'w', encoding='utf-8') as result:
    with open('style.txt', 'r', encoding='utf-8') as style:
        for line in style.readlines():
            result.write(line)
    style.close()
    print('        <li><span>平均到达时间 :' + str(average_customer_arrive_interval) + '</span></li>', file=result)
    print('        <li><span>平均服务时间 :' + str(average_customer_need_serve_time) + '</span></li>', file=result)
    print('        <li><span>顾客数目 :' + str(customer_num) + '</span></li>', file=result)
    print('        <li><span>队列最大长度 :' + str(queue_max_length) + '</span></li>', file=result)
    print('        <li><span>服务台个数 :' + str(server_num) + '</span></li>', file=result)
    print('    </ul>', file=result)
    print('    <h2><a name="2-数据图" class="md-header-anchor"></a><span>2. 数据图</span></h2>', file=result)
    print('    <h3><a name="21-顾客数据" class="md-header-anchor"></a><span>2.1 顾客数据</span></h3>', file=result)
    print('    <ul>', file=result)
    print('        <li><p><span>两顾客相距时间间隔分布图</span></p>', file=result)
    print('            <blockquote><p><span>当数据足够大时，可以显著的看出指数分布的概率密度图样</span></p></blockquote>', file=result)
    print('            <p><img src="pic/customer/interval/interval.jpg" referrerpolicy="no-referrer"></p></li>',
          file=result)
    print('        <li><p><span>顾客所需服务时间分布图</span></p>', file=result)
    print('            <blockquote><p><span>当数据足够大时，可以显著的看出指数分布的概率密度图样</span></p></blockquote>', file=result)
    print('            <p><img src="pic/customer/need-serve-time/time.jpg" referrerpolicy="no-referrer"></p></li>',
          file=result)
    print('        <li><p><span>等待时间分布图</span></p>', file=result)
    print('            <p><img src="pic/customer/wait-time/time.jpg" referrerpolicy="no-referrer"></p></li>',
          file=result)
    print('    </ul>', file=result)
    for server in server_list:
        server.generate_html_code_part2(result)
    print('    <h2><a name="3-所得数据" class="md-header-anchor"></a><span>3. 所得数据</span></h2>', file=result)
    print('    <h3><a name="31-顾客" class="md-header-anchor"></a><span>3.1 顾客</span></h3>', file=result)
    print('    <ul>', file=result)
    print('        <li><span>平均等待时间：' + str(total_wait_time / total_person_num) + '</span></li>', file=result)
    print('        <li><span>详细信息请查看</span><a href=\'customer-log.txt\'><code>customer-log</code></a></li>',
          file=result)
    print('    </ul>', file=result)
    print('    <h3><a name="32-服务台" class="md-header-anchor"></a><span>3.2 服务台</span></h3>', file=result)
    for server in server_list:
        server.generate_html_code_part3(result)
    print('    <p>&nbsp;</p></div>', file=result)
    print('</body>', file=result)
    print('</html>', file=result)
result.close()

os.system('result.html')
