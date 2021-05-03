# -*- coding: utf-8 -*-

import json
import urllib.request


def speech_to_text(filename=None, bytes=None, topic='general', lang='ru-RU', key=None):
    if filename is not None:
        with open(filename, "rb") as f:
            data = f.read()
    elif bytes is not None:
        data = bytes
    else:
        raise Exception("Neither filename nor byte representation are passed to the STT method.")

    params = "&".join([f"topic={topic}", f"lang={lang}"])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
    url.add_header("Authorization", "Api-Key %s" % key)
    url.add_header("Transfer-Encoding", "chunked")

    response_data = urllib.request.urlopen(url).read().decode('UTF-8')
    decoded_data = json.loads(response_data)

    if decoded_data.get("error_code") is None:
        return decoded_data.get("result")
    else:
        raise Exception(json.dumps(decoded_data))
