"""Compare outputs from a deliberately narrow, fictional forms specification."""
from __future__ import annotations
from decimal import Decimal, InvalidOperation

SUPPORTED = {'text', 'number', 'select', 'calculated'}


def validate_schema(fields):
    if not isinstance(fields, list):
        raise ValueError('fields must be a list')
    names = set()
    for field in fields:
        if not isinstance(field, dict) or not isinstance(field.get('name'), str) or not field['name']:
            raise ValueError('Every field needs a name')
        if field['name'] in names:
            raise ValueError('Duplicate field name')
        names.add(field['name'])
        if field.get('type') not in SUPPORTED:
            raise ValueError(f"Unsupported type for {field['name']}")
        cond = field.get('visible_if')
        if cond is not None and (not isinstance(cond, dict) or len(cond) != 1):
            raise ValueError('visible_if must contain exactly one field/value')
        if field['type'] == 'calculated' and field.get('operation') not in {'multiply', 'add'}:
            raise ValueError('Only multiply/add calculations are supported')
    return names


def evaluate(fields, answers):
    names = validate_schema(fields)
    if not isinstance(answers, dict):
        raise ValueError('answers must be an object')
    output, issues = {}, []
    for field in fields:
        name = field['name']
        condition = field.get('visible_if')
        if condition is not None:
            ref, expected = next(iter(condition.items()))
            if ref not in names or ref == name:
                issues.append({'field':name,'code':'invalid_visibility_reference'})
                continue
            if answers.get(ref) != expected:
                continue
        value = answers.get(name)
        if field['type'] == 'calculated':
            operands = field.get('sources', [])
            if not isinstance(operands, list) or len(operands) != 2 or any(s not in names for s in operands):
                issues.append({'field':name,'code':'invalid_calculation_sources'})
                continue
            try:
                a, b = (Decimal(str(answers[s])) for s in operands)
                value = a * b if field['operation'] == 'multiply' else a + b
                value = str(value)
            except (KeyError, InvalidOperation, TypeError):
                issues.append({'field':name,'code':'invalid_number'})
                continue
        elif value is None or value == '':
            if field.get('required'):
                issues.append({'field':name,'code':'required_missing'})
            continue
        elif field['type'] == 'select' and value not in field.get('options', []):
            issues.append({'field':name,'code':'invalid_choice'})
            continue
        elif field['type'] == 'number':
            try:
                value = str(Decimal(str(value)))
            except InvalidOperation:
                issues.append({'field':name,'code':'invalid_number'})
                continue
        output[name] = value
    return {'output':output,'issues':issues}


def compare(spec):
    if not isinstance(spec, dict) or not isinstance(spec.get('cases'), list):
        raise ValueError('Expected source_fields, target_fields and cases')
    source, target = spec['source_fields'], spec['target_fields']
    validate_schema(source)
    validate_schema(target)
    results = []
    for case in spec['cases']:
        if not isinstance(case, dict) or not isinstance(case.get('answers'), dict):
            raise ValueError('Each case needs answers')
        left, right = evaluate(source, case['answers']), evaluate(target, case['answers'])
        results.append({'case':case.get('name', ''),'pass':left == right,
                        'source':left,'target':right})
    return {'mode':'offline_simulation','all_pass':all(x['pass'] for x in results),'cases':results,'form_submissions':0}
