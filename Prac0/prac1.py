#!/usr/bin/env python
from copy import copy
import cairo
from gi.repository import Gtk,Gdk
from alg1 import Point, kohen_sutherland
'''class point:
    def __init__(self,x=None,y=None):
        if x:
            self.x=x
        else: 
            self.x=0
        if y:
            self.y=y
        else: 
            self.y=0
'''
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

'''    LEFT,RIGHT,BOT,TOP=1,2,8,4
    def locate(p):
        loc=0;
        if p.x < ll_edge.x :
            loc|=LEFT
        elif p.x > tr_edge.x:
            loc|=RIGHT
        if p.y< ll_edge.y:
            loc|=BOT
        elif p.y>tr_edge.y:
            loc|=TOP
        return loc
    loc_a,loc_b=locate(a),locate(b)
    r=0
    while (loc_a | loc_b):
        r=1
        if (loc_a & loc_b):
                return 2,a,b;

        if (loc_a) :
                loc = loc_a;
                c = a;
        else:
                loc = loc_b;
                c = b;
        
        if (loc & LEFT) :
                c.y += (a.y - b.y) * (ll_edge.x - c.x) / (a.x - b.x);
                c.x = ll_edge.x;
        elif (loc & RIGHT):
                c.y += (a.y - b.y) * (tr_edge.x - c.x) / (a.x - b.x);
                c.x = tr_edge.x;
        elif (loc & BOT):
                c.x += (a.x - b.x) * (ll_edge.y - c.y) / (a.y - b.y);
                c.y = ll_edge.y;
        elif (loc & TOP):
                c.x += (a.x - b.x) * (tr_edge.y - c.y) / (a.y - b.y);
                c.y = tr_edge.y;
        if (loc == loc_a):
                loc_a = locate(a);
        else:
                loc_b = locate(b);
    return r,a,b'''
