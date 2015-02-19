#!/usr/bin/env python
from copy import deepcopy,copy
from gi.repository import Gtk
from locale import atof,atoi
import subprocess as subp
from imp import reload

def dijkstra(matrix,src,dst):
    '''
    Функция dijkstra ищет кратчайщий путь в графе,
    заданном матрицей смежности matrix,
    из вершины src в вершину dst.
    Возвращает кортеж из длины найденного пути, и
    списка вершин пути.
    Параметры:
    matrix - [double] - матрица смежности,
    src - int - начальная вершина,
    dst - int - конечная вершина
    '''
    src0=src
    dist=[float("inf") for i in matrix]
    dist[src]=0
    prev=[src for i in matrix]
    visited=set()
    if src==dst:
        return (0,[src])
    while len(visited)!=len(matrix):
        minv=float("inf");mini=src
        for i in range(0,len(matrix[src])):
            if i not in visited and i!=src:
                alt=dist[src]+matrix[src][i]
                if alt<dist[i]:
                    dist[i]=alt
                    prev[i]=src
                if dist[i]<minv:
                    minv=dist[i]
                    mini=i
        visited.add(src)
        src=mini
        if src==dst or minv==inf:
            break
    #print(prev,src0,dst)
    path=get_path(prev,src0,dst)
    return dist[dst],path


def get_path(prev,src,dst):
    #print(src,dst)
    path=[dst]
    while dst!=src and dst!=prev[dst]:
        #print(prev[dst])
        path.append(prev[dst])
        dst=prev[dst]
    path.reverse()
    return path

def check_matrix(m1,m2):
    for i in range(0,len(m1)):
        for j in range(0,len(m1[i])):
            if m1[i][j]!=m2[i][j]:
                break
        else:
            continue
        break
    else:
        return True
    return False
def equal_paths(p1,p2,i):
    if i>=len(p2):
        print(0)
        return False;
    for n in range(0,i+1):
        if p1[i]!=p2[i]:
            break
    else:
        return True
    return False

def calc_weigth(matrix,p):
    w=0
    for i in range(0,len(p)-1):
        w+=matrix[p[i]][p[i+1]]
    return w

def yen(matrix,src,dst,k):
    '''
    Функция yen ищет не более k кратчайших путей в графе,
    заданном матрицей смежности matrix,
    из вершины src в вершину dst. Если в графе не может быть найдено k
    кратчайших путей, возвращается лишь найденное количество.
    Возвращает список длиной не более k, состоящий из кортежей,
    в которых записана длина найденного пути, и
    список вершин пути.
    Параметры:
    matrix - [double] - матрица смежности,
    src - int - начальная вершина,
    dst - int - конечная вершина,
    k - int - желаемое количество кратчайших путей.
    '''
    paths=[dijkstra(matrix,src,dst)]
    candidates=[]
    c=1;
    while c<k:
        prev_path=paths[c-1]
        
        minw=inf
        paths.append((inf,None));
        for i in range(0,len(prev_path[1])-1):
            t_matrix=deepcopy(matrix)
            
            for p_j in paths[:-1]:
                
                if equal_paths(prev_path[1],p_j[1],i):
                    t_matrix[prev_path[1][i]][p_j[1][i+1]]=inf
                    
            r_w=calc_weigth(matrix,prev_path[1][0:i+1])
            for j in prev_path[1][0:i]:
                for m in range(0,len(t_matrix[j])):
                    pass
                    t_matrix[j][m]=inf
                    t_matrix[m][j]=inf
            new_p=dijkstra(t_matrix,prev_path[1][i],dst)
            new_path=(new_p[0]+r_w#calc_weigth(t_matrix,prev_path[1][0:i]+new_p[1])
                      ,prev_path[1][0:i]+new_p[1]);

            candidates.append(new_path)
        for new_path in candidates:
            if new_path[0]<minw:
                paths[c]=new_path
                minw=new_path[0]
        if minw==inf:
            break
        else:
            while paths[c] in candidates:
                candidates.remove(paths[c])
        c+=1
    return paths

def check_symmetry(matrix):
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            if matrix[i][j]!=matrix[j][i]:
                break
        else:
            continue
        break
    else:
        return True
    return False

def mat_to_dot(matrix,path=None):
    a=deepcopy(matrix)
    if check_symmetry(matrix):
        graph_type='graph '
        sep='--'
    else:
        graph_type='digraph '
        sep='->'
    dot_p=""
    for i in range(0,len(matrix)):
        if path and i+1 in path:
            
            dot_p+=str(i+1)+"[color=green,fontcolor=green]\n"
        else:
            dot_p+=str(i+1)+'\n'
        
    for i in range(0,len(matrix)):
        if graph_type=='graph ':
            beg=i+1
        else:
            beg=0
        for j in range(beg,len(matrix[i])):
            if matrix[i][j]!=inf and i!=j:
                x,y=0,0
                if path and (i+1) in path and (j+1) in path:
                    x,y=path.index(i+1),path.index(j+1)
                if abs(x-y)==1:
                    dot_p+=(str(path[x])+sep+str(path[y])+
                            '[color=green,fontcolor=green,label='+
                                str(matrix[path[x]-1][path[y]-1])+"]\n")
                else:    
                    dot_p+=str(i+1)+sep+str(j+1)+"[label="+str(matrix[i][j])+"]\n"
    dot_p=graph_type+"G{\n"+dot_p+"}"
    return dot_p

