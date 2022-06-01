from django.shortcuts import render
from django.http import HttpResponse

from threading import Thread
import queue

from yahoo_fin.stock_info import tickers_nifty50, get_quote_table



def stockPicker(request):
    stock_picker = tickers_nifty50()
    return render(request, 'core/stockpicker.html', {'stock_picker': stock_picker})

def stockTracker(request):
    user_stocks = request.GET.getlist('stockpicker')
    # print(user_stocks)    
    data = {}
    available_stocks = tickers_nifty50()
    for stock in user_stocks:
        if stock not in available_stocks:
            return HttpResponse('<h1>Invalid Stock</h1>')
        # else:
        #     details = get_quote_table(stock)
        #     data.update({i : details})
    
    n_threads = len(user_stocks)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({user_stocks[i]: get_quote_table(arg1)}), args = (que, user_stocks[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        res = que.get()
        data.update(res)

    print(data)    
    


    return render(request, 'core/stocktracker.html', {"data": data})