class Application(Gtk.Builder):
    
    def __init__(self,ui_filename):
        self.clipped=False
        Gtk.Builder.__init__(self)
        self.add_from_file(ui_filename)
        self.connect_signals(self)
        self.margin=5
    def show_msg(self,msg):
        md=Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, msg);
        md.run ();
        md.destroy();
    def show(self,form_name):
        window = self.get_object(form_name)
        window.show()
        Gtk.main()
    def on_window_destroy( self,widget, data=None):
        Gtk.main_quit()
    def get_value(self,name):
        return int(float(self.get_object(name).get_text()))
    def on_run_clicked(self,button,data=None):
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
            return
        res=kohen_sutherland(p1,p2,ll_edge,tr_edge)
        p1_info=self.get_object("label19");p2_info=self.get_object("label20");
        res_info=self.get_object("label21");
        if not res:
            res_info.set_text("Отрезок расположен в прямоугольнике")
            p1_info.set_text("X: {0}; Y: {1}".format(int(p1.x),int(p1.y)))
            p2_info.set_text("X: {0}; Y: {1}".format(int(p2.x),int(p2.y)))
        elif res==2:
            res_info.set_text("Отрезок не расположен в прямоугольнике")
            p1_info.set_text("Не существует")
            p2_info.set_text("Не существует")
        elif res==1:
            res_info.set_text("Отрезок частично расположен в прямоугольнике")
            p1_info.set_text("X: {0}; Y: {1}".format(int(p1.x),int(p1.y)))
            p2_info.set_text("X: {0}; Y: {1}".format(int(p2.x),int(p2.y)))
        else:
            res_info.set_text("Извините, маленькие технические неполадки")
        self.clipped=True
        self.get_object('drawingarea1').queue_draw()
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
                cr.rectangle(ll_edge.x+self.margin,ll_edge.y+self.margin,tr_edge.x-ll_edge.x,tr_edge.y-ll_edge.y)
                cr.stroke()
            self.draw_axes(cr,widget)
            cr.pop_group_to_source()
            cr.paint()
    def draw_clipped(self,cr,widget):
        if 1:#try:
            p1=Point(float(self.get_object("entry1").get_text()),
                    float(self.get_object("entry2").get_text()))
            p2=Point(float(self.get_object("entry3").get_text()),
                    float(self.get_object("entry4").get_text()))
            ll_edge=Point(float(self.get_object("entry5").get_text()),
                    float(self.get_object("entry6").get_text()))
            tr_edge=Point(float(self.get_object("entry7").get_text()),
                    float(self.get_object("entry8").get_text()))
            ll_edge.x,ll_edge.y,tr_edge.x,tr_edge.y=(
                min(ll_edge.x,tr_edge.x),
                min(ll_edge.y,tr_edge.y),
                max(ll_edge.x,tr_edge.x),
                max(ll_edge.y,tr_edge.y))
            if (ll_edge.x==tr_edge.x  or ll_edge.y==tr_edge.y):            
                return
            '''    margin=20
            w=widget.get_allocated_width()
            h=widget.get_allocated_height()
            min_x=min(p1.x,p2.x,ll_edge.x,tr_edge.x)
            max_x=max(p1.x,p2.x,ll_edge.x,tr_edge.x)
            zoom_x=(w-2*margin)/(max_x-min_x)

            min_y=min(p1.y,p2.y,ll_edge.y,tr_edge.y)
            max_y=max(p1.y,p2.y,ll_edge.y,tr_edge.y)
            zoom_y=(h-2*margin)/(max_y-min_y)

            zoom=min(zoom_x,zoom_y)
            '''
            cr.set_source_rgb(1.0,1.0,1.0)
            cr.paint()
            '''cr.set_source_rgb(0.0,1.0,0.0)
            cr.set_line_width(2)
            cr.move_to(p1.x+self.margin,p1.y+self.margin)
            cr.line_to(p2.x+self.margin,p2.y+self.margin)
            cr.close_path()
            cr.stroke()'''
            cr.set_source_rgb(1.0,0.0,0.0)
            cr.rectangle(ll_edge.x+self.margin,ll_edge.y+self.margin,tr_edge.x-ll_edge.x,tr_edge.y-ll_edge.y)
            cr.stroke()
            '''
            cr.set_source_rgb(0.0,1.0,0.0)
            cr.set_line_width(2)
            cr.move_to(zoom*(p1.x-min_x)+margin,zoom*(p1.y-min_y)+margin)
            cr.line_to(zoom*(p2.x-min_x)+margin,zoom*(p2.y-min_y)+margin)
            cr.close_path()
            cr.stroke()
            cr.set_source_rgb(1.0,0.0,0.0)
            cr.rectangle(zoom*(ll_edge.x-min_x)+margin,zoom*(ll_edge.y-min_y)+margin,zoom*(tr_edge.x-ll_edge.x),zoom*(tr_edge.y-ll_edge.y))
            cr.stroke()
            '''
            res=kohen_sutherland(p1,p2,ll_edge,tr_edge)
            if res<2:
                cr.set_source_rgb(1.0,0.0,0.0)
                cr.set_line_width(2)
                cr.move_to(p1.x+self.margin,p1.y+self.margin)
                cr.line_to(p2.x+self.margin,p2.y+self.margin)
                cr.close_path()
                cr.stroke()
                '''cr.move_to(zoom*(p1.x-min_x)+margin,zoom*(p1.y-min_y)+margin)
                cr.line_to(zoom*(p2.x-min_x)+margin,zoom*(p2.y-min_y)+margin)
                cr.close_path()
                cr.stroke()
                '''
            self.draw_axes(cr,widget)
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
        if self.clipped:
            self.draw_clipped(cr,widget)
        else:
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
                cr.set_source_rgb(1.0,0.0,0.0)
                cr.rectangle(ll_edge.x+self.margin,ll_edge.y+self.margin,tr_edge.x-ll_edge.x,tr_edge.y-ll_edge.y)
                cr.stroke()
            self.draw_axes(cr,widget)
app=Application("prac1.ui")
app.show("window1")


