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

def get_word(piter):
    a = piter.copy()
    b = piter.copy()
    
    while True:
        if a.starts_line():
            break
        
        a.backward_char()
        ch = a.get_char()
        
        #if not (ch.isalnum() or ch in ['_', ':', '.', '-', '>']):
        if not (ch.isalnum() or ch in "_:.->"):
            a.forward_char()
            break
    
    word = a.get_visible_text(b)
    return a, word

def get_document(piter):
    a = piter.copy()
    b = piter.copy()
    
    while True:
        if not a.backward_char():
            break
    
    while True:
        if not b.forward_char():
            break
    
    return a.get_visible_text(b)

# ex:ts=4:et:
