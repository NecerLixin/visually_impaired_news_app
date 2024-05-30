class StatusCode:
    CODE_FINISTH = 200
    CODE_SYTAX_ERROR = 400
    CODE_UNDERSTAND_REFUSE = 403
    CODE_CANT_FINISHT = 406
    
def get_brief(content:list,length=60)->str:
    """
    根据content构建一个新闻简

    Args:
        content (list): 新闻content列表

    Returns:
        str: 新闻简介
    """
    text_list = [sample['data'] for sample in content if sample['type']=="text"]
    text = "".join(text_list)
    if len(text) > length:
        return text[:length] + "……"
    else:
        return text + "……"