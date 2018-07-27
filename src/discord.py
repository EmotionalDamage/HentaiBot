from typing import Optional, Dict
from threading import Lock
from requests import post, Response
from json import dumps
from time import time, sleep
from math import ceil

BASE_URL = "https://discordapp.com/api"


class Discord:
    def __init__(self, token: str, base_url: str = BASE_URL) -> None:
        self.token: str = token
        self.reset_time: Optional[int] = None  # When the rate limit refreshes
        self.reset_remaining: Optional[int] = None  # Amount of requests remaining
        self.base_url: str = base_url
        self.lock = Lock()

    def rate_limit(self):
        if self.reset_time is None:
            return
        if (self.reset_remaining is not None) and (self.reset_remaining > 0):
            return
        elif time() > self.reset_time:
            return
        else:
            sleep(self.reset_time - ceil(time()))

    def send_msg(self, channel: str, content: str, embed: Optional[Dict] = None) -> Response:
        data = {
            "content": content,
        }
        if embed is not None:
            data["embed"] = embed
        with self.lock:
            self.rate_limit()
            assert self.lock.locked()
            response: Response = post(
                url=f"{self.base_url}/channels/{channel}/messages",
                data=dumps(data),
                headers={"Authorization": f"Bot {self.token}", "Content-Type": "application/json"}
            )
            self.reset_remaining = int(response.headers["X-RateLimit-Remaining"])
            self.reset_time = int(response.headers["X-RateLimit-Reset"])
        return response
