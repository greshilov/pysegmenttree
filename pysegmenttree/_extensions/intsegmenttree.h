
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    Py_ssize_t size;
    long *tree;
} IntSegmentTreeObject;

static void
intsegmenttree_dealloc(IntSegmentTreeObject* self) 
{
    free(self->tree);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
intsegmenttree_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    IntSegmentTreeObject *self;

    self = (IntSegmentTreeObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->size = 0;
    }

    return (PyObject *)self;
}

static int
intsegmenttree_init(IntSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"source", NULL};
    PyObject *source = NULL;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist,
                                     &source))
        return -1;

    if (source) {
        Py_ssize_t size = PyList_Size(source);
        self->size = size;
        self->tree = (long*) malloc(sizeof(long) * 2 * size);

        /* Fill in the elements from source */
        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject *item = PyList_GetItem(source, i);

            int overflow;
            long val = PyLong_AsLongAndOverflow(item, &overflow);

            if (overflow != 0) {
                PyErr_SetString(PyExc_OverflowError, "Overflow while building the tree");
                return -1;
            }
            self->tree[size + i] = val;
        }

        for (Py_ssize_t i = size - 1; i > 0; i--) {
            long left = self->tree[i << 1];
            long right = self->tree[i << 1 | 1];

            long res;
            if (__builtin_saddl_overflow(left, right, &res)) {
                PyErr_SetString(PyExc_OverflowError, "Overflow while building the tree");
                return -1;
            }
            self->tree[i] = res;
        }
    }
    return 0;
}

static PyObject *
intsegmenttree_query(IntSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"start", "end", NULL};
    Py_ssize_t left, right;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "nn|", kwlist,
                                     &left, &right))
        return NULL;

    if (left >= right || left < 0) {
        Py_RETURN_NONE;
    }
    
    long res = 0;
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

    PyObject *respy = PyLong_FromLong(res);
    return respy;
}


static PyObject *
intsegmenttree_update(IntSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"i", "value", NULL};
    Py_ssize_t i;
    long value;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "nl|", kwlist,
                                     &i, &value))
        return NULL;
    
    if (i > self->size - 1 || i < 0) {
        PyErr_SetString(PyExc_IndexError, "IntSegmentTree index out of range");
        return NULL;
    }

    Py_ssize_t parent, indx;
    long left_child = 0, right_child = 0;

    indx = i + self->size;
    self->tree[indx] = value;
    parent = indx >> 1;

    while (parent > 0) {
        left_child = self->tree[parent << 1];
        right_child = self->tree[parent << 1 | 1];

        if (__builtin_saddl_overflow(left_child, right_child, &self->tree[parent])) {
            PyErr_SetString(PyExc_OverflowError, "Overflow while updating the tree");
            return NULL;
        }
        parent >>= 1;
    }

    Py_RETURN_NONE;
}

static PyMemberDef intsegmenttree_members[] = {
    {"size", T_INT, offsetof(IntSegmentTreeObject, size), 0,
     "Size of the tree"},
    {NULL},  /* Sentinel */
};

static PyMethodDef intsegmenttree_methods[] = {
    {"query", (PyCFunction) intsegmenttree_query, METH_VARARGS | METH_KEYWORDS,
    "Performs the query operation"},
    {"update", (PyCFunction) intsegmenttree_update, METH_VARARGS | METH_KEYWORDS,
    "Performs the update operation"},
    {NULL},  /* Sentinel */
};

static PyTypeObject intsegmenttree_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pysegmenttree.c_extensions.IntSegmentTree",
    sizeof(IntSegmentTreeObject),
    .tp_dealloc = (destructor)intsegmenttree_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "IntSegmentTree",
    .tp_methods = intsegmenttree_methods,
    .tp_members = intsegmenttree_members,
    .tp_init = (initproc)intsegmenttree_init,
    .tp_alloc = PyType_GenericAlloc,
    .tp_new = intsegmenttree_new,
};
