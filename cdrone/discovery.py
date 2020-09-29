from werkzeug.utils import import_string, find_modules


def auto_discovery():
    for mod in find_modules("apps", recursive=True):
        if str(mod).endswith("tasks"):
            import_string(mod)
        elif str(mod).endswith("views"):
            import_string(mod)


def auto_get_urlpatterns():
    urlpatterns = []
    for mod in find_modules("apps", recursive=True):
        if str(mod).endswith("urls"):
            model = import_string(mod)
            if hasattr(model, "urlpatterns") and isinstance(model.urlpatterns, list):
                urlpatterns += model.urlpatterns
    return urlpatterns

