import asyncio
import json
import urllib.parse

import aiohttp

from .exception import (
    DingTalkError,
    DingTalkTimeoutError,
)


class DingTalkApi:

    API_HOST = 'https://oapi.dingtalk.com'

    def __init__(self, timeout=5):
        conn = aiohttp.TCPConnector(limit=1024)
        self.session = aiohttp.ClientSession(connector=conn)
        self.timeout = timeout

    async def get_token(self, app_key, app_secret):
        path = '/gettoken'
        url = urllib.parse.urljoin(self.API_HOST, path)
        params = {
            'appkey': app_key,
            'appsecret': app_secret,
        }
        result = await self.__do_get(url, params)
        return result.get('access_token')

    async def send_text_message(self, access_token, user_ids, agent_id, text):
        """
        :param access_token: access token
        :param user_ids: 用户id列表
        :param agent_id: 应用id
        :param text: 要发送的内容
        :return:
        """
        msg_obj = {
            'msgtype': 'text',
            'text': {
                'content': text
            },
        }
        return await self.__do_send_msg(access_token, user_ids, agent_id,
                                        msg_obj)

    async def send_markdown_message(self, access_token, user_ids, agent_id,
                                    title, markdown_text):
        """
        :param access_token: access token
        :param user_ids: 用户id列表
        :param agent_id: 应用id
        :param title: 消息标题
        :param markdown_text: 要发送的markdown内容
        :return:
        """
        msg_obj = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': markdown_text
            }
        }
        return await self.__do_send_msg(access_token, user_ids, agent_id,
                                        msg_obj)

    async def __do_send_msg(self, access_token, user_ids, agent_id, msg_obj):
        path = '/message/send?access_token={}'.format(access_token)
        url = urllib.parse.urljoin(self.API_HOST, path)
        if isinstance(user_ids, list):
            to_user = '|'.join(user_ids)
        else:
            to_user = user_ids
        msg_obj.update({
            'touser': to_user,
            'agentid': agent_id,
        })
        return await self.__do_post(url, msg_obj)

    async def __do_get(self, url, params):
        try:
            async with self.session.get(url, params=params,
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

    async def __do_post(self, url, params):
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

    def __del__(self):
        if not self.session.closed:
            if self.session._connector is not None \
                    and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None
