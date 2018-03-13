#!/usr/bin/env python
#--*-- coding:utf-8 --*--
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import re


class MainForm(object):
    def __init__(self):
        # this code is full of bug so do not use it!
        '''
        self.systemCode = "(.*)"
        self.systemName = "(.*)"
        self.ipaddress = "^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$"
        self.systemPort = '^[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]{1}|6553[0-5]$'
        self.systemPass = '(.*)'
        '''
        pass

    def check_valid(self, request):
        form_dict = self.__dict__
        res = []
        for key, regular in form_dict.items():
            post_value = request.get_argument(key)
            
            # 让提交的数据 和 定义的正则表达式进行匹配
            ret = re.match(regular, post_value)
            if ret != None:
                res.append(1)
            else:
                res.append(0)
        print res
        if 0 in res:
            return False
        else:
            return True
            


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        banner = '''
        <h1>Heimdall Anti-shell System</h1>
        '''
        #self.write(banner)
        self.render("index.html")

    def post(self, *args, **kwargs):
        obj = MainForm()
        flag = obj.check_valid(self)
        if flag == True:
            self.write('valid form')
        else:
            self.write("invalid form")


class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write_error(404)

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r"/", MainHandler),
            (r".*", PageNotFoundHandler),
        ]

        settings = dict(
            static_path= os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == "__main__":
    port = 8899
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port)

    print('Listen on http://localhost:{0}'.format(port))
    tornado.ioloop.IOLoop.instance().start()

    
    
    







