#!/usr/bin/env python
from math import *
import subprocess as subp
from gi.repository import Gtk,Gdk
from tempfile import NamedTemporaryFile
from os import remove
from sympy import sympify,diff
from sys import stderr
from signal import signal,SIG_IGN,SIGCHLD
from sympy.utilities.autowrap import autowrap
from time import time

class UserFunc:
    allow_func={"sin":sin,
                "cos":cos,
                "exp":exp}
    def __init__(self,expr="",compile_to=''):
        self.expr=expr
        if compile_to:
            
            var=sympify('x'),sympify('y')
            
            self.compiled=autowrap(sympify(expr),language=compile_to,args=var)
            print(expr,'compiled!')
        else:
            self.compiled=None
            pass
    
    def __call__(self,x,y):

        if self.compiled:
            return self.compiled(x,y)
        elif self.expr:
            self.allow_func["x"]=x
            self.allow_func["y"]=y
            try:
                z=eval(self.expr,{"__builtins__":None},self.allow_func)
            except:
                raise TypeError
            else:
                try:
                    z=float(z)
                except:
                    raise TypeError
            return z
    def __str__(self):
        return str(self.expr)
    def __repr__(self):
        return str(self.expr)
def gradient(max_iter,eps,xs,f,df_dx,d2f_dx):
    '''
    Функция gradient проводит минимизацию функции f,
    используя начальное приближение xs, первые производные df_dx,
    вторые производные d2f_dx, при максимальном кол-ве итераций max_iter
    и точностью eps.
    Возвращает список, содержащий приближения к минимуму функции.
    Параметры:
    max_iter - int - максимальное кол-во итераций,
    eps - float - максимальная разница между соседними приближениями,
    xs - (double) - кортеж начальных приближений,
    f - function - минимизируемая функция,
    df_dx - [function] - список первых производных функции,
    d2f_dx - [[function]] - матрица вторых производных (матрица Гессе)
    '''
    res=[xs]
    
    end=False
    t=time()
    while max_iter>0 and not end:
        end=True
        xns=[]
        for i in range(0,len(xs)):
            v=df_dx[i](*xs)
            l0=0;l=0;
            for j in range(0,len(xs)):
                for k in range(0,len(xs)):
                    #print('a',end='')
                    a=d2f_dx[j][k](*xs)
                    #print(a)
                    a*=df_dx[j](*xs)
                    a*=df_dx[k](*xs)
                    l0+=a
                l+=df_dx[j](*xs)**2
            if l0 and l:
                l=l/l0;
                xns.append(xs[i]-l*v)
                if abs(xns[-1]-xs[i])>eps:
                    end=False
            else:
                xns.append(xs[i])
                print("Extremum!")
        xs=xns
        max_iter-=1
        res.append(xs)
    print(time()-t)
    return res
    

class Application(Gtk.Builder):
    def __init__(self,ui_filename):
        #signal(SIGCHLD,SIG_IGN)
        Gtk.Builder.__init__(self)
        self.add_from_file(ui_filename)
        self.connect_signals(self)
        self.plot=None
        self.tempfile=NamedTemporaryFile(delete=False)
        self.tempfile.close()
    def show_msg(self,msg):
        md=Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, 
                      Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, msg);
        md.run ();
        md.destroy();
    def show(self,form_name):
        window = self.get_object(form_name)
        window.show()
        Gtk.main()
    def on_window_destroy( self,widget, data=None):
        self.get_object('window1').hide()
        if self.plot and self.plot.poll()==None:
            self.plot.stdin.close()
            self.plot.terminate()
            if self.plot.poll()==None:
                self.plot.kill()
                self.plot.wait()
        if self.tempfile:
            if not self.tempfile.closed:
                self.tempfile.close()
            remove(self.tempfile.name)
        Gtk.main_quit()
    def on_func_clicked(self,button,data=None):
        expr=self.get_object("entry1").get_text();
        if self.get_object("combobox1").get_property("active")==1:
            lang='F95'
        elif self.get_object("combobox1").get_property("active")==2:
            lang='C'
        else:
            lang=''
        self.f=UserFunc(expr,lang)
        var=sympify('x'),sympify('y')
        self.df_dx=[]
        for i in var:    
            self.df_dx.append(UserFunc(str(diff(sympify(self.f.expr),i)),lang))
        self.d2f_dx=[]
        for i in range(0,len(var)):
            t=[]
            for j in range(0,i):
                t.append(self.d2f_dx[j][i])
            for j in range(i,len(var)):
                t.append(UserFunc(str(diff(sympify(self.df_dx[i].expr),var[j])),lang))
            self.d2f_dx.append(t)
        print(self.df_dx); print(self.d2f_dx);
    def show_chart(self):
        table=self.get_object("treeview1")
        model=table.get_model()
        self.tempfile=open(self.tempfile.name,'wb')
        for r in model:
            self.tempfile.write("{0} {1} {2}\n".format(r[0],r[1],
                                        self.f(r[0],r[1])).encode())
        self.tempfile.close()
        if self.plot and self.plot.poll()==None:
            self.plot.stdin.close()
            self.plot.terminate()
            if self.plot.poll()==None:
                self.plot.kill()
                self.plot.wait()
        msg=('set pm3d;splot '+self.f.expr+',"'+self.tempfile.name+
            '" title "Рассчитано" with linespoints;pause -1')
        self.plot=subp.Popen(['gnuplot','-e',msg],bufsize=4000,shell=False,
                    stdin=subp.PIPE);

    def chart_clicked(self,widget,data=None):
        self.show_chart()
    def input_data(self):
        x=float(self.get_object("entry2").get_text());
        y=float(self.get_object("entry3").get_text())
        maxiter=int(self.get_object("entry6").get_text())
        eps=float(self.get_object("entry7").get_text())
        return x,y,maxiter,eps,self.f,self.df_dx,self.d2f_dx
    def output_data(self,res):
        table=self.get_object("treeview1")
        model=table.get_model()
        model.clear()
        for r in res:       
            model.append([r[0],r[1],self.f(r[0],r[1])])
        
    def on_run_clicked(self,button,data=None):
        x,y,maxiter,eps,f,df_dx,d2f_dx=self.input_data()
        res=gradient(maxiter,eps,(x,y),f,df_dx,d2f_dx)
        self.output_data(res)
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
        
        
app=Application("prac4.ui")
app.show("window1")
