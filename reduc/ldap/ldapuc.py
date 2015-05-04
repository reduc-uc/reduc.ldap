#! /usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010. Jose Dinuncio
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License.
#
##############################################################################
import ldap
from  ldap import modlist
from filter import Eq

class Ldap:
    def __init__(self, uri, base_dn, root_dn='', root_pwd=''):
        self.uri = uri
        self.base_dn = base_dn
        self._root_dn = root_dn
        self._root_pwd = root_pwd
        self.initServer(self.uri)
        self.bind(self._root_dn, self._root_pwd)

    def initServer(self, uri, retry_max=2, retry_delay=10.0):
        self.server = ldap.ldapobject.ReconnectLDAPObject(uri,
                retry_max=retry_max, retry_delay=retry_delay)

    def bind(self, dn, pwd):
        self.server.simple_bind_s(dn, pwd)

    def login(self, uid, pwd):
        dn = self.find(Eq('uid', uid)).dn
        self.bind(dn, pwd)

    def auth(self, uid, pwd):
        try:
            self.login(uid, pwd)
            auth = True
        except ldap.INVALID_CREDENTIALS:
            auth = False
        except AttributeError:
            # dn not found
            auth = False
        finally:
            self.bind(self._root_dn, self._root_pwd)
        return auth

    def add(self, entry):
        modlist = ldap.modlist.addModlist(entry)
        return self.server.add_s(entry.dn, modlist)

    def delete(self, entry):
        return self.server.delete_s(entry.dn)

    def modify(self, oldEntry, newEntry):
        if oldEntry.dn <> newEntry.dn:
            self.server.rename_s(oldEntry.dn, newEntry.dn)
            # TODO: Manejar renombre
            #self.delete(old_entry)
            #return self.new(new_entry)
        else:
            modlist = ldap.modlist.modifyModlist(oldEntry, newEntry)
            # Convertimos unicode a string
            modlist = [(x[0], x[1], None if x[2] is None else str(x[2]))
                            for x in modlist]
            return self.server.modify_s(newEntry.dn, modlist)

    def search(self, filter, base_dn=None):
        filter = str(filter)
        base_dn = base_dn or self.base_dn

        msgid = self.server.search(base_dn, ldap.SCOPE_SUBTREE, filter)
        while True:
            _type, data = self.server.result(msgid, all=0)
            if not data:
                return
            dn, dct = data[0]
            yield Entry(dn, **dct)

    def find(self, filter):
        try:
            return self.search(filter).next()
        except StopIteration:
            return Entry()


class Entry(dict):
    '''
    Entry es un diccionario que representa una entrada LDAP. Almacena el dn
    de donde proviene y tiene metodos de acceso de conveniencia para acceder a
    sus propiedades (las cuales suelen ser listas con un único valor).
    '''
    def __init__(self, dn='', **dct):
        dict.__init__(self, **dct)
        self.dn = dn

    def clone(self):
        '''Devuelve un clone de si mismo'''
        return Entry(self.dn, **self)

    """
    def update(self, entry, **kargs):
        '''Actualiza esta entrada basado en entry y kargs'''
        self.dn = entry.dn
        dict.update(self, entry, **kargs)
    """

    def first(self, key, default=None):
        '''Devuelve el primer elemento de self[key]'''
        if default is None:
            v = self[key]
        else:
            v = self.get(key, default)

        if type(v) == list:
            return v[0]
        else:
            return v


