import os, asyncio
from sanic_script import Manager
from app import create_app

app = create_app('development')
manager = Manager(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
    # serv_coro = app.create_server(host="0.0.0.0", port=8000, debug=True, return_asyncio_server=True)
    # loop = asyncio.get_event_loop()
    # serv_task = asyncio.ensure_future(serv_coro, loop=loop)
    # server = loop.run_until_complete(serv_task)
    # server.after_start()
    # try:
    #     loop.run_forever()
    # except KeyboardInterrupt as e:
    #     loop.stop()
    # finally:
    #     server.before_stop()
    #
    #     # Wait for server to close
    #     close_task = server.close()
    #     loop.run_until_complete(close_task)
    #
    #     # Complete all tasks on the loop
    #     for connection in server.connections:
    #         connection.close_if_idle()
    #     server.after_stop()
    #manager.run()
