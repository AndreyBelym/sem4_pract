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
