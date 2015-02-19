#include <Python.h>
#include "structmember.h"
typedef struct{
    float x,y;
} POINT;
#define LEFT 1
#define RIGHT 2
#define BOT 8
#define TOP 4
/*
Функция locate определяет код точки p относительно прямоугольной области отсечения,
заданной правым верхним углом tr_edge и левым нижним ll_edge.
Возвращает код положения точки - TOP, RIGHT, LEFT или BOTTOM.
Параметры:
p - POINT - точка для определения местоположения
ll_edge - POINT - левый нижний угол области отсечения
tr_edge - POINT - правый верхний угол области отсечения
*/
int locate(POINT p,POINT ll_edge,POINT tr_edge){
    int loc=0;
    if (p.x < ll_edge.x)
        loc|=LEFT;
    else if (p.x > tr_edge.x)
        loc|=RIGHT;
    if (p.y< ll_edge.y)
        loc|=BOT;
    else if (p.y>tr_edge.y)
        loc|=TOP;
    return loc;
}
/*
Функция kohen_sutherland выполняет отсечение отрезка, заданного точками a и b, 
прямоугольной областью, заданной правым верхним углом tr_edge и 
левым нижним ll_edge.
Возвращает 0, если исходный отрезок полностью лежит в области отсечения,
           1 - если лежит частично,
           2 - если вообще не лежит.
Функция модифицирует параметры a и b - в них возвращаются точки отсеченного отрезка.
Параметры:
a,b - POINT - концы исходного отрезка
ll_edge - POINT - левый нижний угол области отсечения
tr_edge - POINT - правый верхний угол области отсечения
*/
int kohen_sutherland(POINT *a,POINT *b,
                            POINT ll_edge,
                            POINT tr_edge){
    
    int loc=0,loc_a=locate(*a,ll_edge,tr_edge),loc_b=locate(*b,ll_edge,tr_edge);
    POINT *c;
    int res=0;
    if (loc_a|loc_b){
        res=1;
        while (loc_a | loc_b){
            if (loc_a & loc_b){
                res=2;
                break;
            }
            if (loc_a) {
                loc = loc_a;
                c = a;
            } else {
                loc = loc_b;
                c = b;
            }
            if (loc & LEFT) {
                c->y += (a->y - b->y) * (ll_edge.x - c->x) / (a->x - b->x);
                c->x = ll_edge.x;
            } else if (loc & RIGHT){
                c->y += (a->y - b->y) * (tr_edge.x - c->x) / (a->x - b->x);
                c->x = tr_edge.x;
            } else if (loc & BOT){
                c->x += (a->x - b->x) * (ll_edge.y - c->y) / (a->y - b->y);
                c->y = ll_edge.y;
            } else if (loc & TOP){
                c->x += (a->x - b->x) * (tr_edge.y - c->y) / (a->y - b->y);
                c->y = tr_edge.y;
            }
            if (loc == loc_a)
                loc_a = locate(*a,ll_edge,tr_edge);
            else
                loc_b = locate(*b,ll_edge,tr_edge);
        }
    }
    return res;
}

typedef struct {
    PyObject_HEAD
    double x;
    double y;
} Py_Point;

static void
Py_Point_dealloc(Py_Point* self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
Py_Point_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Py_Point *self;

    self = (Py_Point *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->x = 0.0;
        self->y = 0.0;
    }

    return (PyObject *)self;
}

static int
Py_Point_init(Py_Point *self, PyObject *args, PyObject *kwds)
{
    if (self!=NULL){
        self->x=0;
        self->y=0;
    }
    if (! PyArg_ParseTuple(args, "|d|d", &self->x, &self->y))
        return -1; 

    return 0;
}


static PyMemberDef Py_Point_Members[] = {
    {"x",T_DOUBLE,offsetof(Py_Point,x),0,""},
    {"y",T_DOUBLE,offsetof(Py_Point,y),0,""},
    {NULL}  /* Sentinel */
};

static PyTypeObject Py_Point_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "alg1.Point",             /* tp_name */
    sizeof(Py_Point),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)Py_Point_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    0,             /* tp_methods */
    Py_Point_Members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Py_Point_init,      /* tp_init */
    0,                         /* tp_alloc */
    Py_Point_new,                 /* tp_new */
};

static PyObject *
kohen_sutherland_wrapper(PyObject *self, PyObject *args){
    #define conv(p,py_p) (p).x=(py_p)->x;(p).y=(py_p)->y 
    POINT a,b,ll_edge,tr_edge;
    Py_Point *py_a,*py_b,*py_tr_edge,*py_ll_edge;
    if (!PyArg_ParseTuple(args, "OOOO", &py_a,&py_b,
                                        &py_ll_edge,
                                        &py_tr_edge))
        return NULL;
    conv(a,py_a); conv(b,py_b);conv(ll_edge,py_ll_edge);conv(tr_edge,py_tr_edge);
    int res=kohen_sutherland(&a,&b,ll_edge,tr_edge);
    py_a->x=a.x;py_b->x=b.x;
    py_a->y=a.y;py_b->y=b.y;
    return PyLong_FromLong(res);
}



static PyMethodDef Alg1Methods[] = {
    {"kohen_sutherland",  kohen_sutherland_wrapper, METH_VARARGS,""},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
static struct PyModuleDef alg1module = {
   PyModuleDef_HEAD_INIT,
   "alg1",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   Alg1Methods
};

PyMODINIT_FUNC
PyInit_alg1(void)
{
    PyObject* m;

    if (PyType_Ready(&Py_Point_Type) < 0)
        return NULL;

    m = PyModule_Create(&alg1module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&Py_Point_Type);
    PyModule_AddObject(m, "Point", (PyObject *)&Py_Point_Type);
    return m;    
}

