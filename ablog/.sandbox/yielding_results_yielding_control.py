# class ContextManager():
#     def __init__(self, f):
#         self.f = f()

#     def __call__(self):
#         return self

#     def __enter__(self):
#         self.f.__next__()

#     def __exit__(self, *args, **kwargs):
#         try:
#             self.f.__next__()
#         except StopIteration:
#             pass

@ContextManager
def context_manager():
    print('enter')
    yield None
    print('exit')

# if __name__ == "__main__":
#     with context_manager() as c:
#         print(c)
#         print('within context_manager')

################################################################################

# import requests
# import json

# class HTTPStatus:
#     def __init__(self, url):
#         self.url = url
#         self.session = requests.Session()
#         self.resp = None

#     def get_resp(self):
#         self.resp = self.session.get(self.url)

#     def post_resp(self):
#         self.resp = self.session.post(self.url)

#     @property
#     def text(self):
#         return self.resp.text

# conn = HTTPStatus('https://api.mocki.io/v1/b043df5a')
# conn.get_resp()
# assert conn.resp.status_code == 200
# print(json.loads(conn.text))

################################################################################

# import requests
# import json

# class HTTPStatus:
#     def __init__(self, url):
#         self.url = url
#         self.session = requests.Session()
#         self.resp = None
#         self.generator = self.generator()

#     def get_resp(self):
#         self.resp = self.session.get(self.url)

#     def post_resp(self):
#         self.resp = self.session.post(self.url)

#     @property
#     def text(self):
#         return self.resp.text

#     def generator(self):
#         self.get_resp()
#         yield self
#         yield self.text

# conn = HTTPStatus('https://api.mocki.io/v1/b043df5a')
# conn = next(conn.generator)
# assert conn.resp.status_code == 200
# conn = next(conn.generator)
# print(json.loads(conn))

################################################################################

import requests
import json

class MockGet:
    def __init__(self, url, data=None):
        self.url = url
        self.text = data
        self.status_code = 200

class MockPost:
    def __init__(self, url, data):
        self.url = url
        self.status_code = 202
        self.text = json.dumps({data: self.return_resp(data)})

    def return_resp(self, data):
        if data == "this":
            return "that"
        elif data == "fizz":
            return "buzz"
        else:
            return "goobar"

class MockSession:
    def get(self, url, data):
        return MockGet(url, data)

    def post(self, url, data):
        return MockPost(url, data)
    
class HTTPResponse:
    def __init__(self, url):
        self.url = url
        self.session = MockSession()
        self.generator = self.generator()

    def __next__(self):
        self.generator.__next__()

    def generator(self):
        self.GET()
        yield
        self.POST()
        yield

    def GET(self):
        self.resp = self.session.get(self.url, self.url.split("://")[1])

    def POST(self):
        self.resp = self.session.post(self.url, self.resp.text)

conn = HTTPResponse("mock://this")
assert conn.url.startswith("mock://")
next(conn)
assert conn.url.startswith("mock://")
assert conn.resp.status_code == 200
print(conn.resp.text)
next(conn)
assert conn.url.startswith("mock://")
assert conn.resp.status_code == 202
print(json.loads(conn.resp.text))

################################################################################

# import requests
# import json

# class MockGet:
#     def __init__(self, url, data=None):
#         self.url = url
#         self.text = data
#         self.status_code = 200

# class MockPost:
#     def __init__(self, url, data):
#         self.url = url
#         self.status_code = 202
#         self.text = json.dumps({data: self.return_resp(data)})

#     def return_resp(self, data):
#         if data == "this":
#             return "that"
#         elif data == "fizz":
#             return "buzz"
#         else:
#             return "goobar"

# class MockSession:
#     def get(self, url, data):
#         return MockGet(url, data)

#     def post(self, url, data):
#         return MockPost(url, data)
    
# class HTTPResponse:
#     def __init__(self, url):
#         self.url = url
#         self.session = MockSession()

#     def GET(self):
#         self.resp = self.session.get(self.url, self.url.split("://")[1])

#     def POST(self):
#         self.resp = self.session.post(self.url, self.text)


# conn = HTTPResponse("mock://fizz")
# conn.GET()
# assert conn.resp.url.startswith("mock://")
# assert conn.status_code == 200
# print(conn.text)
# conn.POST()
# assert conn.resp.url.startswith("mock://")
# assert conn.status_code == 202
# print(json.loads(conn.text))
