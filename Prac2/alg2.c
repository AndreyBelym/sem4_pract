#include <Python.h>
#include <structmember.h>

typedef struct{
    double *elements;
    int n,m;
} MATRIX;

typedef struct{
    double *elements;
    int n;
} VECTOR_f;

typedef struct{
    long *elements;
    int n;
} VECTOR_l;

typedef struct{
    VECTOR_l cols_nums,rows_ptrs;
    VECTOR_f elements;
} RRCU;

int x_in_v(double x,VECTOR_l v,long i0,long i1){
    printf("i1=%ld\n",i1);
    while (i1>=i0&&v.elements[i1]!=x)
        --i1;
    return i1;
}
void print_vf(VECTOR_f v){
    int i;
    for (i=0;i<v.n;++i){
        printf("%f ",v.elements[i]);
    }
    printf("\n");
}


void print_vl(VECTOR_l v){
    int i;
    for (i=0;i<v.n;++i){
        printf("%ld ",v.elements[i]);
    }
    printf("\n");
}
/*
Функция create_rrcu преобразует матрицу а в формат разреженных матриц RR(C)U.
Возврщает матрицу в формате RR(C)U.
Параметры:
a - MATRIX - матрица в стандартном представлении.
*/
RRCU create_rrcu(MATRIX a){
    int i,j,l=0;
    RRCU res;
    res.elements.n=0;res.elements.elements=NULL;
    res.rows_ptrs.n=a.n+1;res.rows_ptrs.elements=malloc((a.n+1)*sizeof(long));
    res.cols_nums.n=0; res.cols_nums.elements=NULL;
    for (i=0;i<a.n;++i){
        res.rows_ptrs.elements[i]=l+1;
        for (j=0;j<a.m;++j){
            if (a.elements[i*a.m+j]!=0.0){
                ++res.elements.n;
                res.elements.elements=realloc(res.elements.elements,
                        res.elements.n*sizeof(double));
                res.elements.elements[l]=a.elements[i*a.m+j];
                ++res.cols_nums.n;
                res.cols_nums.elements=realloc(res.cols_nums.elements,
                        res.cols_nums.n*sizeof(long));
                res.cols_nums.elements[l]=j+1;
                ++l;
            }
        }
    }
    res.rows_ptrs.elements[a.n]=l+1;
    return res;
}
/*
Функция expand_rrcu восстанавливает стандартное представление матрицы из 
матрицы rrcu, заданной в формате RR(C)U, с m столбцами.
Возвращает матрицу в стандартном представлении.
Параметры:
rrcu - RRCU - матрица в формате RR(C)U
m - количество столбцов в полном представлении матрицы.
*/
MATRIX expand_rrcu(RRCU rrcu,int m){
    MATRIX res;
    long i,j;
    res.n=rrcu.rows_ptrs.n-1;
    res.m=m;
    res.elements=calloc(res.n*res.m,sizeof(double));
    for (i=0;i<res.n;++i){
        for (j=rrcu.rows_ptrs.elements[i]-1;
             j<rrcu.rows_ptrs.elements[i+1]-1;
             ++j){
            res.elements[i*res.m+rrcu.cols_nums.elements[j]-1]=
                                            rrcu.elements.elements[j];
        }
    }
    return res;
}
/*
Функция sum_rrcu складвает матрицы rrcu1 и rrcu2, заданных в формате RR(C)U.
Возвращает матрицу - сумму исходных матриц.
rrcu1 - RRCU - первая матрица в формате RR(C)U
rrcu2 - RRCU - вторая матрица в формате RR(C)U
*/
RRCU sum_rrcu(RRCU rrcu1, RRCU rrcu2){
    RRCU res;
    res.rows_ptrs.n=rrcu1.rows_ptrs.n;
    res.rows_ptrs.elements=malloc((rrcu1.rows_ptrs.n)*sizeof(long));
    res.cols_nums.n=0;
    res.cols_nums.elements=NULL;
    res.elements.n=0;
    res.elements.elements=NULL;
    print_vl(rrcu1.rows_ptrs);
    print_vl(rrcu2.rows_ptrs);
    long l=0;
    int i,j,k;
    VECTOR_l used;
    for (i=0;i<rrcu1.rows_ptrs.n-1;i++){
        res.rows_ptrs.elements[i]=l+1;
        printf("1\n------------\n");
        int ja0=rrcu1.rows_ptrs.elements[i]-1,
            ja1=rrcu1.rows_ptrs.elements[i+1]-1,
            jb0=rrcu2.rows_ptrs.elements[i]-1,
            jb1=rrcu2.rows_ptrs.elements[i+1]-1;
        used.n=0;
        printf("ja0=%d ja1=%d\n",ja0,ja1);
        used.elements=NULL;
        for (j=ja0;j<ja1;++j){
            printf("2\n");
            if ((k=x_in_v(rrcu1.cols_nums.elements[j],
                              rrcu2.cols_nums,
                              jb0,jb1-1))>=jb0){

                if (rrcu2.elements.elements[k]!=-rrcu1.elements.elements[j]){
                    printf("31\n");
                    ++res.elements.n;
                    res.elements.elements=realloc(res.elements.elements,
                                            res.elements.n*sizeof(double));
                    res.elements.elements[l]=rrcu1.elements.elements[j]+
                                                    rrcu2.elements.elements[k];
                    ++res.cols_nums.n;
                    res.cols_nums.elements=realloc(res.cols_nums.elements,
                                                res.cols_nums.n*sizeof(long));
                    res.cols_nums.elements[l]=rrcu1.cols_nums.elements[j];
                    ++l;
                }
                ++used.n;
                used.elements=realloc(used.elements,used.n*sizeof(long));
                used.elements[used.n-1]=rrcu1.cols_nums.elements[j];
            }else{
                printf("4\n");
                ++res.elements.n;
                res.elements.elements=realloc(res.elements.elements,
                                            res.elements.n*sizeof(double));
                res.elements.elements[l]=rrcu1.elements.elements[j];
                printf("41\n");
                ++res.cols_nums.n;
                res.cols_nums.elements=realloc(res.cols_nums.elements,
                                            res.cols_nums.n*sizeof(long));
                res.cols_nums.elements[l]=rrcu1.cols_nums.elements[j];
                ++l;
            }
        }
        for (j=jb0;j<jb1;++j){
            printf("5\njb0=%d jb1=%d used.n=%d\n",jb0,jb1,used.n);
            if (x_in_v(rrcu2.cols_nums.elements[j],
                        used,
                        0,used.n-1)<0){
                printf("6\n");
                ++res.elements.n;
                res.elements.elements=realloc(res.elements.elements,
                                        res.elements.n*sizeof(double));
                res.elements.elements[l]=rrcu2.elements.elements[j];
                ++res.cols_nums.n;
                res.cols_nums.elements=realloc(res.cols_nums.elements,
                                            res.cols_nums.n*sizeof(long));
                res.cols_nums.elements[l]=rrcu2.cols_nums.elements[j];
                ++l;
            }
            printf("50\n");
        }
        free(used.elements);
    }
    printf("7\n");
    print_vl(res.rows_ptrs);
    res.rows_ptrs.elements[res.rows_ptrs.n-1]=l+1;
    printf("8\n");
    return res;
}
VECTOR_f PyList_to_VECTORf(PyObject* list){
    VECTOR_f res;
    int i;
    res.n=PyList_Size(list);
    res.elements=malloc(res.n*sizeof(double));
    for (i=0;i<res.n;++i){
        res.elements[i]=PyFloat_AsDouble(PyList_GetItem(list,i));
    }
    return res;
}
PyObject* VECTORf_to_PyList(VECTOR_f v){
    PyObject* list=PyList_New(v.n);
    int i;
    for (i=0;i<v.n;++i){
        PyList_SetItem(list,i,PyFloat_FromDouble(v.elements[i]));
    }
    return list;
}

