from django.shortcuts import render
from django.http import HttpResponse

from threading import Thread
import queue

from yahoo_fin.stock_info import tickers_nifty50, get_quote_table


def stockPicker(request):
    stockpicker = tickers_nifty50()
    return render(request, 'core/stockpicker.html', {'stockpicker': stockpicker})

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    # print(stockpicker)    
    data = {}
    available_stocks = tickers_nifty50()
    for stock in stockpicker:
        if stock not in available_stocks:
            return HttpResponse('<h1>Invalid Stock</h1>')
        # else:
        #     details = get_quote_table(stock)
        #     data.update({i : details})
    
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

    print(data)    
    


    return render(request, 'core/stocktracker.html', {"data": data, 'room_name': 'track'})
