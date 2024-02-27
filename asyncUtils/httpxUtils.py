#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Lu
# @Desc: { http客户端 }
# @Date: 2024/01/10 09:33
import asyncio
from datetime import timedelta

import httpx

# 参考博客：http://t.csdnimg.cn/U492l

class RespFmt():
    """http响应格式"""
    JSON = "json"
    BYTES = "bytes"
    TEXT = "text"


class HttpMethod:
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AsyncHttpClient:
    """异步HTTP客户端"""

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None, resp_fmt: RespFmt = RespFmt.JSON):
        """构造异步HTTP客户端"""
        self.default_timeout = timeout
        self.default_headers = headers or {}
        self.default_resp_fmt = resp_fmt
        self.client = httpx.AsyncClient()
        self.response: httpx.Response = None

    async def _request(self, method: HttpMethod, url: str, params: dict = None, data: dict = None,
                       timeout: timedelta = None, **kwargs):
        """内部请求实现方法

        创建客户端会话,构造并发送HTTP请求,返回响应对象

        Args:
            method: HttpMethod 请求方法, 'GET', 'POST' 等
            url: 请求URL
            params: 请求查询字符串参数字典
            data: 请求体数据字典
            timeout: 超时时间,单位秒
            kwargs: 其他关键字参数

        Returns:
            httpx.Response: HTTP响应对象
        """
        timeout = timeout or self.default_timeout
        headers = self.default_headers or {}
        self.response = await self.client.request(method=method.value, url=url,
                                                  params=params,
                                                  data=data,
                                                  headers=headers,
                                                  timeout=timeout.total_seconds(),
                                                  **kwargs
                                                  )
        return self.response

    async def post(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = RespFmt.JSON, **kwargs):
        """POST请求
        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict or bytes
        """
        await self._request(HttpMethod.POST, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    def _parse_response(self, resp_fmt: RespFmt = None):
        """解析响应
        Args:
            resp_fmt: 响应格式

        Returns:
            resp Union[dict, bytes, str]
        """
        resp_fmt = resp_fmt or self.default_resp_fmt
        resp_content_mapping = {
            RespFmt.JSON: self.json,
            RespFmt.BYTES: self.bytes,
            RespFmt.TEXT: self.text,
        }
        resp_func = resp_content_mapping.get(resp_fmt)
        return resp_func()

    def json(self):
        return self.response.json()

    def bytes(self):
        return self.response.content

    def text(self):
        return self.response.text


class AsyncHttpClient:
    """异步HTTP客户端

    通过httpx封装，实现了常见的HTTP方法,支持设置超时时间、请求参数等，简化了异步调用的层级缩进。

    Attributes:
        default_timeout: 默认请求超时时间,单位秒
        default_headers: 默认请求头字典
        default_resp_fmt: 默认响应格式json
        client: httpx 异步客户端
        response: 每次实例请求的响应
    """

    def __init__(self, timeout=timedelta(seconds=10), headers: dict = None, resp_fmt: RespFmt = RespFmt.JSON):
        """构造异步HTTP客户端"""
        self.default_timeout = timeout
        self.default_headers = headers or {}
        self.default_resp_fmt = resp_fmt
        self.client = httpx.AsyncClient()
        self.response: httpx.Response = None

    async def _request(self, method: str, url: str, params: dict = None, data: dict = None, timeout: timedelta = None,
                       **kwargs):
        """内部请求实现方法

        创建客户端会话,构造并发送HTTP请求,返回响应对象

        Args:
            method: HttpMethod 请求方法, 'GET', 'POST' 等
            url: 请求URL
            params: 请求查询字符串参数字典
            data: 请求体数据字典
            timeout: 超时时间,单位秒
            kwargs: 其他关键字参数

        Returns:
            httpx.Response: HTTP响应对象
        """
        timeout = timeout or self.default_timeout
        headers = self.default_headers or {}
        self.response = await self.client.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout.total_seconds(),
            **kwargs
        )
        return self.response

    def _parse_response(self, resp_fmt: RespFmt = None):
        """解析响应

        Args:
            resp_fmt: 响应格式

        Returns:
            resp Union[dict, bytes, str]
        """
        resp_fmt = resp_fmt or self.default_resp_fmt
        resp_content_mapping = {
            RespFmt.JSON: self.json,
            RespFmt.BYTES: self.bytes,
            RespFmt.TEXT: self.text,
        }
        resp_func = resp_content_mapping.get(resp_fmt)
        return resp_func()

    def json(self):
        return self.response.json()

    def bytes(self):
        return self.response.content

    def text(self):
        return self.response.text

    async def get(self, url: str, params: dict = None,timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """GET请求

        Args:
            url: 请求URL
            params: 请求查询字符串参数字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict or bytes
        """

        await self._request(HttpMethod.GET, url, params=params, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    async def post(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """POST请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict or bytes
        """
        await self._request(HttpMethod.POST, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    async def put(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """PUT请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict
        """
        await self._request(HttpMethod.PUT, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)

    async def delete(self, url: str, data: dict = None, timeout: timedelta = None, resp_fmt: RespFmt = None, **kwargs):
        """DELETE请求

        Args:
            url: 请求URL
            data: 请求体数据字典
            timeout: 请求超时时间,单位秒
            resp_fmt: 响应格式，默认None 使用实例对象的 default_resp_fmt

        Returns:
            resp => dict
        """
        await self._request(HttpMethod.DELETE, url, data=data, timeout=timeout, **kwargs)
        return self._parse_response(resp_fmt)


async def main():
    res = await AsyncHttpClient().get("http://www.baidu.com", resp_fmt=RespFmt.TEXT)
    print(res)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
