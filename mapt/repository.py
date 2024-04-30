import os
import sys
import logging
import re
import json

import apt_pkg
import apt.progress
import functools

logger = logging.getLogger(__name__)


class Repository:
    class __Progress(apt.progress.base.AcquireProgress):
        '''
            Logging of network activity for RepoSuite.updateCache()
        '''
        logger = logging.getLogger(__name__)
        def start():
            logger.debug("[start]")
        def stop():
            logger.debug("[stop]")
        def fetch(i):
            logger.debug("[fetch {}]".format(i.description))
        def fail(i):
            logger.debug("[fail {}]".format(i.description))
        def done(i):
            logger.debug("[done {}]".format(i.description))
        def ims_hit(i):
            logger.debug("[hit {}]".format(i.description))
        def pulse(owner):
            #for item in owner.items:
                #print(item)
                #if item.complete==1:
            #    print(item.desc_uri)
            #print("############################################")
            return True 
    def __init__(self,basedir,suite):
        #print("Basedir="+basedir)
        
        
        parts=suite["url"].split("/")
        for part in parts:
            if part.strip()=="":
                continue
            name=part
        suite["name"]=name+":"+suite["distribution"]
        suite["basedir"]=basedir+"/"+suite["name"]
        
        
        path=suite["basedir"]+"/etc/apt/"
        os.makedirs(path, exist_ok=True)
  
        
        #path="/root/"
        #f = open(path+"apt.conf", "w")
        #f.write('Dir "/root/.cache/apt-repos";')
        #f.close()
        
        
        
        path=suite["basedir"]+"/etc/apt/"
        os.makedirs(path, exist_ok=True)
        
        f = open(path+"apt.conf", "w")
        f.write('APT { Architectures { "'+'"; "'.join(suite['arch'])+'"; }; };')
        f.close()
    
    
        f = open(path+"sources.list", "w")
        f.write('deb [trusted=yes] '+suite["url"]+" "+suite['distribution']+" "+" ".join(suite["components"]))
    
        if suite["sources"]:
            f.write('\ndeb-src [trusted=yes] '+suite["url"]+" "+suite['distribution']+" "+" ".join(suite["components"])+"\n")
        f.close()
    
        path=suite["basedir"]+"/var/lib/dpkg/"
        os.makedirs(path, exist_ok=True)
        #print(path)
         
        f = open(path+"/status", "w")
        f.write("")
        f.close()
    
        path=suite["basedir"]+"/var/lib/apt/lists/partial/"
        os.makedirs(path, exist_ok=True)
        #print(path)
        
        path=suite["basedir"]+"/var/cache/apt/archives/partial"
        os.makedirs(path, exist_ok=True)
        #print(path)
        
        self.suite=suite
    def scan(self,pkgname):
        #print(pkgname)
        d=[]
        suite=self.suite
        apt_pkg.read_config_file(apt_pkg.config, suite["basedir"]+"/etc/apt/apt.conf")  
        apt_pkg.config.set("Dir", suite["basedir"])
        apt_pkg.config.set("Dir::State::status", suite["basedir"] + "/var/lib/dpkg/status")
        apt_pkg.init_system()
        cache=apt_pkg.Cache()
        src = apt_pkg.SourceList()
        src.read_main_list()
        for s in src.list:
           print(s.type,s.uri,s.dist,s.is_trusted)
        cache.update(self.__Progress, src)
        cache=apt_pkg.Cache()
        
        records = apt_pkg.PackageRecords(cache)
        req=pkgname
        requestArchs={}
        requestComponents={}
        isRE=False
        count=0
        for pkg in cache.packages:
            count=count+1
            #print(count)
            #print(pkg.name)
            for v in pkg.version_list:
                #sprint("   "+v.ver_str)
                   
                #print(v.file_list[0])
                
                records.lookup(v.file_list[0])
                source = records.source_pkg
                #records.record  complete data as text string
                #print(records.filename)
                
                if source == "":
                    # last directory part of the deb-filename is the source name
                    s = os.path.basename(os.path.dirname(records.filename))
                    if pkg.name == s:
                        source = pkg.name
                #print(pkg.name,v.ver_str,source,v.arch)
                if isRE:
                    m = re.search(req, pkg.name)
                    if not m:
                        m = re.search(req, "src:" + source)
                        if not m:
                            continue
                else:
                    if not (pkg.name == req or ("src:" + source) == req):
                        continue
                        
                if (requestArchs) and (not v.arch in requestArchs):
                    continue
                    
                parts = v.section.split("/", 1)
                if len(parts) == 1:
                    component, unused_section = "main", parts[0]
                else:
                    component, unused_section = parts
                            
                if (requestComponents) and (not component in requestComponents):
                    continues
                
                #rpackage["found"]=1
                #print(pkg.name,v.ver_str,v.arch,source,suite["name"])
                d.append([pkg.name, v.ver_str,suite["name"],v.arch])
                
        #print(count)
        return d
