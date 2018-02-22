# -*- coding: utf-8 -*-

from cm import register_source, Base, getLogger
import neovim
import os
register_source(name='vim-minisnip',
        abbreviation='minisnip',
        priority=9)

logger = getLogger(__name__)

class Source(Base):
    def __init__(self, nvim):
        self.nvim = nvim
        self.minisnip_dir = nvim.eval('get(g:, "minisnip_dir")')
        self.snippets = os.listdir(os.path.expanduser(self.minisnip_dir))

    def cm_refresh(self,info,ctx):
        filetypes = ctx['filetype'].split('.')
        filetype = ['_' + filetype + '_' for filetype in filetypes]
        cleaned = [snippet.split(filetype[0])[1] for snippet in self.snippets if filetype[0] in snippet]
        self.complete(info, ctx, ctx['startcol'], cleaned)
