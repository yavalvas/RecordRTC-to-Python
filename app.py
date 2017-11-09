import os
import tornado.web
from tornado import gen

__UPLOADS__ = "uploads/"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class SaveFileHandler(tornado.web.RequestHandler):
    # @gen.coroutine
    def post(self):
        filename = self.get_body_argument("audio-filename", default=None, strip=False) \
                   or self.get_body_argument("video-filename", default=None, strip=False)
        files = self.request.files
        if "audio-blob" in files:
            for file in self.request.files["audio-blob"]:
                with open(os.path.join(__UPLOADS__, filename), 'wb') as out:
                    out.write(file.body)
        if "video-blob" in files:
            for file in self.request.files["video-blob"]:
                with open(os.path.join(__UPLOADS__, filename), 'wb') as out:
                    out.write(file.body)
        # process file in callback
        self.write({"status": "success"})


class DeleteFilesHandler(tornado.web.RequestHandler):
    def post(self):
        file_to_delete = self.get_argument('delete-file', default=None)
        if file_to_delete:
            os.remove(os.path.join(__UPLOADS__, file_to_delete))


root = os.path.dirname(__file__)
port = 8000

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/static", tornado.web.StaticFileHandler, {"path": os.path.join(root, "static")}),
    (r"/uploads", tornado.web.StaticFileHandler, {"path": os.path.join(root, "uploads")}),
    (r"/save", SaveFileHandler),
    (r"/delete", DeleteFilesHandler)
])

if __name__ == '__main__':
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
