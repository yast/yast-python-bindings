#include <unistd.h>
#include "Y2CCPythonClient.h"
#include <ycp/pathsearch.h>
#define y2log_component "Y2PythonClient"
#include <ycp/y2log.h>

// This is very important: We create one global variable of
// Y2CCPythonClient. Its constructor will register it automatically to
// the Y2ComponentBroker, so that will be able to find it.
// This all happens before main() is called!

Y2CCPythonClient g_y2ccpythonclient;

Y2Component *Y2CCPythonClient::provideNamespace (const char *name)
{
  // let someone else try creating the namespace, we just provide clients
  return 0;
}

Y2Component *Y2CCPythonClient::create ( const char * name) const
{
  y2debug("look for client with name %s", name);
  string sname(name);
  string client_path = YCPPathSearch::find (YCPPathSearch::Client, sname + ".py");
  //client not found in form clients/<name>.py
  if (client_path.empty())
  {
    // for paths it needs at least one slash BNC#330965#c10
    if(!strchr (name, '/'))
      return NULL;

    client_path = Y2PathSearch::completeFilename (sname);
    if (client_path.empty())
      return NULL;

    if (strlen(name) > 3 && strcmp(name + strlen(name) - 3, ".py")) //not python file
      return NULL;
  }

  y2debug("test existence of file %s", client_path.c_str());
  if (access(client_path.c_str(), R_OK) == -1) { //no file or no read permission
    y2error("%s does not exist!", client_path.c_str());
    return NULL;
  }

  Y2PythonClientComponent* rc = Y2PythonClientComponent::instance();
  rc->setClient(client_path);
  return rc;
}

