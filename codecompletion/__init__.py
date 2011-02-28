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

import gedit
import jsonprovider

class JSONCompletionWindowHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        
        self._provider = jsonprovider.JSONProvider(plugin)
        
        # Add the provider to all the views
        for view in self._window.get_views():
            self.add_view(view)
        
        self._tab_added_id = self._window.connect('tab-added', self.on_tab_added)
        self._tab_removed_id = self._window.connect('tab-removed', self.on_tab_removed)
    
    def deactivate(self):
        # Remove the provider from all the views
        for view in self._window.get_views():
            view.get_completion().completion.remove_provider(self._provider)
        
        self._window.disconnect(self._tab_added_id)
        self._window.disconnect(self._tab_removed_id)
        
        self._window = None
        self._plugin = None
    
    def update_ui(self):
        pass
    
    def add_view(self, view):
        view.get_completion().add_provider(self._provider)
    
    def remove_view(self, view):
        view.get_completion().remove_provider(self._provider)
    
    def on_tab_added(self, window, tab):
        # Add provider to the new view
        self.add_view(tab.get_view())
    
    def on_tab_removed(self, window, tab):
        # Remove provider from the view
        self.remove_view(tab.get_view())

class JSONCompletionPlugin(gedit.Plugin):
    WINDOW_DATA_KEY = "JSONCompletionPluginWindowData"
    
    def __init__(self):
        gedit.Plugin.__init__(self)
    
    def activate(self, window):
        helper = JSONCompletionWindowHelper(self, window)
        window.set_data(self.WINDOW_DATA_KEY, helper)
    
    def deactivate(self, window):
        window.get_data(self.WINDOW_DATA_KEY).deactivate()
        window.set_data(self.WINDOW_DATA_KEY, None)
    
    def update_ui(self, window):
        window.get_data(self.WINDOW_DATA_KEY).update_ui()

# ex:ts=4:et:
