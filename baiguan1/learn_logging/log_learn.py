# !/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

logger = logging.getLogger('WUba')
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s-%(name)s-%(lineno)s-%(levelname)s-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('often makes a very good meal of %s', 'visiting tourists')