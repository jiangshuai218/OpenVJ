# coding=utf-8
import requests
from .exceptions import RequestFailed

class Robot(object):
    def __init__(self, cookies=None):
        self.cookies = cookies if cookies is not None else {}

    def login(self, username, password):
        raise NotImplementedError()

    @property
    def is_logged_in(self):
        raise NotImplementedError()

    def get_problem(self, url):
        raise NotImplementedError()

    def _request(self, method, url, **kwargs):
        kwargs["timeout"] = 10

        if kwargs["headers"] is None:
            kwargs["headers"] = {}

        cookies = kwargs.pop("cookies")
        if cookies is not None:
            kwargs["headers"]["Cookies"] = ""
            for k, v in cookies.items():
                kwargs["headers"]["Cookies"] += (k + "=" + v + "; ")

        common_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                          "Accept-Encoding": "gzip, deflate",
                          "Accept-Language": "en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4",
                          "Cache-Control": "no-cache",
                          "User-Agent": "VirtualJudge"}
        for k, v in common_headers.items():
            if k not in kwargs["headers"]:
                kwargs["headers"][k] = v
        retries = 3
        while True:
            try:
                return requests.request(method, url, **kwargs)
            except requests.RequestException as e:
                if retries == 0:
                    raise RequestFailed(e)
                retries -= 1

    def get(self, url, headers=None, cookies=None, allow_redirects=False):
        return self._request("get", url, headers=headers, allow_redirects=allow_redirects)

    def post(self, url, data, headers=None, cookies=None, allow_redirects=False):
        return self._request("post", url, data=data, cookies=cookies, headers=headers, allow_redirects=False)
