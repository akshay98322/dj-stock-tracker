from celery import shared_task
from channels.layers import get_channel_layer
from threading import Thread
import queue
import asyncio

from yahoo_fin.stock_info import tickers_nifty50, get_quote_table

@shared_task(bind=True)
def update_stocks(self, stock_picker):
    data = {}
    available_stocks = tickers_nifty50()
    for stock in stock_picker:
        if stock not in available_stocks:
            stock_picker.remove(stock)    
    n_threads = len(stock_picker)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stock_picker[i]: get_quote_table(arg1)}), args = (que, stock_picker[i]))
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