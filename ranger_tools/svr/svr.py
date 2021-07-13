from ..dataclass import *

GraphPoint = DataClass('GraphPoint', [
    ('classname', Constant(wstr_, 'TGraphPoint')),
    ('pos', Point),
    ('text', wstr_),
    ('_minus1', Constant(int_, -1)),
])

GraphLink = DataClass('GraphLink', [
    ('classname', Constant(wstr_, 'TGraphLink')),
    ('begin', int_),
    ('end', int_),
    ('ord_num', uint_),
    ('has_arrow', bool_),
])

GraphRect = DataClass('GraphRect', [
    ('classname', Constant(wstr_, 'TGraphRectText')),
    ('rect', Rect),
    ('fill_style', byte_),
    ('fill_color', uint_),
    ('border_style', byte_),
    ('border_color', uint_),
    ('border_size', uint_),
    ('border_coef', float_),
    ('text_align_x', uint_),
    ('text_align_y', uint_),
    ('text_align_rect', bool_),
    ('text', wstr_),
    ('text_color', uint_),
    ('font', wstr_),
    ('font_size', uint_),
    ('is_bold', bool_),
    ('is_italic', bool_),
    ('is_underline', bool_),
])

Star = DataClass('Star', [
    # ('classname', Constant(wstr_, 'TStar')),
    # ('pos', Point),
    # ('text', wstr_),
    # ('_minus1', Constant(int_, -1)),

    ('constellation', uint_),
    ('priority', uint_),
    ('is_subspace', bool_),
    ('no_kling', bool_),
    ('no_come_kling', bool_),
])

Planet = DataClass('Planet', [
    ('',),
    ('',),
    ('',),
    ('',),
    ('',),
    ('',),
])

SVR = DataClass('SVR', [
    ('55443322', Constant(bytes_(4), b'\x55\x44\x33\x22')),
    ('version', uint_),
    ('viepos', Point),
    ('name', wstr_),
    ('filename', wstr_),
    ('textfilenames', List(wstr_)),
    ('translations', List(wstr_)),

    ('graphpoints', List(GraphPoint)),
    ('graphlinks', List(GraphLink)),
    ('graphrects', List(GraphRect)),
])
