#include <y2util/y2log.h>

void swig_y2debug(const char *file, const int line, const char *func, const char *msg);
void swig_y2milestone(const char *file, const int line, const char *func, const char *msg);
void swig_y2warning(const char *file, const int line, const char *func, const char *msg);
void swig_y2error(const char *file, const int line, const char *func, const char *msg);
void swig_y2security(const char *file, const int line, const char *func, const char *msg);
void swig_y2internal(const char *file, const int line, const char *func, const char *msg);

