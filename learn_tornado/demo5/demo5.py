import os.path as op

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import json

from tornado.options import define, options

define("port", default=18805, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/upload", UploadHandler)
        ]

        settings = dict(
            template_path=op.join(op.dirname(__file__), "templates"),
            static_path=op.join(op.dirname(__file__), "static"),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('upload.html')

    def post(self):
        ret = {'result': 'OK'}
        upload_path = op.join(op.dirname(__file__), 'files')  # 文件的暂存路径
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据

        if not file_metas:
            ret['result'] = 'Invalid Args'
            return ret

        for meta in file_metas:
            filename = meta['filename']
            file_path = op.join(upload_path, filename)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])

        self.write(json.dumps(ret))


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
