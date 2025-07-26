import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

hostName = "localhost" # Адрес для доступа по сети
serverPort = 8080 # Порт для доступа по сети
file_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'contacts.html')

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200) # Отправка кода ответа
        self.send_header("Content-type", "text/html") # Отправка типа данных, который будет передаваться
        self.end_headers() # Завершение формирования заголовков ответа
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        self.wfile.write(bytes(data, "utf-8"))

    def do_POST(self):
        """Метод для обработки POST-запросов"""
        content_length = int(self.headers['Content-Length']) # Получаем длину тела запроса
        post_data = self.rfile.read(content_length) # Считываем тело запроса
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))         # Декодируем и разбираем в словарь

        # Печатаем данные в консоль
        print("Принятые данные POST-запроса:")
        for key, value in data.items():
            print(f"{key}: {value}")

        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"")

if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")