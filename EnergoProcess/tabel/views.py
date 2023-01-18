from django.http import HttpResponse


def index(request):
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные бразера
    path = request.path  # получаем запрошенный путь

    return HttpResponse(f"""
            <p>Host: {host}</p>
            <p>Path: {path}</p>
            <p>User-agent: {user_agent}</p>
        """)

def about(request):
    return HttpResponse("Инструкция по заполнению табеля")