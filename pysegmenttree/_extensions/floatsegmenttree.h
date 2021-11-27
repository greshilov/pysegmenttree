
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    Py_ssize_t size;
    double *tree;
    enum QueryFunc func;
} FloatSegmentTreeObject;

static void
floatsegmenttree_dealloc(FloatSegmentTreeObject* self)
{
    free(self->tree);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
floatsegmenttree_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    FloatSegmentTreeObject *self;

    self = (FloatSegmentTreeObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->size = 0;
    }

    return (PyObject *)self;
}

static int
floatsegmenttree_init(FloatSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"source", "func", NULL};
    PyObject *source = NULL;
    char* func = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|s", kwlist,
                                     &source, &func))
        return -1;

    if (func != NULL) {
        if (strcmp(func, "sum") == 0) {
            self->func = Sum;
        } else if (strcmp(func, "min") == 0) {
            self->func = Min;
        } else if (strcmp(func, "max") == 0) {
            self->func = Max;
        } else {
            PyErr_SetString(PyExc_ValueError, "Invalid 'func' argument, must be 'sum', 'min' or 'max'");
            return -1;
        }
    } else {
        self->func = Sum;
    }

    if (source) {
        Py_ssize_t size = PyList_Size(source);
        self->size = size;
        self->tree = (double*) malloc(sizeof(double) * 2 * size);

        /* Fill in the elements from source */
        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject *item = PyList_GetItem(source, i);
            double val = PyFloat_AsDouble(item);
            self->tree[size + i] = val;
        }

        for (Py_ssize_t i = size - 1; i > 0; i--) {
            double left = self->tree[i << 1];
            double right = self->tree[i << 1 | 1];

            switch(self->func) {
                case Sum:
                    self->tree[i] = left + right;
                    break;
                case Min:
                    self->tree[i] = MIN(left, right);
                    break;
                case Max:
                    self->tree[i] = MAX(left, right);
                    break;
                default:
                    Py_UNREACHABLE();
                    return -1;
            }
        }
    }
    return 0;
}

static inline Py_ssize_t
floatsegmenttree_mp_len(FloatSegmentTreeObject *self)
{
    return self->size;
}

static PyObject *
floatsegmenttree_query(FloatSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"start", "end", NULL};
    Py_ssize_t left, right;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "nn|", kwlist,
                                     &left, &right))
        return NULL;

    if (left >= right || left < 0) {
        Py_RETURN_NONE;
    }

    left += self->size;
    right += self->size;
    double res;

    switch(self->func) {
        case Sum:
            res = 0;
            break;
        case Min:
        case Max:
            res = self->tree[left];
            break;
        default:
            Py_UNREACHABLE();
            return NULL;
    }

    while (left < right) {
        if (left & 1) {
            switch(self->func) {
                case Sum:
                    res += self->tree[left];
                    break;
                case Min:
                    res = MIN(self->tree[left], res);
                    break;
                case Max:
                    res = MAX(self->tree[left], res);
                    break;
                default:
                    Py_UNREACHABLE();
                    return NULL;
            }

            left++;
        }

        if (right & 1) {
            --right;

            switch(self->func) {
                case Sum:
                    res += self->tree[right];
                    break;
                case Min:
                    res = MIN(res, self->tree[right]);
                    break;
                case Max:
                    res = MAX(res, self->tree[right]);
                    break;
                default:
                    Py_UNREACHABLE();
                    return NULL;
            }
        }

        left >>= 1;
        right >>= 1;
    }

    PyObject *respy = PyFloat_FromDouble(res);
    return respy;
}


static PyObject *
floatsegmenttree_update(FloatSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"i", "value", NULL};
    Py_ssize_t i;
    double value;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "nd|", kwlist,
                                     &i, &value))
        return NULL;

    if (i > self->size - 1 || i < 0) {
        PyErr_SetString(PyExc_IndexError, "FloatSegmentTree index out of range");
        return NULL;
    }

    Py_ssize_t parent, indx;
    double left_child = 0, right_child = 0;

    indx = i + self->size;
    self->tree[indx] = value;
    parent = indx >> 1;

    while (parent > 0) {
        left_child = self->tree[parent << 1];
        right_child = self->tree[parent << 1 | 1];

        switch(self->func) {
            case Sum:
                self->tree[parent] = left_child + right_child;
                break;
            case Min:
                self->tree[parent] = MIN(left_child, right_child);
                break;
            case Max:
                self->tree[parent] = MAX(left_child, right_child);
                break;
            default:
                Py_UNREACHABLE();
                return NULL;
        }
        parent >>= 1;
    }

    Py_RETURN_NONE;
}

static PyMappingMethods floatsegmenttree_mapping = {
    .mp_length = (lenfunc)floatsegmenttree_mp_len,
};

static PyMethodDef floatsegmenttree_methods[] = {
    {"query", (PyCFunction) floatsegmenttree_query, METH_VARARGS | METH_KEYWORDS,
    "Performs the query operation"},
    {"update", (PyCFunction) floatsegmenttree_update, METH_VARARGS | METH_KEYWORDS,
    "Performs the update operation"},
    {NULL},  /* Sentinel */
};

static PyTypeObject floatsegmenttree_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pysegmenttree.c_extensions.FloatSegmentTree",
    sizeof(FloatSegmentTreeObject),
    .tp_dealloc = (destructor)floatsegmenttree_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "FloatSegmentTree",
    .tp_as_mapping = &floatsegmenttree_mapping,
    .tp_methods = floatsegmenttree_methods,
    .tp_init = (initproc)floatsegmenttree_init,
    .tp_alloc = PyType_GenericAlloc,
    .tp_new = floatsegmenttree_new,
};
