import asyncio
import json

import aiohttp

from .exception import (
    DingTalkError,
    DingTalkTimeoutError,
)


class DingTalkRobot:

    GATEWAY_URL = 'https://oapi.dingtalk.com/robot/send?access_token={}'

    def __init__(self, access_token, timeout=5):
        conn = aiohttp.TCPConnector(limit=1024)
        self.session = aiohttp.ClientSession(connector=conn)
        self.access_token = access_token
        self.timeout = timeout

    async def _do_post(self, params):
        url = self.GATEWAY_URL.format(self.access_token)
        try:
            async with self.session.post(url, json=params,
                                         timeout=self.timeout) as resp:
                if resp.status != 200:
                    raise DingTalkError()
                body = await resp.text()
                result = json.loads(body)
                errcode = result.get('errcode', 0)
                if errcode != 0:
                    error = DingTalkError(errcode, result.get('errmsg'))
                    raise error
                return result
        except asyncio.TimeoutError:
            raise DingTalkTimeoutError()

    def __add_misc(self, msg, recipients, to_all):
        if recipients:
            msg['at'] = {
                'atMobiles': recipients
            }
        if to_all:
            msg['at'] = {
                'isAtAll': True
            }

    async def send_text(self, text, recipients=None, to_all=False):
        msg = {
            'msgtype': 'text',
            'text': {
                'content': text
            },
        }
        self.__add_misc(msg, recipients, to_all)
        await self._do_post(msg)

    async def send_markdown(self, title, markdown_text,
                            recipients=None, to_all=False):
        msg = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': markdown_text,
            },
        }
        self.__add_misc(msg, recipients, to_all)
        await self._do_post(msg)

    def __del__(self):
        if not self.session.closed:
            if self.session._connector is not None \
                    and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None
