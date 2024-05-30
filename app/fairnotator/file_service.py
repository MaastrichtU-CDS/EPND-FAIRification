import logging
import chardet


log = logging.getLogger('django')

def build_mapping():
    log.info("Building mapping")

def determine_encoding(blob):
    result = chardet.detect(blob)
    encoding = result['encoding']
    log.debug(f'Encoding: {encoding}')
    return encoding
