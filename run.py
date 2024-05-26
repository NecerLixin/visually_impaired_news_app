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
# 初始化浏览器
# loop = asyncio.get_event_loop()
# asyncio.set_event_loop(loop)
# browser = loop.run_until_complete(init_browser())
# loop.close()
# app = create_app(browser,loop)
nest_asyncio.apply()
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
print(11111)
browser = loop.run_until_complete(init_browser())
# loop.stop()
app = create_app(browser,loop)
# app.run(debug=True)

if __name__ == '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    print(11111)
    browser = loop.run_until_complete(init_browser())
    # loop.stop()
    
    app = create_app(browser,loop)
    app.run(debug=True)