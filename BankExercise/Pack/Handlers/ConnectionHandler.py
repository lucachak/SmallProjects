import http.client
import json

'''
class yet to be finished. intention:
    create a class that handles a connection for the user
    and posting its data, to an api. 
'''

class Connector:
    def __init__(self, url:str, username:str, password:str, id:int|str)->None:
        self.__url = url
        self.__username = username
        self.__password = password
        self.__id = id
        self.__connect()


    def clear_url(self, url:str)->list[str|int]:
        values = url.split('/')
        method = str(values[0])
        base = values[2].split(":")[0] + '/'
        port = values[2].split(":")[1]
        path = '/'.join(values[3:])
        return [method,base.strip('/'), port, path]

    def __check_status(self, response:http.client.HTTPResponse)->bool:
        if response.status == 200:
            return True
        else:
            return False

    def __check_host(self) -> bool:

        info = self.clear_url(self.__url)

        try:

            if info[0] == 'http:':
                conn = http.client.HTTPConnection(str(info[1]), int(info[2]))
                conn.request("GET", '/'+str(info[3]))
            elif info[0] == 'https:':
                conn = http.client.HTTPSConnection(str(info[1]), int(info[2]))
                conn.request("GET", '/'+str(info[3]))
            else:
                raise ValueError("Unsupported protocol")
            response = conn.getresponse()

            if self.__check_status(response):
                conn.close()
                return True
            else:
                conn.close()
                return False

        except Exception as e:
            print(e)
            return False

    def __connect(self)->None|bool:

        if not self.__check_host():
            return False
        url = self.clear_url(self.__url)
        protocol, host, port, path = url

        # Implement connection logic here
        def __disconnect(conn: http.client.HTTPSConnection |http.client.HTTPConnection):
            conn.close()

        try:
            if protocol == 'http:':
                conn = http.client.HTTPConnection(str(host), int(port))
            elif protocol == 'https:':
                conn = http.client.HTTPSConnection(str(host), int(port))
            else:
                raise ValueError("Unsupported protocol")

            # Send a single request
            conn.request("GET", f"/{path}")
            response = conn.getresponse()

            # Read and print the response (optional)
            data = json.loads(response.read().decode('utf-8'))
            print(data)
            # Close the connection
            __disconnect(conn)
            print("Disconnected successfully")

        except Exception as e:
            print(f"Connection error: {e}")
            raise ConnectionError(f"Connection failed: {e}")


    def __str__(self) -> str:
        return f"Connector(url={self.__url}, username={self.__username}, password={self.__password}, id={self.__id})"
