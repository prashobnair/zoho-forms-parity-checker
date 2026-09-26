# Zoho Forms Parity Checker

An offline checker for migrating a fictional form from one specification to another. It tests whether the same sample answers produce the same visible fields, required-field errors, choices and simple calculations. It never creates a Zoho Form or submits an answer.

## Contract use-case

The [Zoho CRM board](https://www.upwork.com/freelance-jobs/zoho-crm/) includes a forms rebuilding request. A [Jotform-to-Zoho Forms migration brief](https://www.freelancer.com/projects/branding/jotform-zoho-forms-migration) calls out conditional logic, calculations, notifications and matching output. This tool covers *input/output parity for a narrow form language*, not notifications or vendor configuration. The brief is an older/closed demand example, not a live opportunity or client project.

## Run it

Python 3.10+ and standard library only. From this repo's root:

```sh
python3 cli.py examples.json
python3 cli.py examples.json --strict  # exit code 2 on parity failure
python3 -m unittest discover -p 'test_*.py' -v
```

No Zoho/Jotform trial, login, API key, Docker or paid plan is needed. The fictional sample has three cases: a complete audit form passes; a delivery estimate fails because the target adds seats and rate instead of multiplying them (`203` vs `600`); a missing required audit detail produces the same error on both sides and passes parity. `all_pass` is false; `form_submissions` is zero. Changing the target `estimate.operation` to `multiply` makes all three pass. A pass means these fixtures agree, not full form compatibility.

## Contract

Each side declares a list of fields with unique `name`, `type` (`text`, `number`, `select`, `calculated`), optional `required`, single-field `visible_if` and options or arithmetic sources. Test cases supply `answers`. Hidden required fields are not validated. Calculations use Python Decimal and only `multiply` or `add` on two answers. The checker compares the source and target output and issue arrays. This is a **fictional intermediate schema**, not a Jotform or Zoho Forms export format.

## Boundaries

Real form migration needs current vendor metadata and sandbox tests of skip logic, repeaters, attachments, notifications, integrations, validation, accessibility, consent, localization and notification recipients. None are implemented here. Don't put actual respondent data in fixtures. `DESIGN.md` describes a mapping and acceptance process, the test matrix and known limitations.
