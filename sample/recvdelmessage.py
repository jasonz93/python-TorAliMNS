#!/usr/bin/env python
#coding=utf8

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import time
from .sample_common import MNSSampleCommon
from toralimns.account import Account
from toralimns.queue import *

#从sample.cfg中读取基本配置信息
## WARNING： Please do not hard code your accessId and accesskey in next line.(more information: https://yq.aliyun.com/articles/55947)
accid,acckey,endpoint,token = MNSSampleCommon.LoadConfig()

#初始化 my_account, my_queue
my_account = Account(endpoint, accid, acckey, token)
queue_name = sys.argv[1] if len(sys.argv) > 1 else "MySampleQueue"
base64 = False if len(sys.argv) > 2 and sys.argv[2].lower() == "false" else True
my_queue = my_account.get_queue(queue_name)
my_queue.set_encoding(base64)


#循环读取删除消息直到队列空
#receive message请求使用long polling方式，通过wait_seconds指定长轮询时间为3秒

## long polling 解析:
### 当队列中有消息时，请求立即返回；
### 当队列中没有消息时，请求在MNS服务器端挂3秒钟，在这期间，有消息写入队列，请求会立即返回消息，3秒后，请求返回队列没有消息；

wait_seconds = 3
print("%sReceive And Delete Message From Queue%s\nQueueName:%s\nWaitSeconds:%s\n" % (10*"=", 10*"=", queue_name, wait_seconds))
while True:
    #读取消息
    try:
        recv_msg = my_queue.receive_message(wait_seconds)
        print("Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id))
    except MNSExceptionBase as e:
        if e.type == "QueueNotExist":
            print("Queue not exist, please create queue before receive message.")
            sys.exit(0)
        elif e.type == "MessageNotExist":
            print("Queue is empty!")
            sys.exit(0)
        print("Receive Message Fail! Exception:%s\n" % e)
        continue

    #删除消息
    try:
        my_queue.delete_message(recv_msg.receipt_handle)
        print("Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle)
    except MNSExceptionBase as e:
        print("Delete Message Fail! Exception:%s\n" % e)
