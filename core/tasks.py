from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue
from channels.layers import get_channel_layer
import asyncio


@shared_task(bind=True)
def update_stock(self, stockpicker):
    data = {}
    available_stocks = tickers_nifty50()
    for stock in stockpicker:
        if stock not in available_stocks:
            stockpicker.remove(stock)    
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        res = que.get()
        data.update(res)
    
    # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", { 
        'type': "send_stock_update",
        'message': data,
        }))


    return 'complete' 