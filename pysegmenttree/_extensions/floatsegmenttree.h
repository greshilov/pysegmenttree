
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    Py_ssize_t size;
    double *tree;
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
            self->tree[i] = left + right;
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

    double res = 0;
    left += self->size;
    right += self->size;

    while (left < right) {
        if (left & 1) {
            res += self->tree[left];
            left++;
        }

        if (right & 1) {
            --right;
            res += self->tree[right];
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

        self->tree[parent] = left_child + right_child;
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
