%{
#include <y2util/y2log.h>

void swig_y2debug(const char *format)
{
    y2debug(format);
}

void swig_y2milestone(const char *format)
{
    y2milestone(format);
}

void swig_y2warning(const char *format)
{
    y2warning(format);
}

void swig_y2error(const char *format)
{
    y2error(format);
}

void swig_y2security(const char *format)
{
    y2security(format);
}

void swig_y2internal(const char *format)
{
    y2internal(format);
}
%}

%rename(y2debug) swig_y2debug;
%rename(y2milestone) swig_y2milestone;
%rename(y2warning) swig_y2warning;
%rename(y2error) swig_y2error;
%rename(y2security) swig_y2security;
%rename(y2internal) swig_y2internal;

%include "y2log.h"

