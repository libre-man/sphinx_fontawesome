#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Module sphinx_fontawesome
"""

import os

import docutils.parsers.rst.directives as directives
import sphinx_fontawesome.constant
from docutils import nodes
from docutils.nodes import Text, emphasis, reference, strong
from docutils.parsers.rst import Directive
from docutils.parsers.rst.roles import set_classes
from sphinx import addnodes

__version_info__ = (0, 0, 6)
__version__ = '.'.join([str(val) for val in __version_info__])

sub_special = [
    {
        'id': 'o',
        'key': 'square-o'
    },
    {
        'id': 'x',
        'key': 'check-square-o'
    },
    {
        'id': 'smile',
        'key': 'smile-o'
    },
    {
        'id': 'mail',
        'key': 'envelope'
    },
    {
        'id': 'note',
        'key': 'info-circle'
    },
]


# add role
def fa_global(key=''):
    def fa(role, rawtext, text, lineno, inliner, options={}, content=[]):
        nodes = []
        if key:
            nodes.append(faicon(key, fa_name=key))
        else:
            for x in text.split(","):
                nodes.append(faicon(x, fa_name=x))
        return nodes, []

    return fa


class faicon(nodes.Element):
    pass


def visit_faicon_html(self, node):
    self.body.append('<em class="fa codegrade fa-{}">'.format(node['fa_name']))


def depart_faicon_html(self, node):
    self.body.append('</em>')


def visit_faicon_latex(self, node):
    self.body.append(r'\fa{}{{}}'.format(''.join(
        part.capitalize() for part in node['fa_name'].split('-'))))


def depart_faicon_latex(self, node):
    pass


#add directive
class Fa(Directive):
    has_content = True

    def run(self):
        nodes = []
        for x in self.content[0].split(' '):
            nodes.append(faicon(x, fa_name=x))
        return nodes


prolog = '\n'.join(['.. |%s| replace:: fa:: %s' % (icon, icon) for icon in sphinx_fontawesome.constant.icons])
prolog += '\n'
prolog += '\n'.join(['.. |%s| replace:: fa:: %s' % (icon['id'], icon['key']) for icon in sub_special])
prolog += '\n'


def setup(app):
    app.add_role('fa', fa_global())
    app.add_directive('fa', Fa)
    app.add_latex_package('fontawesome')
    app.add_node(
        faicon,
        html=(visit_faicon_html, depart_faicon_html),
        latex=(visit_faicon_latex, depart_faicon_latex))
    app.config.rst_prolog = prolog
    return {'version': __version__}
