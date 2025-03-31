from django.http import HttpRequest, HttpResponse


def django_greetings(request) -> HttpResponse:
    return HttpResponse(
        "<h1>Greetings from the Django APP!!! :)</h1>"
    )


def guten_tag(request):
    return HttpResponse("Guten Tag !, Herr Dmytr0 !")
