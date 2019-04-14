models = {}


def register_model(uuid):
    def wrapper(f):
        models[uuid] = f
        return f

    return wrapper


@register_model('copy')
def copy(inputs):
    return inputs[0]