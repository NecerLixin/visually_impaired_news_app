import asyncio
from pyppeteer import launch
from app import create_app
import nest_asyncio
from app import loop,browser
# 全局浏览器实例
# browser = None
# loop = None


# loop.run_until_complete(keep_browser_running()) 
# loop.run_forever()


app = create_app()
# app.run(debug=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    # browser = loop.run_until_complete(init_browser())  
    # loop.create_task(keep_browser_running())
    
    app = create_app()
    app.run(debug=True)
    # try:
    #     app.run()
    # except Exception:
    #     # loop.run_until_complete(browser.close())
    #     print("exit")
    # finally:
    #     loop.run_until_complete(browser.close())
    #     loop.stop()
    