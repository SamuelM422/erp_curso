def dynamic_permission(permission_to):
    def wrapper(view):
        setattr(view, 'permission_to', permission_to)
        return view
    return wrapper