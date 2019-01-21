#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen,PIPE
import StringIO
import re

def execute(command):
    """fork a subprocess to run shell command

    :param command: shell script to run
    :returns: return code, standout, standerr
    """
    r = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
    r.wait()
    out, err = r.communicate()
    stdo = StringIO.StringIO()
    stde = StringIO.StringIO()
    stdo.write(out)
    stdo.seek(0)
    stde.write(err)
    stde.seek(0)

    return r.returncode, stdo, stde

def get_manage():
    with open('/opt/falcon_em/webapps/ROOT/WEB-INF/conf/em.properties', 'rb') as f:
        c_t = f.read()

    return re.findall(r'mng.host\s*=\s*(.*)', c_t)[0].strip()
