#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


Enum = type('Enum', (tuple, ), {
    '__init__': lambda s, i: [
        setattr(s, k, 1 << x)
        for x, k in enumerate(i)
    ] and tuple.__init__(s, i),
})
