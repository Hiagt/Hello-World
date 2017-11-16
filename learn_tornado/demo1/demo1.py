import os
import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=18801, help="run on the given port", type=int)

"""
    tornado.options 来从命令行中读取设置。我们在这里使用这个模块指定我们的应用监听HTTP请求的端口
    
    工作流程:    如果一个与define语句中同名的设置在命令行中被给出，
    那么它将成为全局options的一个属性。如果用户运行程序时使用了--help选项，
    程序将打印出所有你定义的选项以及你在define函数的help参数中指定的文本。
    如果用户没有为这个选项指定值，则使用default的值进行代替。
    Tornado使用type参数进行基本的参数类型验证，当不合适的类型被给出时抛出一个异常。
    
"""


class Application(tornado.web.Application):
    """
    Tornado应用中最多的工作是定义类继承Tornado的RequestHandler类。
    创建App类为一种写法，另一种写法为直接在main中创建

    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    创建了一个简单的应用，在给定的端口监听请求，并在根目录（"/"）响应请求。
    """

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/reverse/(\w+)", ReverseHandler),
            (r"/wrap", WrapHandler),
            (r"/form/index", FormIndexHandler),
            (r"/form/test", FormPageHandler),
        ]

        '''
            通过向Application类的构造函数传递参数来告诉
            Tornado从文件系统的一个特定位置提供静态文件
        '''
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,  # 跨站请求伪造cookie,默认为True
        )
        super(Application, self).__init__(handlers, **settings)

    pass


class ReverseHandler(tornado.web.RequestHandler):
    """
        Tornado的请求处理函数类。当处理一个请求时，Tornado将这个类实例化，并调用与HTTP请求方法所对应的方法。
        这里定义了一个get方法，也就是说这个处理函数将对HTTP的GET请求作出响应。
    """

    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 5)
        self.write(textwrap.fill(text, int(width)))

    def write_error(self, status_code, **kwargs):
        self.write("Test Error!! {0} error.".format(status_code))


class IndexHandler(tornado.web.RequestHandler):
    """
        Tornado的RequestHandler类有一系列有用的内建方法,包括get_argument，
        在这里从一个查询字符串中取得参数greeting的值。
        （如果这个参数没有出现在查询字符串中，Tornado将使用get_argument的第二个参数作为默认值。）

        如果使用自己的方法代替默认的错误响应，可以重写 write_error 方法在RequestHandler类中
    """

    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

    def write_error(self, status_code, **kwargs):
        self.write("Test Error!! {0} error. ".format(status_code))


'''Form模板渲染'''


class FormIndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('upload.html')


class FormPageHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name')
        food1 = self.get_argument('food1')
        food2 = self.get_argument('food2')
        food3 = self.get_argument('food3')
        self.render('poem.html', user=name, food1=food1, food2=food2, food3=food3)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    # app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    app = Application()
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
