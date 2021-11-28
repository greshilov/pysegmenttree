#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

/* Py_UNREACHABLE was introduced only in 3.7 */
#if !defined Py_UNREACHABLE
#define Py_UNREACHABLE() Py_FatalError("Unreachable C code path reached")
#endif

enum QueryFunc {
    Sum = 1,
    Min,
    Max,
};
