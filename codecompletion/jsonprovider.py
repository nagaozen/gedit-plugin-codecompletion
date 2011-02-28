# -*- coding: utf-8 -*-

# gEdit CodeCompletion plugin
# Copyright (C) 2011 Fabio Zendhi Nagao
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import gedit

from gettext import gettext as _

import gobject
import gtksourceview2 as gsv
import json

from jsonproposals import JSONProposal

import re
import os
import utils

class JSONProvider(gobject.GObject, gsv.CompletionProvider):
    MARK_NAME = 'JSONProviderCompletionMark'
    
    def __init__(self, plugin):
        gobject.GObject.__init__(self)
        
        self.mark = None
        self._plugin = plugin
        
        self._libs = {}
        self._libs['global'] = self.get_language_library('global')
    
    def move_mark(self, buf, start):
        # TODO: see do_get_mark_iter
        mark = buf.get_mark(self.MARK_NAME)
        
        if not mark:
            buf.create_mark(self.MARK_NAME, start, True)
        else:
            buf.move_mark(mark, start)
    
    def get_proposals(self, code, lang, word):
        proposals = []
        
        # Get global static proposals
        for proposal in self.get_filtered_proposals(self._libs['global']['statics'].split(' '), word):
            proposals.append(JSONProposal(proposal))
        
        if lang:
            lib = self.get_language_library(lang.get_id())
            
            # Get language static proposals
            if 'statics' in lib:
                for proposal in self.get_filtered_proposals(lib['statics'].split(' '), word):
                    proposals.append(JSONProposal(proposal))
            
            # Get language dynamic proposals
            if 'dynamic' in lib:
                if 'identificators' in lib['dynamic']:
                    identificators = lib['dynamic']['identificators']
                    for identificator in identificators:
                        re_identificator = re.compile(r'%s'%identificator, re.UNICODE)
                        for m in re_identificator.finditer(code):
                            tokens = lib["dynamic"]["members"].get(m.group("class"))
                            if tokens:
                                tokens = tokens.split(' ')
                                tokens = [ "%s%s%s" % (m.group("instance"), lib["dynamic"]["tokenSeparator"], token) for token in tokens ]
                                tokens = self.get_filtered_proposals(tokens, word)
                                
                                proposals.extend([ JSONProposal(token) for token in tokens ])
        return proposals
    
    def do_get_start_iter(self, context, proposal):
        buf = context.get_iter().get_buffer()
        mark = buf.get_mark(self.MARK_NAME)
        
        if not mark:
            return None
        
        return buf.get_iter_at_mark(mark)
    
    def do_populate(self, context):
        start, word = utils.get_word(context.get_iter())
        if not word:
            context.add_proposals(self, [], True)
            return
        
        self.move_mark(context.get_iter().get_buffer(), start)
        
        code = utils.get_document(start)
        lang = start.get_buffer().get_language()
        
        proposals = self.get_proposals(code, lang, word)
        context.add_proposals(self, proposals, True)
    
    def do_get_name(self):
        return _('CodeCompletion Library')
    
    def get_priority(self):
        return 42
    
    def do_get_activation(self):
        return gsv.COMPLETION_ACTIVATION_INTERACTIVE | gsv.COMPLETION_ACTIVATION_USER_REQUESTED
    
    def do_activate_proposal(self, proposal, piter):
        # TODO: implement
        return False
    
    def get_language_library(self, lang):
        if lang in self._libs:
            return self._libs[lang]
        else:
            path = os.path.join( self._plugin.get_install_dir(), 'codecompletion', 'lib', "%s.json"%(lang) )
            
            if not os.path.isfile(path):
                return { "statics": "", "dynamic": {} }
            
            f = open(path, "rb")
            d = json.load(f)
            f.close()
            
            self._libs[lang] = d
            return d
    
    def get_filtered_proposals(self, words, prefix):
        proposals = [word for word in words if word.startswith(prefix) and word != prefix]
        return proposals

gobject.type_register(JSONProvider)

# ex:ts=4:et:
