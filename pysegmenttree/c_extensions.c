
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include "_extensions/intsegmenttree.h"
#include "_extensions/floatsegmenttree.h"

static PyModuleDef c_extensions = {
    PyModuleDef_HEAD_INIT,           /* m_base */
    "pysegmenttree.c_extensions",    /* m_name */
    .m_doc = "Example module that creates an extension type.",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_c_extensions(void)
{
    PyObject* m;

    if (PyType_Ready(&intsegmenttree_type) < 0 || PyType_Ready(&floatsegmenttree_type) < 0)
        return NULL;

    m = PyModule_Create(&c_extensions);
    if (m == NULL)
        return NULL;

    Py_INCREF(&intsegmenttree_type);
    if (PyModule_AddObject(m, "IntSegmentTree", (PyObject*)&intsegmenttree_type) < 0)
    {
        Py_DECREF(&intsegmenttree_type);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&floatsegmenttree_type);
    if (PyModule_AddObject(m, "FloatSegmentTree", (PyObject*)&floatsegmenttree_type) < 0)
    {
        Py_DECREF(&floatsegmenttree_type);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
