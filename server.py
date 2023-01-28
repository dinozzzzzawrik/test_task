import aiohttp
from aiohttp import web
import aiohttp_cors
import json
import asyncio
import os
import uuid
from google.cloud import storage

# create a client for interacting with the Google Cloud Storage API
client = storage.Client()

# specify the bucket to use
bucket_name = 'my-bucket'
bucket = client.bucket(bucket_name)

async def handle_put(request):
    data = await request.read()
    filename = request.query.get('filename')
    if not filename:
        filename = str(uuid.uuid4())
    blob = bucket.blob(filename)
    await blob.upload_from_string(data)
    return web.Response(text='File saved')

async def handle_get(request):
    filename = request.query.get('filename')
    if not filename:
        return web.Response(text='Please provide a filename')
    blob = bucket.blob(filename)
    data = await blob.download_as_string()
    return web.Response(body=data)

app = web.Application()

# setup CORS
cors = aiohttp_cors.setup(app)

resource = cors.add(app.router.add_resource("/"))

cors.add(resource.add_route("PUT", handle_put))
cors.add(resource.add_route("GET", handle_get))

web.run_app(app)
