#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *
pysegmenttree_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyMethodDef PySegmenttreeMethods[] = {
    {"system",  pysegmenttree_system, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef pysegmenttree_module = {
    PyModuleDef_HEAD_INIT,
    "_pysegmenttree",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    PySegmenttreeMethods
};


PyMODINIT_FUNC
PyInit__pysegmenttree(void)
{
    return PyModule_Create(&pysegmenttree_module);
}
