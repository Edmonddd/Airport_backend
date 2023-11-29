from django.http import JsonResponse

class UnifiedResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("接收到get_response请求，视图函数马上执行")

    def __call__(self, request):
        response = self.get_response(request)
        print("接收到request请求，视图函数马上执行")

        # 如果响应已经是一个JsonResponse，则不进行处理
        # if isinstance(response, JsonResponse):
        #     return response

        # 定义统一的响应格式
        unified_response = {
            'code': response.status_code,
            'message': response.reason_phrase,
            'data': response.content.decode('utf-8')
        }

        # 将原始响应替换为统一的JsonResponse
        new_response = JsonResponse(unified_response)

        # 将原始响应的状态码和其他头信息复制到新的JsonResponse中
        new_response.status_code = response.status_code
        for header, value in response.items():
            new_response[header] = value

        return new_response
