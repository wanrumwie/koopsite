"""
Скопіював з файлів Джанго заголовки класів.

"""

Node = None         # фіктивно встановлено, щоб не світилися помилки
NodeList = None     # фіктивно встановлено, щоб не світилися помилки

class BlockNode(Node):
    def __init__(self, name, nodelist, parent=None):
        self.name, self.nodelist, self.parent = name, nodelist, parent

class ExtendsNode(Node):
    must_be_first = True

    def __init__(self, nodelist, parent_name, template_dirs=None):
        self.nodelist = nodelist
        self.parent_name = parent_name
        self.template_dirs = template_dirs
        self.blocks = {n.name: n for n in nodelist.get_nodes_by_type(BlockNode)}

class IncludeNode(Node):
    def __init__(self, template, *args, **kwargs):
        self.template = template
        self.extra_context = kwargs.pop('extra_context', {})
        self.isolated_context = kwargs.pop('isolated_context', False)
        super(IncludeNode, self).__init__(*args, **kwargs)

class TextNode(Node):
    def __init__(self, s):
        self.s = s

class VariableNode(Node):
    def __init__(self, filter_expression):
        self.filter_expression = filter_expression

class TagHelperNode(Node):
    """
    Base class for tag helper nodes such as SimpleNode, InclusionNode and
    AssignmentNode. Manages the positional and keyword arguments to be passed
    to the decorated function.
    """

    def __init__(self, takes_context, args, kwargs):
        self.takes_context = takes_context
        self.args = args
        self.kwargs = kwargs

class AutoEscapeControlNode(Node):
    """Implements the actions of the autoescape tag."""
    def __init__(self, setting, nodelist):
        self.setting, self.nodelist = setting, nodelist

class CommentNode(Node):
    def render(self, context):
        return ''

class CsrfTokenNode(Node):
    pass
class CycleNode(Node):
    def __init__(self, cyclevars, variable_name=None, silent=False):
        self.cyclevars = cyclevars
        self.variable_name = variable_name
        self.silent = silent

class DebugNode(Node):
    pass
class FilterNode(Node):
    def __init__(self, filter_expr, nodelist):
        self.filter_expr, self.nodelist = filter_expr, nodelist

class FirstOfNode(Node):
    def __init__(self, variables):
        self.vars = variables

class ForNode(Node):
    child_nodelists = ('nodelist_loop', 'nodelist_empty')

    def __init__(self, loopvars, sequence, is_reversed, nodelist_loop, nodelist_empty=None):
        self.loopvars, self.sequence = loopvars, sequence
        self.is_reversed = is_reversed
        self.nodelist_loop = nodelist_loop
        if nodelist_empty is None:
            self.nodelist_empty = NodeList()
        else:
            self.nodelist_empty = nodelist_empty

class IfChangedNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, nodelist_true, nodelist_false, *varlist):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self._varlist = varlist

class IfEqualNode(Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

class IfNode(Node):

    def __init__(self, conditions_nodelists):
        self.conditions_nodelists = conditions_nodelists

class LoremNode(Node):
    def __init__(self, count, method, common):
        self.count, self.method, self.common = count, method, common

class RegroupNode(Node):
    def __init__(self, target, expression, var_name):
        self.target, self.expression = target, expression
        self.var_name = var_name

class SsiNode(Node):
    def __init__(self, filepath, parsed):
        self.filepath = filepath
        self.parsed = parsed

class LoadNode(Node):
    def render(self, context):
        return ''

class NowNode(Node):
    def __init__(self, format_string, asvar=None):
        self.format_string = format_string
        self.asvar = asvar

class SpacelessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

class TemplateTagNode(Node):
    # mapping = {'openblock': BLOCK_TAG_START,
    #            'closeblock': BLOCK_TAG_END,
    #            'openvariable': VARIABLE_TAG_START,
    #            'closevariable': VARIABLE_TAG_END,
    #            'openbrace': SINGLE_BRACE_START,
    #            'closebrace': SINGLE_BRACE_END,
    #            'opencomment': COMMENT_TAG_START,
    #            'closecomment': COMMENT_TAG_END,
    #            }

    def __init__(self, tagtype):
        self.tagtype = tagtype

class URLNode(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

class VerbatimNode(Node):
    def __init__(self, content):
        self.content = content

class WidthRatioNode(Node):
    def __init__(self, val_expr, max_expr, max_width, asvar=None):
        self.val_expr = val_expr
        self.max_expr = max_expr
        self.max_width = max_width
        self.asvar = asvar

class WithNode(Node):
    def __init__(self, var, name, nodelist, extra_context=None):
        self.nodelist = nodelist
        # var and name are legacy attributes, being left in case they are used
        # by third-party subclasses of this Node.
        self.extra_context = extra_context or {}
        if name:
            self.extra_context[name] = var

