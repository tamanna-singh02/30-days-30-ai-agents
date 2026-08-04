from copy import deepcopy


def compute_diff(old, new):

    changes = {}

    all_keys = set(old.keys()) | set(new.keys())

    for key in all_keys:

        old_value = old.get(key)
        new_value = new.get(key)

        if old_value == new_value:
            continue

        if isinstance(old_value, dict) and isinstance(new_value, dict):

            nested = compute_diff(
                old_value,
                new_value,
            )

            if nested:
                changes[key] = nested

            continue

        changes[key] = {
            "old": deepcopy(old_value),
            "new": deepcopy(new_value),
        }

    return changes