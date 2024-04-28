from http import HTTPStatus
from dashscope import Application
import dashscope
#dashscope.api_key="YOUR_DASHSCOPE_API_KEY"
#dashscope.api_key="YOUR_DASHSCOPE_API_KEY"
def rag_call():
    #dashscope.api_key="sk-c91bc01a8e0246369ccfb479dd456557"
    #sk - c91bc01a8e0246369ccfb479dd456557
    response = Application.call(app_id='asst_d06be5c7-b690-4b42-af50-54d36ea31d62',
                                api_key='sk-c91bc01a8e0246369ccfb479dd456557',
                                prompt='你好?'
                                )

    if response.status_code != HTTPStatus.OK:
        print('request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
    else:
        print('request_id=%s\n output=%s\n usage=%s\n' % (response.request_id, response.output, response.usage))


if __name__ == '__main__':
    rag_call()