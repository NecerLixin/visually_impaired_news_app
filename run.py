import asyncio
from pyppeteer import launch
from app import create_app
import nest_asyncio
# 全局浏览器实例
browser = None
loop = None

async def init_browser():
    print("浏览器初始化")
    return await launch(headless=True,autoClose=False)

async def keep_browser_running():
    global browser
    browser = await init_browser()
    while True:
        await asyncio.sleep(100) 
    # while True:

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
browser = loop.run_until_complete(init_browser())  
# loop.run_until_complete(keep_browser_running()) 
# loop.run_forever()


app = create_app(browser,loop)
# app.run(debug=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    # browser = loop.run_until_complete(init_browser())  
    # loop.create_task(keep_browser_running())
    
    app = create_app(browser,loop)
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(browser.close())
    