#include <Python.h>

static PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_abi3",
    "ABI3 support module",
    -1,
    NULL,
};

PyMODINIT_FUNC
PyInit__abi3(void)
{
    return PyModule_Create(&moduledef);
}
