import multiprocessing


bind = '127.0.0.1:7220'
worker_class = 'aiohttp.worker.GunicornWebWorker'
workers = multiprocessing.cpu_count() + 1
max_requests = 5000
reload = True
user = 'cck'
