
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include <string.h>
#include "structmember.h"
#include "common.h"

#if defined(_WIN32)
    #define __builtin_saddll_overflow saddll_overflow

    /*
        msvc doesn't have builtin intrinsic function for safe integer addition,
        thus we create our own.
    */
    inline bool saddll_overflow(long long a, long long b, long long *res) {
        unsigned long long buf = 0;

        if (a > 0 && b > 0) {
            buf = a + b;

            if (buf > LLONG_MAX) {
                return true;
            }
        } else if (a < 0 && b < 0) {
            buf = -a - b;

            if (buf > -LLONG_MIN) {
                return true;
            }
        }

        *res = a + b;
        return false;
    }
#endif

typedef struct {
    PyObject_HEAD
    Py_ssize_t size;
    long long *tree;
    enum QueryFunc func;
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
        self->tree = (long long*) malloc(sizeof(long long) * 2 * size);

        /* Fill in the elements from source */
        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject *item = PyList_GetItem(source, i);

            int overflow;
            long long val = PyLong_AsLongLongAndOverflow(item, &overflow);

            if (overflow != 0) {
                PyErr_SetString(PyExc_OverflowError, "Overflow while building the tree");
                return -1;
            }
            self->tree[size + i] = val;
        }

        for (Py_ssize_t i = size - 1; i > 0; i--) {
            long long left = self->tree[i << 1];
            long long right = self->tree[i << 1 | 1];

            long long res;

            switch(self->func) {
                case Sum:
                    if (__builtin_saddll_overflow(left, right, &res)) {
                        PyErr_SetString(PyExc_OverflowError, "Overflow while building the tree");
                        return -1;
                    }
                    break;
                case Min:
                    res = MIN(left, right);
                    break;
                case Max:
                    res = MAX(left, right);
                    break;
                default:
                    Py_UNREACHABLE();
                    return -1;
            }
            self->tree[i] = res;
        }
    }
    return 0;
}

static inline Py_ssize_t
intsegmenttree_mp_len(IntSegmentTreeObject *self)
{
    return self->size;
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

    left += self->size;
    right += self->size;
    long long res;

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

    PyObject *respy = PyLong_FromLongLong(res);
    return respy;
}


static PyObject *
intsegmenttree_update(IntSegmentTreeObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"i", "value", NULL};
    Py_ssize_t i;
    long long value;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "nL|", kwlist,
                                     &i, &value))
        return NULL;

    if (i > self->size - 1 || i < 0) {
        PyErr_SetString(PyExc_IndexError, "IntSegmentTree index out of range");
        return NULL;
    }

    Py_ssize_t parent, indx;
    long long left_child = 0, right_child = 0;

    indx = i + self->size;
    self->tree[indx] = value;
    parent = indx >> 1;

    while (parent > 0) {
        left_child = self->tree[parent << 1];
        right_child = self->tree[parent << 1 | 1];

        switch(self->func) {
            case Sum:
                if (__builtin_saddll_overflow(left_child, right_child, &self->tree[parent])) {
                    PyErr_SetString(PyExc_OverflowError, "Overflow while updating the tree");
                    return NULL;
                };
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


static PyMappingMethods intsegmenttree_mapping = {
    .mp_length = (lenfunc)intsegmenttree_mp_len,
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
    .tp_as_mapping = &intsegmenttree_mapping,
    .tp_methods = intsegmenttree_methods,
    .tp_init = (initproc)intsegmenttree_init,
    .tp_alloc = PyType_GenericAlloc,
    .tp_new = intsegmenttree_new,
};
