import logging


def print_placeholder(level):
    """
    打印日志占位符，用来分布不同区域内容
    """
    if level == 'INFO':
        logging.info('{0:-^40}'.format('-'))
    elif level == 'DEBUG':
        logging.debug('{0:-^40}'.format('-'))
    elif level == 'WARNING':
        logging.warning('{0:-^40}'.format('-'))
