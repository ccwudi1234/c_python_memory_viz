import re


def parse_memory(output: str) -> dict:
    stack_vars = []
    heap_blocks = []
    static_vars = []
    constants = []

    for line in output.splitlines():
        if not line.startswith('ANALYZER:'):
            continue

        segment = line[len('ANALYZER:'):]
        section, _, payload = segment.partition(':')
        fields = dict(item.split('=', 1) for item in payload.split(';') if '=' in item)

        if section == 'STACK':
            stack_vars.append({
                'name': fields.get('name', 'unknown'),
                'address': fields.get('addr', '0x0'),
                'value': fields.get('value', ''),
                'type': fields.get('type', 'unknown')
            })
        elif section == 'HEAP':
            heap_blocks.append({
                'name': fields.get('name', 'heap'),
                'address': fields.get('addr', '0x0'),
                'size': fields.get('size', 'unknown'),
                'type': fields.get('type', 'malloc'),
                'value': fields.get('value', '')
            })
        elif section == 'STATIC':
            static_vars.append({
                'name': fields.get('name', 'static'),
                'address': fields.get('addr', '0x0'),
                'value': fields.get('value', ''),
                'type': fields.get('type', 'static')
            })
        elif section == 'CONST':
            constants.append({
                'name': fields.get('name', 'const'),
                'address': fields.get('addr', '0x0'),
                'value': fields.get('value', ''),
                'ref_count': fields.get('ref_count', 'N/A')
            })

    return {
        'stack': stack_vars,
        'heap': heap_blocks,
        'static': static_vars,
        'constants': constants
    }
