#!/usr/bin/env python
#-*-encoding:UTF-8-*-

import sys
import os
import logging
from Queue import *
import time
from random import randint
import hashlib

def DEBUG(msg):
    logging.getLogger().info(msg)

def WARN(msg):
    logging.getLogger().warn(msg)

def ERROR(msg):
    logging.getLogger().error(msg)

tpl_head = '''<!DOCTYPE html>
<html>
  <head>
    <title>^TPL_TITLE^</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->

  </head>'''

tpl_tail = '''<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="js/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>'''

tpl_body = '''<body>
      <table class="table" style="border-color:#FFF;">
        <thead></thead>
        <tbody>
           <!--^ITEM^-->
        </tbody>
    </table>'''

tpl_item = '''<tr>
                <td width="5%">^PROJECT_NAME^</td>
                <td>
                    <div class="progress progress-striped active">
                        <!--^process^-->
                    </div>
                </td>
            </tr>'''

tpl_process = '''<div id="%s" class="progress-bar progress-bar-%s" style="width: %s" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="%s" onmouseover="$('#%s').tooltip('show')" onmouseout="$('#%s').tooltip('hide')"><span class="">%s</span></div>'''

class plife:
    def __init__(self, filename):
        try:
            self.wp = open('index.html', 'wb+')
            self.filename = filename
            self.content = None
        except Exception, e:
            raise e

    def __del__(self):
        try:
            pass
        except Exception, e:
            raise e
    def read_cfg(self):
        try:
            fp = open(self.filename, 'rb')
            self.content = fp.read()
            fp.close()
        except Exception, e:
            raise e

    def generate(self):
        try:
            author = ''
            email = ''
            blog = ''

            tmp_body = tpl_body

            tmp_item = ''

            print 'read'
            self.read_cfg()
            items = self.content.split('PROJECT_NAME')
            for item in items:
                #cfg file head, contains some author info
                print item
                if '@Author' in item:
                    author = item.split('\n')[0].strip()[item.split('\n')[0].strip().find('=') + 1:]
                    email = item.split('\n')[1].strip()[item.split('\n')[1].strip().find('=') + 1:]
                    blog = item.split('\n')[2].strip()[item.split('\n')[2].strip().find('=') + 1:]
                    DEBUG(author+' '+email+' ' +blog)
                #project item
                else:
                    p_list = item.strip().split('\n')
                    print p_list
                    for i, p_item in enumerate(p_list):
                        if '=' in p_item:
                            tmp_item = tpl_item.replace('^PROJECT_NAME^', p_item.replace('=','').strip())
                            print tmp_item
                        elif p_item.strip() is None:
                            continue
                        else:
                            ids = self.md5(p_item)+str(randint(1,9))
                            tmp_item = tmp_item.replace('<!--^process^-->', tpl_process%(ids,self.get_color(i), p_item.split('#')[1].strip(), p_item.split('#')[0].strip(), ids, ids, p_item.split('#')[1].strip() + ' ' +p_item.split()[0].strip())+'<!--^process^-->')
                            print '===='
                    # print '=============addd============'
                    tmp_body = tmp_body.replace('<!--^ITEM^-->', tmp_item + '<!--^ITEM^-->')
                    tmp_item = ''
                    # print tmp_body
            self.wp.write(tpl_head.replace('^TPL_TITLE^', author+"'s projects")+tmp_body+tpl_tail)
            self.wp.close()
        except Exception, e:
            raise e

    def get_color(self, i):
        try:
            if i%4 == 0:
                return 'success'
            elif i%4 == 1:
                return 'info'
            elif i%4 == 2:
                return 'warning'
            elif i%4 == 3:
                return 'danger'

        except Exception, e:
            raise e

    def md5(self, src):
        try:
            md = hashlib.md5()
            md.update(src)
            return md.hexdigest()[0:7]
        except Exception, e:
            raise e
    
def initLog():
    logging.basicConfig(
            filename = 'build.log',
            filemode = 'a',
            format = '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            datefmt = '%a, %Y-%m-%d %H:%M:%S',
            level = logging.INFO,
            )

if __name__ == '__main__':
    initLog()
    try:
        if len(sys.argv) < 2:
            print('Please input the file name')
            WARN('Need file name')
            sys.exit(-1)
        else:
            p = plife(sys.argv[1])
            p.generate()
            # os.system('index.html')

    except Exception, e:
        raise e
        # ERROR('__main__:' + str(e))