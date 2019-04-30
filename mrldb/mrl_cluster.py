__all__=["MrlDBCluster", "mdbcl"]

_cluster={"main": None}
class MrlDBCluster:
    def __init__(self):
        self.dbs={}
        self.aliases={}
        _cluster["main"]=self
    def get(self, name):
        return self.dbs[self.aliases[name]]
    def add(self, name, db, aliases=[]):
        self.dbs[name]=db
        self.aliases[name]=name
        for alias in aliases: self.aliases[alias]=name
        return name
    def addalias(self, name, aliases):
        if isinstance(aliases, str):
            self.aliases[aliases]=name
        else:
            for alias in aliases: self.aliases[alias]=name
        return name
    def get_cluster_infos(self):
        return {
        name: db._getinfos() for name, db in self.dbs.items()
        }
mdbcl=None
try:
    from werkzeug.local import LocalProxy
    mdbcl=LocalProxy(lambda: _cluster["main"])
except: pass