VECTOR_l PyList_to_VECTORl(PyObject* list){
    VECTOR_l res;
    int i;
    res.n=PyList_Size(list);
    res.elements=malloc(res.n*sizeof(long));
    for (i=0;i<res.n;++i){
        res.elements[i]=PyLong_AsLong(PyList_GetItem(list,i));
    }
    return res;
}
PyObject* VECTORl_to_PyList(VECTOR_l v){
    PyObject* list=PyList_New(v.n);
    int i;
    for (i=0;i<v.n;++i){
        PyList_SetItem(list,i,PyLong_FromLong(v.elements[i]));
    }
    return list;
}

MATRIX PyList_to_MATRIX(PyObject* list){
    int i,j;
    MATRIX res;
    res.n=PyList_Size(list);
    PyObject *line=PyList_GetItem(list,0);
    res.m=PyList_Size(line);
    res.elements=malloc(res.m*res.n*sizeof(double));
    for (i=0;i<res.n;i++){
        line=PyList_GetItem(list,i);
        for (j=0;j<res.m;j++){
            res.elements[i*res.m+j]=PyFloat_AsDouble(PyList_GetItem(line,j));    
        }
    }
    return res;
}

PyObject* MATRIX_to_PyList(MATRIX matrix){
    PyObject* res=PyList_New(matrix.n);
    int i,j;
    for (i=0;i<matrix.n;++i){
        PyObject* line=PyList_New(matrix.m);
        PyList_SetItem(res,i,line);
        for(j=0;j<matrix.m;++j){
            PyList_SetItem(line,j,PyFloat_FromDouble(matrix.elements[i*matrix.m+j]));
        }
    }
    return res;
}

