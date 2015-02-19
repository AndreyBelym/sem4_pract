#!/usr/bin/env python
from gi.repository import Gtk
from math import exp
from alg3 import solve_eq
import subprocess as subp
from tempfile import NamedTemporaryFile
from os import remove
from sys import stderr
def c(a,b):
    return (a-b)/(exp(b)*(b-1)-exp(a)*(a-1)-2)
def y_solved(x,a,b):
    return exp(-x)+x*c(a,b)
def k(x,s):
    return 1/2*x*exp(s);
def f(x):
    return exp(-x);
class Application(Gtk.Builder):
    def __init__(self,ui_filename):
        Gtk.Builder.__init__(self)
        self.add_from_file(ui_filename)
        self.connect_signals(self)
        self.plot=None
        self.tempfile=NamedTemporaryFile(delete=False)
        self.tempfile.close()
        #print(help(NamedTemporaryFile))
    def show(self,form_name):
        window = self.get_object(form_name)
        window.show()
        Gtk.main()
    def on_window_destroy( self,widget, data=None):
        
        if self.plot and self.plot.poll()==None:
            self.plot.terminate()
            if self.plot.poll()==None:
                self.plot.kill()
                self.plot.wait()
        if self.tempfile:
            if not self.tempfile.closed:
                self.tempfile.close()
            remove(self.tempfile.name)
        def on_window_destroy( self,widget, data=None):
        #self.get_object('window2').destroy()
        widget.hide()
        widget.destroy()
        Gtk.main_quit()
    def show_chart(self):
        a=float(self.get_object("entry1").get_text())
        b=float(self.get_object("entry2").get_text())
        h=float(self.get_object("entry3").get_text())
        table=self.get_object("treeview1").get_model()
        expr='exp(-x)+{0}*x'.format(c(a,b))
        print(expr)
        if self.plot and self.plot.poll()==None:
            self.plot.terminate()
            if self.plot.poll()==None:
                self.plot.kill()
                self.plot.wait()
        self.tempfile=open(self.tempfile.name,'wb')
        for i in table:
            self.tempfile.write("{0} {1}\n".format(i[0],i[1]).encode())
        self.tempfile.close()
        msg='plot '+expr+',"'+self.tempfile.name+'";pause -1'
        self.plot=subp.Popen(['gnuplot','-e',msg],shell=False,stdin=subp.PIPE)
    def chart_clicked(self,button,data=None):
        self.show_chart()
    def input_data(self):
        a=float(self.get_object("entry1").get_text())
        b=float(self.get_object("entry2").get_text())
        h=float(self.get_object("entry3").get_text())
        return a,b,h
    def output_data(self,a,b,x,y):
        table=self.get_object("treeview1")
        model=table.get_model()
        table.set_model(None)
        model.clear()
        for i in range(0,len(x)):
            model.append([x[i],y[i],y_solved(x[i],a,b)])
        table.set_model(model)
        
    def on_run_click(self,button,data=None):
        a,b,h=self.input_data()
        x,y=solve_eq(a,b,h,k,f)
        self.output_data(a,b,x,y)
        self.show_chart()

    def on_help_show(self,widget,*args):
        self.show('window2');
    def on_help_destroy(self,widget,*args):
        widget.hide()
        widget.destroy()
    def on_help_close(self,widget,*args):
        self.get_object('window2').destroy()
    def on_close(self,widget,*args):
        self.get_object('window1').destroy()
        
app=Application("prac3.ui")
app.show("window1")


