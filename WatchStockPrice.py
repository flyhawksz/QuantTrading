# -*- coding:utf-8 -*-
#查看股票实时价格

__author__ = 'zyy'
from Tkinter import *
import sys, urllib2, time

count = 0
root = Tk()
title = Label(root,text=u'股票代码')
title.pack()
l_stock_no = Entry(root)
l_stock_no.pack()
content = Label(root,text=u'实时行情')
content.pack()


class StockMonitor(Frame):
    msec = 1000

    def __init__(self,parent=None,**kw):
        Frame.__init__(self,parent,kw)
        self._running = False
        self.c_date = StringVar()
        self.c_time = StringVar()
        self.stockinfo  = StringVar()
        self.flag = True
        self.makeWidget()

    def makeWidget(self):
        label_date = Label(self,textvariable=self.c_date)
        label_date.pack()
        label_time = Label(self,textvariable=self.c_time)
        label_time.pack()
        label_stock = Label(self,textvariable=self.stockinfo)
        label_stock.pack()

        btn_start = Button(self,text='start',command=self.start)
        btn_start.pack(side=LEFT)
        btn_end = Button(self,text='end',command=self.quit)
        btn_end.pack(side=LEFT)

    def get_stock_info(self,stock_no,num_retries=2):
        try:
            url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd='+stock_no.strip()+'2&sty=CTBF&st=z&sr=&p=&ps=&cb=var%20pie_data=&js=(x)&token=28758b27a75f62dc3065b81f7facb365&_=1496312544427'
            headers = {'User-agent':'WSWP'}
            request = urllib2.Request(url,headers=headers)
            page = urllib2.urlopen(request)
            page_content = page.read()
        except urllib2.URLError as e:
            print  'download error:',e.reason
            page_content = None
            if num_retries > 0:
                if hasattr(e,'code' and 500 <= e.code <600):
                    # recursively retry 5xx HTTP errors
                    return get_stock_info(stock_no,num_retries-1)
        return page_content

    def _update(self):
        self._set_count()
        self.timer = self.after(self.msec,self._update)

    def _set_count(self):

        stock_info = self.get_stock_info(l_stock_no.get())
        if stock_info is not None:
            stock_info = stock_info[14:64]
        today1 = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        time1 = str(time.strftime('%H:%M:%S', time.localtime(time.time())))
        self.stockinfo.set(stock_info)
        self.c_date.set(today1)
        self.c_time.set(time1)

    def start(self):
        self._update()
        self.pack(side = TOP)


def main():

    stock = StockMonitor(root)
    stock.pack(side = BOTTOM)
    root.mainloop()
    root.geometry('350x250')

if __name__ == '__main__':
    main()