typedef struct {
    PyObject_HEAD;
    /* Type-specific fields go here. */
    PyObject *rows_ptrs,*cols_nums, *elements;
} Py_RRCU;

static void
Py_RRCU_dealloc(Py_RRCU* self)
{
    Py_XDECREF(self->rows_ptrs);
    Py_XDECREF(self->cols_nums);
    Py_XDECREF(self->elements);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
Py_RRCU_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Py_RRCU *self;
    printf("New X\n");
    self = (Py_RRCU *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->rows_ptrs = Py_None; 
        if (self->rows_ptrs == NULL)
          {
            Py_DECREF(self);
            return NULL;
          }
        Py_INCREF(Py_None);
        self->cols_nums = Py_None;
        if (self->cols_nums == NULL)
          {
            Py_DECREF(self);
            return NULL;
          }
        Py_INCREF(Py_None);
        self->elements = Py_None;
        if (self->cols_nums == NULL)
          {
            Py_DECREF(self);
            return NULL;
          }
    }

    return (PyObject *)self;
}

static int
Py_RRCU_init(Py_RRCU *self, PyObject *args, PyObject *kwds)
{
   // PyObject *rows_ptrs,*cols_nums,*elements;
    PyObject *py_matrix=Py_None;
    MATRIX matrix;
    RRCU new_rrcu;
    printf("init 0\n");
    if (! PyArg_ParseTuple(args,"|O",&py_matrix))
        return -1;
    Py_DECREF(self->elements);
    Py_DECREF(self->cols_nums);
    Py_DECREF(self->rows_ptrs);
    if (PyObject_IsTrue(py_matrix)&&PyList_Check(py_matrix)){
        matrix=PyList_to_MATRIX(py_matrix);
        new_rrcu=create_rrcu(matrix);
        free(matrix.elements);
        self->elements=VECTORf_to_PyList(new_rrcu.elements);
        self->rows_ptrs=VECTORl_to_PyList(new_rrcu.rows_ptrs);
        self->cols_nums=VECTORl_to_PyList(new_rrcu.cols_nums);
        free(new_rrcu.elements.elements);
        free(new_rrcu.rows_ptrs.elements);
        free(new_rrcu.cols_nums.elements);
    }else{
        self->elements=PyList_New(0);
        self->cols_nums=PyList_New(0);
        self->rows_ptrs=PyList_New(0);
    }
    printf("Init X\n");
    return 0;
}


static PyMemberDef Py_RRCU_members[] = {
    {"rows_ptrs", T_OBJECT_EX, offsetof(Py_RRCU,rows_ptrs ), 0,
     "first name"},
    {"cols_nums", T_OBJECT_EX, offsetof(Py_RRCU,cols_nums ), 0,
     "last name"},
    {"elements", T_OBJECT_EX, offsetof(Py_RRCU,elements ), 0,
     "noddy number"},
    {NULL}  /* Sentinel */
};

