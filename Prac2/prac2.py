#!/usr/bin/env python
from gi.repository import Gtk
from locale import atof,atoi
from alg2 import RRCU,expand_rrcu,sum_rrcu

class Application(Gtk.Builder):
    def __init__(self,ui_filename):
        Gtk.Builder.__init__(self)
        self.add_from_file(ui_filename)
        self.connect_signals(self)
        self.liststoresA=[]
        self.liststoresB=[]
        self.liststoresC=[]
        self.update_tables()
    def show(self,form_name):
        window = self.get_object(form_name)
        window.show()
        Gtk.main()
    def show_msg(self,msg):
        md=Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
                             Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, msg);
        md.run ();
        md.destroy();
    def clear_table(self,table):
        model=table.get_model()
        if model:
            model.clear()
        try:
            c=table.get_column(0)
            while c:
                table.remove_column(c)
                c=table.get_column(0)
        except:
            pass
    def on_resize_click(self,widget,data=None):
        for table in (self.get_object("treeview1"),
                      self.get_object("treeview2"),
                      self.get_object("treeview3"),
                      self.get_object("treeview4"),
                      self.get_object("treeview5"),
                      self.get_object("treeview6"),
                      self.get_object("treeview7"),
                      self.get_object("treeview8"),
                      self.get_object("treeview9"),
                      self.get_object("treeview10"),
                      self.get_object("treeview11"),
                      self.get_object("treeview12")):
            self.clear_table(table)
        self.update_tables()
    def resize_click(self,widget,data=None):
        for table in (self.get_object("treeview3"),
                      self.get_object("treeview4"),
                      self.get_object("treeview5"),
                      self.get_object("treeview6"),
                      self.get_object("treeview7"),
                      self.get_object("treeview8"),
                      self.get_object("treeview9"),
                      self.get_object("treeview10"),
                      self.get_object("treeview11"),
                      self.get_object("treeview12")):
            self.clear_table(table)
        n=round(self.get_object("adjustment1").get_value())
        m=round(self.get_object("adjustment2").get_value())
        for table in ("treeview1",
                      "treeview2"):
            mat=[[0.0 for j in range(0,m)] for i in range(0,n)]
            model=self.get_object(table).get_model()
            i=0;j=0;
            for x in model:
                i+=1;j=0
                if i>n:
                    break;
                for y in x:
                    j+=1
                    if j>m:
                        break
                    mat[i-1][j-1]=y
            
            self.clear_table(self.get_object(table))
            self.create_table(table,2,str,mat,True)
        mat=[[str(0.0) for j in range(0,m)] for i in range(0,n)]
        self.create_table("treeview3",2,str,mat)
        row_model=self.get_object("liststoreRows")
        row_model.clear()
        for i in range(1,n+1):
            row_model.append([i])
    def update_tables(self):
        n=round(self.get_object("adjustment1").get_value())
        m=round(self.get_object("adjustment2").get_value())
        empty_mat=[[str(0.0) for j in range(0,m)] for i in range(0,n)]
        self.create_table("treeview1",2,str,empty_mat,True)
        self.create_table("treeview2",2,str,empty_mat,True)
        self.create_table("treeview3",2,str,empty_mat)
        row_model=self.get_object("liststoreRows")
        row_model.clear()
        for i in range(1,n+1):
            row_model.append([i])
    def on_window_destroy( self,widget, data=None):
        #self.get_object('window2').destroy()
        widget.hide()
        widget.destroy()
        Gtk.main_quit()
    def create_table(self,name,dim,el_type,data,editable=False):
        table=self.get_object(name)
        model=table.get_model()
        self.clear_table(table)
        if dim==1:
            m=len(data)
        elif dim==2:
            m=len(data[0])
        model=Gtk.ListStore(*(el_type for j in range(0,m)))
        if dim==1:
            model.append(data)
        elif dim==2:
            for i in data:
                model.append(i)
        table.set_model(model)
        for i in range(0,m):
            rend = Gtk.CellRendererText()
            if editable:
                rend.set_property("editable",True)
                if el_type==str:
                    rend.connect("edited",self.on_cell_edit_f,(model,i))
            col = Gtk.TreeViewColumn(str(i+1), rend)
            col.add_attribute(rend,"text",i)
            table.append_column(col)
    def on_cell_edit_f(self, widget, path, text,data=None):
        model,col=data
        model[path][col]=str(float(text))
    def on_matrix_a_ok(self,widget,data=None):
        a=[[float(j) for j in i] for i in self.get_object("treeview1").get_model()]
        rrcu_a=RRCU(a)
        self.create_table("treeview4",1,int,rrcu_a.rows_ptrs)
        self.create_table("treeview5",1,int,rrcu_a.cols_nums)
        self.create_table("treeview6",1,float,rrcu_a.elements)
        self.rrcu_a=rrcu_a
        
    def on_matrix_b_ok(self,widget,data=None):
        b=[[float(j) for j in i] for i in self.get_object("treeview2").get_model()]
        rrcu_b=RRCU(b)
        self.create_table("treeview7",1,int,rrcu_b.rows_ptrs)
        self.create_table("treeview8",1,int,rrcu_b.cols_nums)
        self.create_table("treeview9",1,float,rrcu_b.elements)
        self.rrcu_b=rrcu_b

    def input_data(self):
        try:
            if self.rrcu_a==None:
                print(1)
                self.show_msg("Матрица A не создана!")
                raise
        except:
            self.show_msg("Матрица A не создана!")
            raise
        try :               
            if self.rrcu_b==None:
                self.show_msg("Матрица B не создана!")
                raise
        except:
            self.show_msg("Матрица B не создана!")
            raise
        return self.rrcu_a,self.rrcu_b
    def output_data(self,rrcu_c):
        if rrcu_c:
            self.create_table("treeview10",1,int,rrcu_c.rows_ptrs)
            self.create_table("treeview11",1,int,rrcu_c.cols_nums)
            self.create_table("treeview12",1,float,rrcu_c.elements)
            n=round(self.get_object("adjustment1").get_value())
            m=round(self.get_object("adjustment2").get_value())
            c=[[str(j) for j in i] for i in expand_rrcu(rrcu_c,m)]
            self.create_table("treeview3",2,str,c)
    def on_run_click(self,widget,data=None):
        rrcu_a,rrcu_b=self.input_data()
        rrcu_c=sum_rrcu(rrcu_a,rrcu_b);
        self.output_data(rrcu_c);
    def on_help_show(self,widget,*args):
        self.show('window2');
    def on_help_destroy(self,widget,*args):
        widget.hide()
        widget.destroy()
    def on_help_close(self,widget,*args):
        self.get_object('window2').destroy()
    def on_close(self,widget,*args):
        self.get_object('window1').destroy()
app=Application("prac2.ui")
app.show("window1")

