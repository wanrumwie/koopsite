from functools import wraps
from urllib.parse import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url, get_object_or_404
from django.utils.decorators import available_attrs
from koopsite import settings

def request_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the REQUEST, *ARGS, **KWARGS
    and returns True if the user passes.
    Функція майже повністю повторює стандартну user_passes_test()
    Змінено тільки рядок:
            if test_func(request, *args, **kwargs):
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # змінено наступний рядок:
            if test_func(request, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def author_or_permission_required(model, perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user is object owner
    or has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    Функція майже повністю повторює стандартну permission_required()
    Додано тільки оператор:
        if 'pk' in kwargs: ...
    """
    def check_perms(request, *args, **kwargs):
        user = request.user
        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # Тепер перевіряємо чи user є власником (автором) об'єкта,
        # pk якого має бути в kwargs
        if 'pk' in kwargs:
            object_id = kwargs['pk']
            try:
                object = get_object_or_404(model, pk=object_id)
                if user == object.user:
                    return True
            except:
                pass
                print('except 404, model =', model, 'pk =', object_id)
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return request_passes_test(check_perms, login_url=login_url)

#---------------- Кінець коду, охопленого тестуванням ------------------

