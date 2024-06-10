from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
def allowed_users(allowed_roles=['worker']):
    def decorator(view_func):
        def wrapped_view(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == "worker":
                return view_func(request,*args, **kwargs)
            if group == "customer":
                return redirect("user:profile", pk=request.user.pk)

        return wrapped_view
    return decorator

class OwnProFileMixin:
    @method_decorator(login_required)
    @method_decorator(allowed_users())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



