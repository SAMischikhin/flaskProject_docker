from typing import Union, Dict, List, TextIO

from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

reg_pattern = r'^(.*_REG_EX_\s{1}[A-Za-z]{3,4}\/[\d.]{1,}"\s{1}\d+).*'


class UserSchema(Schema):
    query = fields.Str(required=True)
    file_name = fields.Str(required=True)


def get_path(file_name: str) -> Union[str, BadRequest]:
    file_path = os.path.join(DATA_DIR, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        return BadRequest(description=f'{file_path} is not exist')
    else:
        return file_path


def get_content(data: Dict[str, str]) -> str:
    file_path = get_path(data['file_name'])
    with open(file_path) as fp:
        res = build_query(data['query'], fp)
        return '\n'.join(res)


def build_query(query: str, fp: TextIO) -> List[str]:
    query_items = query.split('|')
    print(query_items)
    res = map(lambda v: v.strip(), fp)

    for item in query_items:
        split_item = item.split(':')
        cmd = split_item[0]

        if cmd in ('map', 'limit'):
            arg = int(split_item[1])
        else:
            arg = split_item[1]

        if cmd == 'filter':
            res = filter(lambda v, txt=arg: txt in v, res)
        if cmd == 'map':
            res = map(lambda v, index=arg: v.split(' ')[index], res)
        if cmd == 'unique':
            res = set(res)
        if cmd == 'sort':
            res = sorted(res, reverse=bool(arg == 'desc'))
        if cmd == 'limit':
            res = list(res)[:arg]
        if cmd == 'regex':
            reg_ex = reg_pattern.replace('_REG_EX_', arg)
            res = list([j for i in map(lambda r: re.findall(reg_ex, r), res) for j in i])

    return res
