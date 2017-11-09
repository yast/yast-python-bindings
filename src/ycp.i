%ignore YCPValueRep;
%rename(Value) YCPValue;
%include <ycp/YCPValue.h>
%extend YCPValue {
    const char * valuetype_str() {
        return (*($self))->valuetype_str();
    }
    bool isVoid() {
        return (*($self))->isVoid();
    }
    bool isBoolean() {
        return (*($self))->isBoolean();
    }
    bool isInteger() {
        return (*($self))->isInteger();
    }
    bool isFloat() {
        return (*($self))->isFloat();
    }
    bool isString() {
        return (*($self))->isString();
    }
    bool isByteblock() {
        return (*($self))->isByteblock();
    }
    bool isPath() {
        return (*($self))->isPath();
    }
    bool isSymbol() {
        return (*($self))->isSymbol();
    }
    bool isList() {
        return (*($self))->isList();
    }
    bool isTerm() {
        return (*($self))->isTerm();
    }
    bool isMap() {
        return (*($self))->isMap();
    }
    bool isCode() {
        return (*($self))->isCode();
    }
    bool isBreak() {
        return (*($self))->isBreak();
    }
    bool isReturn() {
        return (*($self))->isReturn();
    }
    bool isEntry() {
        return (*($self))->isEntry();
    }
    bool isReference() {
        return (*($self))->isReference();
    }
    YCPVoid asVoid() {
        return (*($self))->asVoid();
    }
    YCPBoolean asBoolean() {
        return (*($self))->asBoolean();
    }
    YCPInteger asInteger() {
        return (*($self))->asInteger();
    }
    YCPFloat asFloat() {
        return (*($self))->asFloat();
    }
    YCPString asString() {
        return (*($self))->asString();
    }
    YCPByteblock asByteblock() {
        return (*($self))->asByteblock();
    }
    YCPPath asPath() {
        return (*($self))->asPath();
    }
    YCPSymbol asSymbol() {
        return (*($self))->asSymbol();
    }
    YCPList asList() {
        return (*($self))->asList();
    }
    YCPTerm asTerm() {
        return (*($self))->asTerm();
    }
    YCPMap asMap() {
        return (*($self))->asMap();
    }
    YCPCode asCode() {
        return (*($self))->asCode();
    }
    YCPEntry asEntry() {
        return (*($self))->asEntry();
    }
    YCPReference asReference() {
        return (*($self))->asReference();
    }
    bool equal (const YCPValue&v) {
        return (*($self))->equal(v);
    }
    YCPOrder compare(const YCPValue &v, bool rl = false) {
        return (*($self))->compare(v, rl);
    }
}

%ignore YCPTermRep;
%rename(Term) YCPTerm;
%include <ycp/YCPTerm.h>
%extend YCPTerm {
    YCPOrder compare(const YCPTerm &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%ignore YCPListRep;
%rename(List) YCPList;
%include <ycp/YCPList.h>
%extend YCPList {
    YCPOrder compare(const YCPList &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%feature("valuewrapper") YCPString;
class YCPString;
%ignore YCPStringRep;
%rename(String) YCPString;
%include <ycp/YCPString.h>
%extend YCPString {
    bool isAscii() {
        return (*($self))->isAscii();
    }
    const string& value() {
        return (*($self))->value();
    }
    wstring wvalue() {
        return (*($self))->wvalue();
    }
    YCPOrder compare(const YCPString &v, bool rl = false) {
        return (*($self))->compare(v, rl);
    }
    const char *value_cstr() {
        return (*($self))->value_cstr();
    }
    string toString() {
        return (*($self))->toString();
    }
}

%ignore YCPSymbolRep;
%rename(Symbol) YCPSymbol;
%include <ycp/YCPSymbol.h>
%extend YCPSymbol {
    string symbol() {
        return (*($self))->symbol();
    }
    const char *symbol_cstr() {
        return (*($self))->symbol_cstr();
    }
    YCPOrder compare(const YCPSymbol &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%feature("valuewrapper") YCPInteger;
class YCPInteger;
%ignore YCPIntegerRep;
%rename(Integer) YCPInteger;
%include <ycp/YCPInteger.h>
%extend YCPInteger {
    long long value() {
        return (*($self))->value();
    }
    YCPOrder compare(const YCPInteger &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%feature("valuewrapper") YCPBoolean;
class YCPBoolean;
%ignore YCPBooleanRep;
%rename(Boolean) YCPBoolean;
%include <ycp/YCPBoolean.h>
%extend YCPBoolean {
    bool value() {
        return (*($self))->value();
    }
    YCPOrder compare(const YCPBoolean &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%ignore YCPFloatRep;
%rename(Float) YCPFloat;
%include <ycp/YCPFloat.h>
%extend YCPFloat {
    double value() {
        return (*($self))->value();
    }
    YCPOrder compare(const YCPFloat &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%ignore YCPMapRep;
%ignore YCPMapIterator;
%rename(Map) YCPMap;
%include "YCPMap.h"
%extend YCPMap {
    YCPOrder compare(const YCPMap &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%ignore YCPBreakRep;
%ignore YCPBreak;
%ignore YCPReturnRep;
%ignore YCPReturn;
%ignore YCPReferenceRep;
%ignore YCPReference;
%ignore YCPEntryRep;
%ignore YCPEntry;
%ignore YCPCodeRep;
%rename(Code) YCPCode;
%include <ycp/YCPCode.h>
%extend YCPCode {
    YCodePtr code() {
        return (*($self))->code();
    }
    YCPOrder compare (const YCPCode &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
    YCPValue evaluate (bool cse = false) {
        return (*($self))->evaluate(cse);
    }
}

%ignore YCPByteblockRep;
%rename(Byteblock) YCPByteblock;
%include <ycp/YCPByteblock.h>
%extend YCPByteblock {
    const unsigned char *value() {
        return (*($self))->value();
    }
    long size() {
        return (*($self))->size();
    }
    string toString() {
        return (*($self))->toString();
    }
    YCPOrder compare(const YCPByteblock& s) {
        return (*($self))->compare(s);
    }
}

%ignore YCPPathRep;
%rename(Path) YCPPath;
%include <ycp/YCPPath.h>
%extend YCPPath {
    bool isRoot() {
        return (*($self))->isRoot();
    }
    YCPValue select(const YCPValue& val) {
        return (*($self))->select(val);
    }
    void append(const YCPPath&p) {
        return (*($self))->append(p);
    }
    void append(string c) {
        return (*($self))->append(c);
    }
    long length() {
        return (*($self))->length();
    }
    bool isPrefixOf(const YCPPath& p) {
        return (*($self))->isPrefixOf(p);
    }
    YCPPath at(long index) {
        return (*($self))->at(index);
    }
    YCPPath prefix(long index) {
        return (*($self))->prefix(index);
    }
    string component_str(long index) {
        return (*($self))->component_str(index);
    }
    YCPOrder compare(const YCPPath &v) {
        return (*($self))->compare(v);
    }
    string toString() {
        return (*($self))->toString();
    }
}

%ignore YCPVoidRep;
%rename(Void) YCPVoid;
%include <ycp/YCPVoid.h>

