import queue
from threading import Thread

from django.shortcuts import render
from django.http import HttpResponse

from asgiref.sync import sync_to_async
from yahoo_fin.stock_info import tickers_nifty50, get_quote_table


def stockPicker(request):
    stockpicker = tickers_nifty50()
    return render(request, 'core/stockpicker.html', {'stockpicker': stockpicker})

@sync_to_async
def checkAuth(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

async def stockTracker(request):
    is_logged = await checkAuth(request)
    if not is_logged:
        return HttpResponse("You are not logged in")
    stockpicker = request.GET.getlist('stockpicker')
    data = {}
    available_stocks = tickers_nifty50()
    for stock in stockpicker:
        if stock not in available_stocks:
            return HttpResponse('<h1>Invalid Stock</h1>')
    
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

    return render(request, 'core/stocktracker.html', {"data": data, 'room_name': 'track'})
