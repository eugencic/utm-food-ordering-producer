from flask import Flask, request
from threading import Thread
import requests
import random
from time import sleep
from products import products

app = Flask(__name__)

threads = []

@app.route('/producer', methods = ['GET', 'POST'])

def producer():
    data = request.get_json()
    print(f'Order nr.{data["order_id"]} is received to client nr.{data["client_id"]}\n')
    sleep(3)
    return {'isSuccess': True}

def create_client(name):
    try:
        client_id = name
        product = random.choice(products)
        order_id = int(random.random() * random.random() / random.random() * 1000)
        payload = dict({'order_id': order_id, 'client_id': client_id, 'product_id': product['id']})
        print(f"Client nr.{name} has ordered a {product['name']} which costs {product['price']}$. Order nr.{order_id} is sent to the delivery service\n")
        requests.post('http://localhost:4040/producer_aggregator', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass

def run_producer():
    producer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 4000, debug = False, use_reloader = False), daemon = True)
    threads.append(producer_thread)
    sleep(2)
    client_thread_name = 1
    for _ in range(7):
        client_thread = Thread(target = create_client, args = (client_thread_name,), name = str(client_thread_name))
        threads.append(client_thread)
        client_thread_name += 1
    for thread in threads:
        thread.start()
        sleep(3)
    for thread in threads:
        thread.join()
   
if __name__ == '__main__':
    run_producer()