import os
import re
import pathlib

import yaml


def load_config(path):
    PROJECT_ROOT = pathlib.Path(__file__).parent.parent
    var_pattern = re.compile(r'^(.*)?\$\{(.*)\}(.*)$')

    yaml.add_implicit_resolver("!vars", var_pattern)
    VARS = {
        'PROJECT_ROOT': PROJECT_ROOT
    }

    def _yaml_vars_constructor(loader, node):
        value = loader.construct_scalar(node)
        prefix, var_name, postfix = var_pattern.match(value).groups()
        return f'{prefix}{VARS.get(var_name)}{postfix}'
    yaml.add_constructor('!vars', _yaml_vars_constructor)

    with open(f'{PROJECT_ROOT}/{path}', 'r') as f:
        return yaml.load(f)
