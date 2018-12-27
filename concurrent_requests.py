#!/usr/local/bin/python3.7

import asyncio
from aiohttp import ClientSession
import json
import time

# async, await, and the module asyncio are native to python after version 3.5
# async keywork makes the function asynchronous 
# async functions do not return a result immediately, instead they return generators which need to be iterated over 
# 'await' iterates over the generator function and 'awaits' for an actual response
async def fetch(url, session):
    # sending a dummy payload to my server
    data = {
        "payload": "some payload"
    }

    # asynchronous post request that will give my program the 'concurrent' functionality
    # keyword 'with' makes sure to close the connection after every post request
    # important takeaway: in python, the data dictionary must be passed into jason.dumps() in order to successfully make the post request 
    async with session.post(url, data=json.dumps(data)) as response:
        # return the status of the async post request, 200 if successful
        return response.status

async def run(r):
    # url to my local server with my post route
    url = "http://0.0.0.0:5000/api/post"
    # headers with dummy api key
    headers = {
        "Content-type": "application/json",
        "x-api-key": "test123"
    }
    # list where all of the async reponses will be stored
    tasks = []

    # storing the time that our program begins to run to see how long this concurrent process takes.
    start = time.time()

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    # pass in the same headers for all requests
    async with ClientSession(headers=headers) as session:
        for i in range(r):
            # ensure_future() awaits the response of the asynchrownouse function fetch() and turns them to Future objects to be executed in the event loop
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        # you now have all response bodies in this variable
        # .gather() waits for all tasks to return a response
        responses = await asyncio.gather(*tasks)
        
        # the time that our program finished with the concurrent post requests
        end = time.time()
        # number of calls made
        print("CALLS: ", len(responses))
        # number of responses that were not of a status code 200
        print("ERRORS: ", len(responses) - responses.count(200))
        # total time elapsed 
        print("TIME: {0:.4f}".format(round(end - start,4)), "seconds")

# create an event loop to be able to use this asynchronous functionality
loop = asyncio.get_event_loop()
# turning our tasks to asyncio Future objects to be able to run them in the loop
# r is the number of concurrent requests we want to do
future = asyncio.ensure_future(run(10))
loop.run_until_complete(future)