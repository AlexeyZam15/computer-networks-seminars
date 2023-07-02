import os
import socket
from threading import Thread


class Client:

    # инициализация объекта
    def __init__(self, server: (str, int), nickname: str):
        try:
            self.__nickname = nickname
            # Connecting To Server
            self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client.connect(server)
            self.__receive_thread = Thread(target=self.__receive)
            self.__write_thread = Thread(target=self.__write)
        # обработка ошибки подключения к серверу
        except ConnectionRefusedError:
            print('Сервер выключен')
            exit()

    # Starting Threads For Listening And Writing
    def start(self):
        self.__receive_thread.start()
        self.__write_thread.start()

    # Listening to Server and Sending Nickname
    def __receive(self):
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.__client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.__client.send(self.__nickname.encode('utf-8'))
                else:
                    print(message)
            except ConnectionResetError:
                # Выход из программы при отсутствии подключения к серверу
                print("Сервер выключен")
                self.exit()

    # Ввод сообщений и отправка их на сервер
    def __write(self):
        while True:
            try:
                string = input()
                if string != '':
                    message = '{}: {}'.format(self.__nickname, string)
                    self.__client.send(message.encode('utf-8'))
            # Обработка ошибок и выход из программы
            except:
                self.exit()

    def exit(self):
        self.__client.close()
        print('Выход из программы')
        os._exit(0)


def exit():
    print('Выход из программы')
    os._exit(0)


def main():
    nickname = ''
    try:
        nickname = input("Choose your nickname: ")
    # Обработка ошибок и выход из программы
    except:
        exit()
    # Создание объекта с передачей IP и порта сервера и имени пользователя
    client = Client(('127.0.0.1', 55555), nickname)
    client.start()


if __name__ == "__main__":
    main()
