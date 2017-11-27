%{
#include <y2util/y2log.h>

void swig_y2debug(const char *file, const int line, const char *func, const char *msg)
{
    y2_logger(LOG_DEBUG, "Python", file, line, func, msg);
}

void swig_y2milestone(const char *file, const int line, const char *func, const char *msg)
{
    y2_logger(LOG_MILESTONE, "Python", file, line, func, msg);
}

void swig_y2warning(const char *file, const int line, const char *func, const char *msg)
{
    y2_logger(LOG_WARNING, "Python", file, line, func, msg);
}

void swig_y2error(const char *file, const int line, const char *func, const char *msg)
{
    y2_logger(LOG_ERROR, "Python", file, line, func, msg);
}

void swig_y2security(const char *file, const int line, const char *func, const char *msg)
{
    y2_logger(LOG_SECURITY, "Python", file, line, func, msg);
}

void swig_y2internal(const char *file, const int line, const char *func, const char *msg)
{
    y2_logger(LOG_INTERNAL, "Python", file, line, func, msg);
}
%}

%rename(y2debug) swig_y2debug;
%rename(y2milestone) swig_y2milestone;
%rename(y2warning) swig_y2warning;
%rename(y2error) swig_y2error;
%rename(y2security) swig_y2security;
%rename(y2internal) swig_y2internal;

%include "y2log.h"

