import json
from rest_framework.renderers import BaseRenderer


class CustomJSONRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'json'

    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = data.pop('message', 'success')
                code = data.pop('code', 1)
                code = renderer_context['response'].status_code
            else:
                msg = 'success'
                code = renderer_context['response'].status_code
                state = 1

            # 重新构建返回的JSON字典
            # for key in data:
            #     # 判断是否有自定义的异常的字段
            #     if key == 'message':
            #         msg = data[key]
            #         data = ''
            #         code = 0

            ret = {
                'code': code,
                'message': msg,
                'data': data,
            }
            # 返回JSON数据
            ret = json.dumps(ret, indent=4)
            return ret
        else:
            return data
