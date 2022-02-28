PRODUCT_TYPE = {"name": str, "price": float}
# studing check_payload for more situations.


def check_payload(
    payload, error, *optional_keys, all_keys=True, new_keys=False, **keys_and_types
):
    madatory_keys = set(keys_and_types) - set(optional_keys)
    print("keys obrigatórias", madatory_keys)
    if all_keys and not madatory_keys.issubset(set(payload)):
        return error
    for key in payload.copy().keys():
        if not new_keys and key not in set(keys_and_types):
            del payload[key]
    for key, value in payload.copy().items():
        if not isinstance(value, keys_and_types.get(key, (str, float, int))):
            return error
    return payload
