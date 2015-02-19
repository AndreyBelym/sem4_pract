#!/usr/bin/env python
from copy import copy
import cairo
from gi.repository import Gtk,Gdk
from alg1 import Point, kohen_sutherland

def view_binary(decimal):
    bin_str=""
    while decimal:
        if decimal&1:
            bin_str='1'+bin_str
        else:
            bin_str='0'+bin_str
        decimal>>=1
    while len(bin_str)!=4:
        bin_str='0'+bin_str
    return bin_str

class Application(Gtk.Builder):
    
    def __init__(self,ui_filename):
        self.clipped=False
        Gtk.Builder.__init__(self)
        self.add_from_file(ui_filename)
        self.connect_signals(self)
        self.margin=5
        
    def show_msg(self,msg):
        md=Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
                             Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, msg);
        md.run ();
        md.destroy();
    def show(self,form_name):
        window = self.get_object(form_name)
        window.show_all()
        Gtk.main()
    def on_window_destroy( self,widget, data=None):
        #self.get_object('window2').destroy()
        widget.hide()
        widget.destroy()
        Gtk.main_quit()
    def get_value(self,name):
        return int(float(self.get_object(name).get_text()))
    def input_data(self):
        try:
            p1=Point(self.get_value("entry1"),
                    self.get_value("entry2"))
            p2=Point(self.get_value("entry3"),
                    self.get_value("entry4"))
            ll_edge=Point(self.get_value("entry5"),
                    self.get_value("entry6"))
            tr_edge=Point(self.get_value("entry7"),
                    self.get_value("entry8"))
        except Exception as e:
            self.show_msg("Неправильное значение в поле ввода!\n"+str(e))
            return
        ll_edge.x,ll_edge.y,tr_edge.x,tr_edge.y=(
            min(ll_edge.x,tr_edge.x),
            min(ll_edge.y,tr_edge.y),
            max(ll_edge.x,tr_edge.x),
            max(ll_edge.y,tr_edge.y))
        if (ll_edge.x==tr_edge.x  or ll_edge.y==tr_edge.y):            
            self.show_msg("Координаты X или Y углов прямоугольника равны!")
            raise
        return p1,p2,ll_edge,tr_edge
    def output_data(self,p1,p2,ll_edge,tr_edge):
        p1x_info=self.get_object("label20");p1y_info=self.get_object("label24");
        p2x_info=self.get_object("label26");p2y_info=self.get_object("label28");
        res_info=self.get_object("label21");
        if not res:
            res_info.set_text("Отрезок расположен в прямоугольнике")
            p1x_info.set_text(str(int(p1.x)))
            p1y_info.set_text(str(int(p1.y)))
            p2x_info.set_text(str(int(p2.x)))
            p2y_info.set_text(str(int(p2.y)))
        elif res==2:
            res_info.set_text("Отрезок не расположен в прямоугольнике")
            p1x_info.set_text("Не существует")
            p1y_info.set_text("Не существует")
            p2x_info.set_text("Не существует")
            p2y_info.set_text("Не существует")
        elif res==1:
            res_info.set_text("Отрезок частично расположен в прямоугольнике")
            p1x_info.set_text(str(int(p1.x)))
            p1y_info.set_text(str(int(p1.y)))
            p2x_info.set_text(str(int(p2.x)))
            p2y_info.set_text(str(int(p2.y)))
        else:
            res_info.set_text("Извините, маленькие технические неполадки")
        self.clipped=True
        self.get_object('drawingarea1').queue_draw()
    def on_run_clicked(self,button,data=None):
        p1,p2,ll_edge,tr_edge=self.input_data()
        res=kohen_sutherland(p1,p2,ll_edge,tr_edge)
        self.output_data(p1,p2,ll_edge,tr_edge)
    def on_mouse_press(self,widget,event,data=None):
        '''if self.clipped:
            cr=widget.get_window().cairo_create()
            cr.set_source_rgb(1.0,1.0,1.0)
            cr.paint()
            self.clipped=False'''
        if event.button==1:
            self.get_object("entry1").set_text(str(int(event.x)-self.margin))
            self.get_object("entry2").set_text(str(int(event.y)-self.margin))
            
        elif event.button==3:
            self.get_object("entry5").set_text(str(int(event.x)-self.margin))
            self.get_object("entry6").set_text(str(int(event.y)-self.margin))
            
    def on_mouse_release(*args):
        pass
    def update_draw(self,widget,data=None):
        drawarea=self.get_object("drawingarea1")
        cr=drawarea.get_window().cairo_create()
        if self.clipped:
            self.on_run_clicked(None)
        else:
            self.draw_clipped(cr,drawarea)

        self.draw_clipped(cr,widget)
    def coord_changed(self,widget,data=None):
        drawarea=self.get_object("drawingarea1")
        cr=drawarea.get_window().cairo_create()
        if self.clipped:
            self.on_run_clicked(None)
        else:
            self.draw_clipped(cr,drawarea)
    def on_help_show(self,widget,*args):
        self.show('window2');
    def on_help_destroy(self,widget,*args):
        widget.hide()
        widget.destroy()
    def on_help_close(self,widget,*args):
        self.get_object('window2').destroy()
    def on_close(self,widget,*args):
        self.get_object('window1').destroy()
    def on_move(self,widget,event,pointer=None):
        cr=widget.get_window().cairo_create()
        draw_serie=False;draw_rect=False;
        if event.state&(event.state.BUTTON1_MASK|event.state.BUTTON3_MASK):
            if event.state&event.state.BUTTON1_MASK:
                p1=Point(int(float(self.get_object("entry1").get_text())),
                        int(float(self.get_object("entry2").get_text())))
                p2=Point(int(event.x)-self.margin,int(event.y)-self.margin)
                self.get_object("entry3").set_text(str(int(event.x)-self.margin))
                self.get_object("entry4").set_text(str(int(event.y)-self.margin))
                draw_serie=True
                try:
                    ll_edge=Point(int(float(self.get_object("entry5").get_text())),
                            int(float(self.get_object("entry6").get_text())))
                    tr_edge=Point(int(float(self.get_object("entry7").get_text())),
                            int(float(self.get_object("entry8").get_text())))
                except:
                    pass
                else:
                    draw_rect=True
            elif event.state&event.state.BUTTON3_MASK:
                ll_edge=Point(int(float(self.get_object("entry5").get_text())),
                        int(float(self.get_object("entry6").get_text())))
                tr_edge=Point(int(event.x)-self.margin,int(event.y)-self.margin)
                self.get_object("entry7").set_text(str(int(event.x)-self.margin))
                self.get_object("entry8").set_text(str(int(event.y)-self.margin))
                draw_rect=True
                try:
                    p1=Point(int(float(self.get_object("entry1").get_text())),
                            int(float(self.get_object("entry2").get_text())))
                    p2=Point(int(float(self.get_object("entry3").get_text())),
                            int(float(self.get_object("entry4").get_text())))
                except:
                    pass
                else:
                    draw_serie=True
            
            cr.push_group()
            cr.set_source_rgb(1.0,1.0,1.0)
            cr.paint()
            if draw_serie:
                cr.set_source_rgb(0.0,1.0,0.0)
                cr.set_line_width(2)
                cr.move_to(p1.x+self.margin,p1.y+self.margin)
                cr.line_to(p2.x+self.margin,p2.y+self.margin)
                cr.close_path()
                cr.stroke()
            if draw_rect:
                cr.set_source_rgb(1.0,0.0,0.0)
                cr.rectangle(ll_edge.x+self.margin,ll_edge.y+self.margin,
                             tr_edge.x-ll_edge.x,tr_edge.y-ll_edge.y)
                cr.stroke()
            self.draw_axes(cr,widget)
            cr.pop_group_to_source()
            cr.paint()
    def draw_clipped(self,cr,widget):
        if 1:#try:
            draw_serie=False;draw_rect=False;
            try:
                p1=Point(float(self.get_object("entry1").get_text()),
                        float(self.get_object("entry2").get_text()))
                p2=Point(float(self.get_object("entry3").get_text()),
                        float(self.get_object("entry4").get_text()))
            except:
                pass
            else:
                draw_serie=True
            try:
                ll_edge=Point(float(self.get_object("entry5").get_text()),
                        float(self.get_object("entry6").get_text()))
                tr_edge=Point(float(self.get_object("entry7").get_text()),
                        float(self.get_object("entry8").get_text()))
            except:
                pass
            else:
                draw_rect=True
            cr.set_source_rgb(1.0,1.0,1.0)
            cr.paint()
            if draw_serie:
                cr.set_source_rgb(0.0,1.0,0.0)
                cr.set_line_width(2)
                cr.move_to(p1.x+self.margin,p1.y+self.margin)
                cr.line_to(p2.x+self.margin,p2.y+self.margin)
                cr.close_path()
                cr.stroke()
            if draw_rect:
                ll_edge.x,ll_edge.y,tr_edge.x,tr_edge.y=(
                    min(ll_edge.x,tr_edge.x),
                    min(ll_edge.y,tr_edge.y),
                    max(ll_edge.x,tr_edge.x),
                    max(ll_edge.y,tr_edge.y))
                cr.set_source_rgb(1.0,0.0,0.0)
                cr.rectangle(ll_edge.x+self.margin,ll_edge.y+self.margin,
                             tr_edge.x-ll_edge.x,tr_edge.y-ll_edge.y)
                cr.stroke()
            if self.clipped:
                p1=Point(float(self.get_object("label20").get_text()),
                        float(self.get_object("label24").get_text()))
                p2=Point(float(self.get_object("label26").get_text()),
                        float(self.get_object("label28").get_text()))
                cr.set_source_rgb(1.0,0.0,0.0)
                cr.set_line_width(2)
                cr.move_to(p1.x+self.margin,p1.y+self.margin)
                cr.line_to(p2.x+self.margin,p2.y+self.margin)
                cr.close_path()
                cr.stroke()
            self.draw_axes(cr,widget)
            #cr.paint()
        #except:
        #    pass
    def draw_axes(self,cr,widget):
        zoom=1;min_x,min_y=0,0
        w=widget.get_allocated_width()
        h=widget.get_allocated_height()
        cr.set_source_rgb(0.0,0.0,0.0)

        cr.move_to(5,0)
        cr.line_to(5,h-5);
        cr.line_to(8,h-8);
        cr.move_to(2,h-8)
        cr.line_to(5,h-5)
        cr.move_to(10,h-5)
        cr.show_text("y")
        cr.stroke()

        cr.move_to(0,5)
        cr.line_to(w-10,5)
        cr.line_to(w-13,8)
        cr.move_to(w-13,2)
        cr.line_to(w-10,5)
        cr.move_to(w-7,5)
        cr.show_text("x")
        cr.stroke()
        cr.move_to(10,15)
        cr.show_text('0')
        x=self.margin+50
        while x<w-self.margin:
            cr.move_to(x,2);
            cr.line_to(x,8);
            cr.move_to(x,15);
            cr.show_text(str(int((x-self.margin)/zoom+min_x)));
            x+=50
        cr.stroke();
        y=self.margin+50;
        while y<h-self.margin:
            cr.move_to(2,y);
            cr.line_to(8,y);
            cr.move_to(10,y+5);
            cr.show_text(str(int((y-self.margin)/zoom+min_y)));
            y+=50
        cr.stroke()
    def draw(self,widget,cr,data=None):
        self.draw_clipped(cr,widget)
app=Application("prac1.ui")
app.show("window1")


