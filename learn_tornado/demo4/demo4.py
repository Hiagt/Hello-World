import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=18804, help="run on the given port", type=int)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')


class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'


class Application(tornado.web.Application):
    """
        模板中引用模块，必须在应用的设置中声明
        ui_modules参数期望一个模块名为键、类为值的字典输入来渲染

        此例中把名为Hello的模块的引用和我们定义的HelloModule类结合
    """

    def __init__(self):
        handlers = [
            (r'/', HelloHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={'Hello': HelloModule},
            debug=True
        )

        super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
