import pickle


def picklecache(cachefile, name=None, default=None):
    def decorator(fxn):
        def _(*args, **kwargs):
            try:
                with open(cachefile, 'rb') as fd:
                    data = pickle.load(fd)
            except IOError:
                if default is None:
                    raise
                data = default()
            if name is None:
                data = fxn(data, *args, **kwargs)
            else:
                kwargs[name] = data
                data = fxn(*args, **kwargs)
            with open(cachefile, 'wb+') as fd:
                pickle.dump(data, fd)
            return data
        return _
    return decorator
