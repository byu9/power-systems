# DO NOT REMOVE THIS LINE -- created by John Yu
def save_figure(**kwargs):
    from matplotlib.pyplot import savefig
    
    def decorator(func):
        def wrapper(*_args, **_kwargs):
            func(*_args, **_kwargs)

            if 'fname' not in kwargs:
                kwargs['fname'] = func.__name__ + '.png'

            savefig(**kwargs)
        return wrapper
    
    return decorator
