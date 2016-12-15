#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import datetime
import operator
from decimal import Decimal
from functools import partial
from sql import Literal, Union, Column
from sql.aggregate import Sum
from sql.conditionals import Coalesce
from sql.operators import Concat

from trytond.model import Workflow, Model, ModelView, ModelSQL, fields
from trytond import backend
from trytond.pyson import In, Eval, Not, Equal, If, Bool
from trytond.tools import reduce_ids
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta

__all__ = ['Move']
__metaclass__ = PoolMeta

class Move():
    "Stock Move"
    __name__ = 'stock.move'
    estado = fields.Function(fields.Char('Estado',
            readonly=True), 'get_estado')

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()


    @classmethod
    def get_estado(cls, moves, names):
        pool = Pool()
        Location = pool.get('stock.location')

        result = {n: {m.id: Decimal(0) for m in moves} for n in names}
        for name in names:
            for move in moves:
                if move.to_location.type == 'customer':
                    result[name][move.id] = 'Salida'
                else:
                    result[name][move.id] = 'Entrada'
        return result
