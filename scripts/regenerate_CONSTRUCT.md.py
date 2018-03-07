from constructor import construct
import jinja2
import sys
from os.path import join, dirname


valid_platforms = construct.ns_platform(sys.platform)

header = """
"""

template = """
# Keys in `construct.yaml` file:

This document describes each of they keys in the `construct.yaml` file,
which is the main configuration file of a constructor configuration
directory.

All keys are optional, except otherwise noted.  Also, the keys `specs`
and `packages` take either a list of items, or a path to a file,
which contains one item per line (excluding lines starting with `#`).

Also note, that any line in `construct.yaml` may contain a selector at the
end, in order to allow customization for selected platforms.


{% for key_info in keys %}
## `{{key_info[0]}}`

required: {{key_info[1]}}

argument type(s): {% for arg_type in key_info[2] %}``{{arg_type}}``, {% endfor %}
{{key_info[3]}}{% endfor %}

## List of available selectors:
{% for platform in platforms.keys() %}
- ``{{platform}}``{% endfor %}

"""

key_info_list = []
for key_info in construct.KEYS:
    try:
        key_types = iter(key_info[2])
    except TypeError:
        key_types = (key_info[2],)
    key_types = [k.__name__ for k in key_types]

    key_info_list.append((key_info[0], key_info[1], key_types, key_info[3]))

output = jinja2.Template(template).render(
    platforms=valid_platforms,
    keys=key_info_list)

with open(join(dirname(dirname(__file__)), 'CONSTRUCT.md'), 'w') as f:
    f.write(output)