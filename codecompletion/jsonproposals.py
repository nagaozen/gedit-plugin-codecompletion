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

import gtksourceview2 as gsv
import gobject

class JSONProposal(gobject.GObject, gsv.CompletionProposal):
    def __init__(self, name):
        gobject.GObject.__init__(self)
        
        self.name = name
    
    def do_get_text(self):
        return self.name
    
    def do_get_label(self):
        return self.name
    
    def do_get_info(self):
        # FIXME: gettext
        return 'No extra info available'

gobject.type_register(JSONProposal)

# ex:ts=4:et:
