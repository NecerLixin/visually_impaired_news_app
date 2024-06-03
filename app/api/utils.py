class StatusCode:
    CODE_FINISTH = 200
    CODE_SYTAX_ERROR = 400
    CODE_UNDERSTAND_REFUSE = 403
    CODE_CANT_FINISHT = 406


def get_content(content:list,title:str)->str:
    """
    根据content返回一个内容字符串

    Args:
        content (list): 内容列表,
        title (str): 新闻标题

    Returns:
        str: 新闻文本字符串
    """
    text_list = [sample['data'] for sample in content if sample['type']=="text"]
    text = "".join(text_list)
    text = title + text
    return text



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

