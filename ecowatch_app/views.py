from django.shortcuts import render, redirect
from .models import WasteSite, Video
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from allauth.account.views import SignupView

from django.urls import reverse, reverse_lazy

from django.contrib.auth import logout, login

from django.contrib import messages

from .filters import WasteSiteFilter

# from .forms import UploadForm, TagForm

def waste_site_list(request, **kwargs):
    queryset = WasteSite.objects.all()
    context = {}
    
    if 'my_post' in kwargs.keys() and request.user.is_authenticated:
        queryset = queryset.filter(user=request.user)
        context['my_post'] = ''
    
    f = WasteSiteFilter(request.GET, queryset=queryset)
    context['waste_sites'] = f
    print(f.qs.values())
    
    return render(request, 'ecowatch_app/waste_site_list.html', context)


@login_required(login_url="login")
def upload_and_tag(request):
    if request.method == 'POST':
        # Get data from the POST request
        video_file = request.FILES.get('video_file')

        city_name = request.POST.get('city_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        description = request.POST.get('description')
        
        # Create Video object
        video = Video.objects.create(video_file=video_file)
        
        # Create WasteSite object
        WasteSite.objects.create(user = request.user, city_name=city_name, latitude=latitude, longitude=longitude, description=description, video=video)
        
        return redirect('waste_site_list')  # Update with correct URL name
    else:
        return render(request, 'ecowatch_app/upload_and_tag.html')


class CustomLoginView(LoginView):
    template_name='ecowatch_app/login.html'
    field = '__all__'
    redirect_authenticated_user = True
    redirect_field_name = next
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        # Get the 'next' parameter from the request
        next_url = self.request.GET.get('next')
        # If 'next' parameter exists and it's a valid URL, redirect to that URL
        if next_url:
            return next_url
        # Otherwise, redirect to the home page
        return reverse_lazy('waste_site_list')


class CustomRegisterView(FormView):
    template_name='ecowatch_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = False
    # success_url = reverse_lazy('waste_site_list')

    def form_valid(self,form):                 # overriding form_valid method so that user don't have to login again after registration
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(CustomRegisterView,self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('waste_site_list')


def Logout(request):
    logout(request)
    messages.success(request,{"you've successfully logged out"})
    return redirect('waste_site_list')


# class AllAuthCustomLoginView(LoginView):
#     def get_redirect_url(self):
#         # Check for the 'next' parameter in the request
#         next_url = self.request.GET.get('next')
#         # Return the next URL if provided, otherwise default to LOGIN_REDIRECT_URL
#         return next_url if next_url else reverse_lazy('waste_site_list')



# class AllAuthCustomSignupView(SignupView):
#     def get_redirect_url(self):
#         # Check for the 'next' parameter in the request
#         next_url = self.request.GET.get('next')
#         # Return the next URL if provided, otherwise default to LOGIN_REDIRECT_URL
#         return next_url if next_url else reverse_lazy('waste_site_list')
