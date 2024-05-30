from app import create_app, socketio


# 全局浏览器实例
# browser = None
# loop = None


# loop.run_until_complete(keep_browser_running()) 
# loop.run_forever()


app = create_app()
# app.run(debug=True)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop) 
    # browser = loop.run_until_complete(init_browser())  
    # loop.create_task(keep_browser_running())
    
    # app = create_app()
    # app.run(debug=True)
    socketio.run(app,host='127.0.0.1',port=5001)

    