class Application(Gtk.Builder):
    def __init__(self,ui_filename):
        self.clipped=False
        Gtk.Builder.__init__(self)
        self.add_from_file(ui_filename)
        self.connect_signals(self)
        self.graphviz=None
    def _graphviz_init(self):
        args=[]
        args.append('dot')
        args.append('-T')
        args.append('x11')
        return subp.Popen(args ,shell=False,stdin=subp.PIPE); 
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
        if self.graphviz and self.graphviz.poll()==None:
            self.graphviz.terminate()
            print("killed")
            if self.graphviz.poll()==None:
                self.graphviz.kill()
        Gtk.main_quit()

    def adj_changed(*args):
        print("changed")
    def clear_table(self,table):
        model=table.get_model()
        if model:
            model.clear()
        c=table.get_column(0)
        while c:
            table.remove_column(c)
            c=table.get_column(0)

    def on_resize_click(self,widget,data=None):
        table=self.get_object("treeview1")
        self.clear_table(table)
        self.update_tables()
        n=round(self.get_object("adjustment1").get_value())
        for adj in ((self.get_object(i) for i in('adjustment2','adjustment3'))):
            adj.set_property('upper',n)
        table=self.get_object("treeview2")
        table.get_model().clear()

    def resize_click(self,widget,data=None):
        n=round(self.get_object("adjustment1").get_value())
        table="treeview1"
        mat=[[float('inf') for j in range(0,n)] for i in range(0,n)]
        model=self.get_object(table).get_model()
        i=0;j=0;
        for x in model:
            i+=1;j=0
            if i>n:
                break;
            for y in x:
                j+=1
                if j>n:
                    break
                mat[i-1][j-1]=y
        model=self.get_object('liststore3')
        model.clear()
        for i in range(0,n):
            model.append([i+1])
        self.clear_table(self.get_object(table))
        self.create_table(table,2,float,mat,True)
        for adj in ((self.get_object(i) for i in('adjustment2','adjustment3'))):
            adj.set_property('upper',n)
        table=self.get_object("treeview2")
        table.get_model().clear()

    def update_tables(self):
        n=round(self.get_object("adjustment1").get_value())
        empty_mat=[[float('inf') for j in range(0,n)] for i in range(0,n)]
        self.create_table("treeview1",2,float,empty_mat,True)
        model=self.get_object('liststore3')
        model.clear()
        for i in range(0,n):
            model.append([i+1])
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
                if el_type==float:
                    rend.connect("edited",self.on_cell_edit_f,(model,i))
            col = Gtk.TreeViewColumn(str(i+1), rend)
            col.add_attribute(rend,"text",i)
            table.append_column(col)

    def on_cell_edit_f(self, widget, path, text,data=None):
        model,col=data
        model[path][col]=atof(text)

    def input_data(self):
        matrix=[[j for j in i] for i in self.get_object("treeview1").get_model()]
        src=round(self.get_object("adjustment2").get_value())-1
        dst=round(self.get_object("adjustment3").get_value())-1
        k=int(self.get_object("entry1").get_text())
        return matrix,src,dst,k
    def output_data(self,paths):
        model=self.get_object("treeview2").get_model()
        model.clear()
        for w,p in paths:
            if p and w!=inf:
                model.append([w,"->".join((str(i+1) for i in p))])
    def on_run_click(self,widget,data=None):
        matrix,src,dst,k=self.input_data()
        paths=yen(matrix,src,dst,k)
        self.output_data(paths)
        
    def on_graph_show(self,widget,data=None):
        if self.graphviz and self.graphviz.poll()==None:
            self.graphviz.terminate()
            if self.graphviz.poll()==None:
                self.graphviz.kill()
        graphviz=self._graphviz_init()
        self.graphviz=graphviz
        matrix=[[j for j in i] for i in self.get_object("treeview1").get_model()]
        dot=mat_to_dot(matrix)
        graphviz.stdin.write(dot.encode()+b"\n")
        graphviz.stdin.close()        
    def on_path_show(self,widget,data=None):
        if self.graphviz and self.graphviz.poll()==None:
            self.graphviz.terminate()
            if self.graphviz.poll()==None:
                self.graphviz.kill()
        graphviz=self._graphviz_init()
        self.graphviz=graphviz
        matrix=[[j for j in i] for i in self.get_object("treeview1").get_model()]
        model=self.get_object("treeview2").get_model()
        selection=self.get_object("treeview2").get_selection()
        print (selection.get_selected_rows()[1])
        path=[int(i) for i in model[selection.get_selected_rows()[1][0]][1].split("->")]
        dot=mat_to_dot(matrix,path)
        #print (dot.encode()+b"\n\x04")
        #print(self.graphviz)
        #print(dir(self.graphviz))
        graphviz.stdin.write(dot.encode()+b"\n")

        graphviz.stdin.close()
    def make_symmetric(self,widget,data=None):
        print("ok")
        table=self.get_object("treeview1")
        matrix=[[j for j in i] for i in table.get_model()]
        for i in range(0,len(matrix)):
            for j in range(i+1,len(matrix[i])):
                matrix[j][i]=matrix[i][j]
        self.clear_table(table)
        self.create_table("treeview1",2,float,matrix,True)
    def on_help_show(self,widget,*args):
        self.show('window2');
    def on_help_destroy(self,widget,*args):
        widget.hide()
        widget.destroy()
    def on_help_close(self,widget,*args):
        self.get_object('window2').destroy()
    def on_close(self,widget,*args):
        self.get_object('window1').destroy()
        
inf=float("inf")
app=Application("prac5.ui")
app.show("window1")
  
