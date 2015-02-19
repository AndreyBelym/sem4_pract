#include <Python.h>

typedef struct{
    double *elements;
    int n,m;
} MATRIX;

typedef struct{
    double *elements;
    int n;
} VECTOR;

typedef struct{
    int i,j;
} COORD;
VECTOR gauss_direct(MATRIX a){
    int i,j,k;
    VECTOR index;
    index.elements=malloc(a.n*sizeof(double));
    index.n=a.n;
    for (i=0;i<index.n;++i)
        index.elements[i]=i;
    
    COORD index_of_max(void){
        
        COORD max;
        int j,k;
        double m=abs(a.elements[i*a.m+i]);
        max.i=i,max.j=i;
        for (j=i;j<a.n;++j){
            for (k=i;k<a.n;++k){
                if (abs(a.elements[j*a.m+k])>m){
                    m=abs(a.elements[j*a.m+k]);max.i=j;max.j=k;
                }
            }
        }
        return max;
    }
    for (i=0;i<a.n;++i){
        COORD max=index_of_max();
        if (a.elements[max.i*a.m+max.j]==0){
            return index;
        }
        if (max.i!=i){
            double temp;
            for (j=i;j<a.m;++j){
                temp=a.elements[i*a.m+j];
                a.elements[i*a.m+j]=a.elements[max.i*a.m+j];
                a.elements[max.i*a.m+j]=temp;
            }
        }
        if (max.j!=i){    
            int temp_i=index.elements[max.j];
            index.elements[max.j]=index.elements[i];
            index.elements[i]=temp_i;
            double temp;
            for (j=0;j<a.n;++j){
                temp=a.elements[j*a.m+i];
                a.elements[j*a.m+i]=a.elements[j*a.m+max.j];
                a.elements[j*a.m+max.j]=temp;
            }
        }
        for (j=i+1;j<a.n;++j){
            if (!a.elements[i*a.m+i])
                printf("Error!\n");
            double factor=a.elements[j*a.m+i]/a.elements[i*a.m+i];
            a.elements[j*a.m+i]=0;
            int k;
            for (k=i+1;k<a.m;++k){
                a.elements[j*a.m+k]-=a.elements[i*a.m+k]*factor;
                /*if (abs(a.elements[j*a.m+k])<1e-10)
                    a.elements[j*a.m+k]=0;*/
            }
        }
        
    }
    return index;
}

VECTOR gauss_reverse(MATRIX a){
    int i,j;
    VECTOR res;
    res.elements=malloc(a.n*sizeof(double));
    res.n=a.n;
    for(i=0;i<a.n;i++)
        res.elements[i]=a.elements[i*a.m+a.m-1];
    
    for (i=a.n-1;i>=0;--i){
        for (j=a.n-1;j>i;--j)
            res.elements[i]-=a.elements[i*a.m+j]*res.elements[j];
        res.elements[i]/=a.elements[i*a.m+i];
    }
    return res;
}

void return_order(VECTOR *values,VECTOR index){
    int i;
    double *res;
    res=malloc(values->n*sizeof(double));
    for (i=0;i<values->n;++i)
        res[(int)index.elements[i]]=values->elements[i];
    free(values->elements);
    values->elements=res;
}
/*
Функция create_sys создает матрицу системы для решения уравнения Фредгольма
второго рода,  используя таблично-заданные 
ядро k_d и свободную составляющую f_d, с шагом h на интервале [a,b].
Возвращает матрицу системы.
Параметры:
k - MATRIX - таблично-заданное ядро уравнения
f - VECTOR - таблично-заданная свободная функция
h - double - шаг поиска решения
a,b - double - интервал поиска решения
*/
MATRIX create_sys(MATRIX k,VECTOR f,double h,double a,double b){
    int i,j;
    MATRIX res;
    int n=round((b-a)/h+1);
    res.n=n;res.m=n+1;
    res.elements=malloc(res.n*res.m*sizeof(double));
    if (res.elements==NULL)
        printf("Error!\n");
    for (i=0;i<n;i++){
        for (j=0;j<n;++j)
            res.elements[i*res.m+j]=-h*(((j==0)||(j==n-1))?0.5:1)*
                    k.elements[i*k.m+j];
        res.elements[i*res.m+i]+=1; 
        
        res.elements[i*res.m+res.m-1]=f.elements[i];
    }
    return res;
}
VECTOR gauss(MATRIX matr){
    VECTOR index=gauss_direct(matr);
    VECTOR ys=gauss_reverse(matr);   
    return_order(&ys,index);
    return ys;

}

/*
Функция solve_eq решает интегральное уравнение Фредгольма второго рода, 
используя таблично-заданные 
ядро k_d и свободную составляющую f_d, с шагом h на интервале [a,b].
Возвращает вектор решения уравнения.
Параметры:
k - MATRIX - таблично-заданное ядро уравнения
f - VECTOR - таблично-заданная свободная функция
h - double - шаг поиска решения
a,b - double - интервал поиска решения
*/
VECTOR solve_eq(MATRIX k,VECTOR f,double h, double a,double b){
    MATRIX matr=create_sys(k,f,h,a,b);
    return gauss(matr);
}
PyObject* solve_eq_py(PyObject* self,PyObject *args){
    int i,j;
    double a,b,h;
    PyObject *k,*f;
    PyArg_ParseTuple(args,"dddOO",&a,&b,&h,&k,&f);
    MATRIX k_d;
    VECTOR f_d;
    int n=round((b-a)/h+1);
    if (n<=0)
        return NULL;
    VECTOR xs;
    xs.n=n;
    xs.elements=malloc(n*sizeof(double));
    xs.elements[0]=a;
    for (i=1;i<n;i++)
        xs.elements[i]=xs.elements[i-1]+h;
    f_d.n=n;k_d.n=n;k_d.m=n;
    f_d.elements=malloc(f_d.n*sizeof(double));
    k_d.elements=malloc(k_d.n*k_d.m*sizeof(double));
    PyObject* temp;
    for (i=0;i<n;++i){
        for (j=0;j<n;++j){
            PyObject* arg=Py_BuildValue("(dd)",xs.elements[i],xs.elements[j]);
            temp=PyObject_CallObject(k,arg);
            Py_XDECREF(arg);
            k_d.elements[i*k_d.m+j]=PyFloat_AsDouble(temp);
            Py_XDECREF(temp);
        }
        PyObject *arg=Py_BuildValue("(d)",xs.elements[i]);
        temp=PyObject_CallObject(f,arg);
        Py_XDECREF(arg);
        f_d.elements[i]=PyFloat_AsDouble(temp);
        Py_XDECREF(temp);
    }
    VECTOR ys=solve_eq(k_d,f_d,h,a,b);
    PyObject *py_xs=PyList_New(n),
             *py_ys=PyList_New(n);
    for (i=0;i<n;++i){
        PyList_SetItem(py_xs,i,PyFloat_FromDouble(xs.elements[i]));
        PyList_SetItem(py_ys,i,PyFloat_FromDouble(ys.elements[i]));
    }

    return Py_BuildValue("OO",py_xs,py_ys);
}

static PyMethodDef alg3methods[] = {
    {"solve_eq",  solve_eq_py, METH_VARARGS,""},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
static struct PyModuleDef alg3module = {
   PyModuleDef_HEAD_INIT,
   "alg3",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   alg3methods
};

PyMODINIT_FUNC
PyInit_alg3(void)
{
    return PyModule_Create(&alg3module);
}