static PyTypeObject Py_RRCUType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "alg2.RRCU",             /* tp_name */
    sizeof(Py_RRCU), /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)Py_RRCU_dealloc,  /* tp_dealloc */
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
    Py_TPFLAGS_DEFAULT,        /* tp_flags */
    "RRCU sparse matrix",           /* tp_doc */
    0,                     /* tp_traverse */
    0,                     /* tp_clear */
    0,                     /* tp_richcompare */
    0,                     /* tp_weaklistoffset */
    0,                     /* tp_iter */
    0,                     /* tp_iternext */
    0,                     /* tp_methods */
    Py_RRCU_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Py_RRCU_init,      /* tp_init */
    0,                         /* tp_alloc */
    Py_RRCU_new,       
};

static PyObject* expand_rrcu_wrapper(PyObject *self, PyObject *args){
    long m;
    MATRIX matrix;
    PyObject *res;
    Py_RRCU *py_rrcu;
    RRCU rrcu;
    PyArg_ParseTuple(args,"Oi",&py_rrcu,&m);
    
    rrcu.cols_nums=PyList_to_VECTORl(py_rrcu->cols_nums);
    rrcu.rows_ptrs=PyList_to_VECTORl(py_rrcu->rows_ptrs);
    rrcu.elements=PyList_to_VECTORf(py_rrcu->elements);
    
    matrix=expand_rrcu(rrcu,m);
    res=MATRIX_to_PyList(matrix);

    free(matrix.elements);
    free(rrcu.elements.elements);
    free(rrcu.rows_ptrs.elements);
    free(rrcu.cols_nums.elements);

    return res;
}

PyObject* sum_rrcu_wrapper(PyObject* self,PyObject *args){
    RRCU a,b,c;
    Py_RRCU *py_a,*py_b,*py_c;
    PyArg_ParseTuple(args,"OO",&py_a,&py_b);
    a.cols_nums=PyList_to_VECTORl(py_a->cols_nums);
    a.rows_ptrs=PyList_to_VECTORl(py_a->rows_ptrs);
    a.elements=PyList_to_VECTORf(py_a->elements);
    b.cols_nums=PyList_to_VECTORl(py_b->cols_nums);
    b.rows_ptrs=PyList_to_VECTORl(py_b->rows_ptrs);
    b.elements=PyList_to_VECTORf(py_b->elements);
    c=sum_rrcu(a,b);
    
    PyObject* temp_args=Py_BuildValue("(O)",Py_None);
    py_c=(Py_RRCU*)PyObject_CallObject((PyObject*)&Py_RRCUType,temp_args);
    Py_XDECREF(temp_args);
    printf("A\n");
    py_c->rows_ptrs=VECTORl_to_PyList(c.rows_ptrs);
    py_c->cols_nums=VECTORl_to_PyList(c.cols_nums);
    py_c->elements=VECTORf_to_PyList(c.elements);
    printf("B\n");
    free(c.rows_ptrs.elements);free(c.cols_nums.elements);free(c.elements.elements);
    free(b.rows_ptrs.elements);free(b.cols_nums.elements);free(b.elements.elements);
    free(a.rows_ptrs.elements);free(a.cols_nums.elements);free(a.elements.elements);

    return (PyObject*)py_c;
}

static PyMethodDef alg2methods[]={

    {"expand_rrcu",expand_rrcu_wrapper,METH_VARARGS,""},
    {"sum_rrcu",sum_rrcu_wrapper,METH_VARARGS,""},
    {NULL,NULL,0,NULL}
};
static PyModuleDef alg2module = {
    PyModuleDef_HEAD_INIT,
    "alg2",
    "RRCU sparse matrix algorhytms",
    -1,
    alg2methods
};

PyMODINIT_FUNC
PyInit_alg2(void) 
{
    PyObject* m;

    if (PyType_Ready(&Py_RRCUType) < 0)
        return NULL;

    m = PyModule_Create(&alg2module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&Py_RRCUType);
    PyModule_AddObject(m, "RRCU", (PyObject*)&Py_RRCUType);
    return m;
}
