from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from apiservices.core.constants import BLOG
from django.shortcuts import render
from .forms import InputForm
from .utils import processInputDataAndGiveMatches


@api_view(["GET"])
def home(request):
    """
    :param request:
    :return: JSON response
    """
    data = {"Success": "Home"}

    return Response(data, status=HTTP_200_OK)


@api_view(["GET"])
def blog(request):
    """
    :param request:
    :return: JSON response
    """

    return Response(BLOG, status=HTTP_200_OK)


def home_view(request):
    username = "not logged in"
    if request.method == "POST":
        # Get the posted form
        MyLoginForm = InputForm(request.POST)

        if MyLoginForm.is_valid():
            # username = MyLoginForm.cleaned_data['first_name']
            print(MyLoginForm.cleaned_data)
            prop_data = processInputDataAndGiveMatches(MyLoginForm.cleaned_data)
            
            return render(request, 'loggedin.html', {"properties": prop_data})
            # return render(request, 'loggedin.html', {
            #     "first_name": str(MyLoginForm.cleaned_data),
            #     "day_list": ['sunday','monday','tuesday']
            # })
    context = {}
    context['form'] = InputForm()
    return render(request, "home.html", context)


# def home_view(request):
#     context ={}
#     context['form']= InputForm()
#     return render(request, "home.html", context)


# def home_view(request):
#     username = "not logged in"
#     if request.method == "POST":
#         #Get the posted form
#         MyLoginForm = InputForm(request.POST)

#         if MyLoginForm.is_valid():
#             username = MyLoginForm.cleaned_data['first_name']
#     else:
#         MyLoginForm = InputForm()

#     return render(request, 'loggedin.html', {"first_name" : username})
