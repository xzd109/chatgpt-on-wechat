# encoding:utf-8

import os
import signal
import sys
import time

from channel import channel_factory
from common import const
from config import load_config
from plugins import *
import threading


def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def start_channel(channel_name: str):
    channel = channel_factory.create_channel(channel_name)
    if channel_name in ["wx", "wxy", "terminal", "wechatmp", "wechatmp_service", "wechatcom_app", "wework",
                        const.FEISHU, const.DINGTALK]:
        PluginManager().load_plugins()

    if conf().get("use_linkai"):
        try:
            from common import linkai_client
            threading.Thread(target=linkai_client.start, args=(channel,)).start()
        except Exception as e:
            pass
    channel.startup()


def run():
    #print(os.path.dirname(os.path.abspath(__file__)))
    #exit()

    try:
        # load config
        load_config()
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)

        # create channel
        channel_name = conf().get("channel_type", "wx")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        if channel_name == "wxy":
            os.environ["WECHATY_LOG"] = "warn"

        start_channel(channel_name)

        while True:
            time.sleep(1)
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)
def _fetch_app_info(app_code: str="HYhYAOBb"):
    import requests
    load_config()
    headers = {"Authorization": "Bearer " + conf().get("linkai_api_key")}
    # do http request
    base_url = conf().get("linkai_api_base", "https://api.link-ai.chat")
    params = {"app_code": app_code}
    res = requests.get(url=base_url + "/v1/app/info", params=params, headers=headers, timeout=(5, 10))
    if res.status_code == 200:
        print(res.json())
    else:
        logger.info(f"[LinkAI] find app info exception, res={res}")

if __name__ == "__main__":
    #_fetch_app_info()
    run()
