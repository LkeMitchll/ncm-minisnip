""" An ncm source for vim-minisnip """
from os import listdir, path
from cm import register_source, Base, getLogger

register_source(
    name='vim-minisnip',
    abbreviation='minisnip',
    priority=9)

LOGGER = getLogger(__name__)

class Source(Base):
    """ The primary class: fetches, processes and returns snippets """

    def __init__(self, nvim):
        self.nvim = nvim
        self.minisnip_dir = nvim.eval('get(g:, "minisnip_dir")')
        self.snippets = listdir(path.expanduser(self.minisnip_dir))
        LOGGER.info('minisnip snippets: %s', self.snippets)

    def process_matches(self, filetypes):
        """ Process and return snippet names"""
        matches = []
        for filetype in filetypes:
            for snippet in self.snippets:
                if filetype in snippet:
                    matches.append(snippet.split(filetype)[1])
        LOGGER.info('minisnip matches: %s', matches)
        return matches

    def cm_refresh(self, info, ctx):
        """ Refresh NCM with matches """
        split_filetypes = ctx['filetype'].split('.')
        filetypes = ['_' + filetype + '_' for filetype in split_filetypes]
        self.complete(info, ctx, ctx['startcol'], self.process_matches(filetypes))
