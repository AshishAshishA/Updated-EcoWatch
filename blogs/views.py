from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.db.models import F
from django.urls import reverse, reverse_lazy

from .models import Category, Post, Comment
from .forms import PostForm, CommentForm

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login, LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login
from django.contrib import messages

from allauth.account.views import SignupView

from django.core.paginator import Paginator

class UserAccessMixin(PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),self.get_login_url(),self.get_redirect_field_name())

        if not self.has_permission():
            messages.error(request, self.permission_denied_message)
            return redirect('home')
        return super(UserAccessMixin,self).dispatch(request,*args,**kwargs)

class CustomLoginView(LoginView):
    template_name='blogs/login.html'
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
        return reverse_lazy('home')

customLoginView = CustomLoginView.as_view()

class CustomRegisterView(FormView):
    template_name='blogs/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = False
    success_url = reverse_lazy('home')

    def form_valid(self,form):                 # overriding form_valid method so that user don't have to login again after registration
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(CustomRegisterView,self).form_valid(form)

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect('home')
    #     return super(CustomRegisterView, self).get(*args, **kwargs)
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')

customRegisterView = CustomRegisterView.as_view()

def Logout(request):
    logout(request)
    messages.success(request,{"you've successfully logged out"})
    return redirect('home')

#commented
    # class AllAuthCustomLoginView(LoginView):
    #     def get_redirect_url(self):
    #         # Check for the 'next' parameter in the request
    #         next_url = self.request.GET.get('next')
    #         print(next_url)
    #         # Return the next URL if provided, otherwise default to LOGIN_REDIRECT_URL
    #         return next_url if next_url else reverse_lazy('home')



    # class AllAuthCustomSignupView(SignupView):
    #     template_name='blogs/register.html'
    #     def get_redirect_url(self):
    #         # Check for the 'next' parameter in the request
    #         next_url = self.request.GET.get('next')
    #         # Return the next URL if provided, otherwise default to LOGIN_REDIRECT_URL
    #         return next_url if next_url else reverse_lazy('home')



class CreateBlogs(LoginRequiredMixin,UserAccessMixin,CreateView):
    raise_exception = False
    permission_required = 'blogs.add_post'
    permission_denied_message="not allowed"
    login_url = 'login'
    redirect_field_name = 'next'


    model=Post
    form_class=PostForm
    template_name='blogs/create_blog.html'

    def has_permission(self):
        # Check if the user has the required permissions
        return self.request.user.has_perm(self.permission_required)
    
    def get_success_url(self,*args,**kwargs):
        created_post = self.object
        return reverse('home-updated', args=[created_post.id, created_post.slug])

    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.has_perm('Post.add_post'):
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            # If user is not authenticated or does not have required permissions
            return self.handle_no_permission()

createBlogs = CreateBlogs.as_view()

class UpdateBlogsView(LoginRequiredMixin,UserAccessMixin,UpdateView):
    raise_exception = False
    permission_required = ['Post.change_Post',]
    permission_denied_message="not allowed"
    login_url = 'login'
    redirect_field_name = 'next'

    model=Post
    form_class=PostForm
    template_name='blogs/create_blog.html'

    def get_success_url(self):

        return reverse('home-updated', args=[self.kwargs['id'],self.kwargs['slug']])

updateBlogsView = UpdateBlogsView.as_view()

class DetailPostViewWithCommentForm(CreateView):
    model=Comment
    form_class=CommentForm
    template_name='blogs/detail_blog.html'
    # success_url=''

    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        # print(self.kwargs)
        post = Post.objects.filter(id=self.kwargs.get('id'))
        comments = Comment.objects.filter(post=(post.values())[0].get('id')).values()
        # print(post)
        post.update(views=F('views')+1)
        context['blog'] = post[0]
        print(post[0])
        context['comments'] = comments
        
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        post_id = self.kwargs.get('id')
        post = get_object_or_404(Post, id=post_id)
        
        kwargs['post'] = post
        return kwargs
    
    def get_success_url(self):

        return reverse('detail', args=[self.kwargs['slug'], self.kwargs['id']])

detailPostWithComments = DetailPostViewWithCommentForm.as_view()

class ListBlogs(ListView):
    model = Post
    template_name='blogs/list_blog.html'


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        blogs=context['blogs'] = Post.objects.all()

        context['cat']=''
        context['categories'] = Category.objects.all()
        context['latest_id'] = -1

        if 'id' in self.kwargs.keys():
            latest_id = context['latest_id'] = self.kwargs['id']
            latest_blog = context['latest_blog'] = (Post.objects.filter(id=self.kwargs['id']).values())[0]

        search_input = self.request.GET.get('search_area') or ''

        if search_input:
            blogs=context['blogs'] = context['blogs'].filter(title__icontains=search_input)

        if 'my_post' in self.kwargs.keys() and self.request.user.is_authenticated:
            # print(self.request.user)
            blogs=context['blogs'] = context['blogs'].filter(user=self.request.user)
            context['my_post']=''
            # print(blogs)

        context['search_input'] = search_input

        paginator = Paginator(blogs,3)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context

showListOfAllBlogs = ListBlogs.as_view()

class ListBlogByCategory(ListView):
    model = Post
    template_name='blogs/list_blog.html'
    context_object_name='blogs'
    paginate_by = 3

    def __init__(self):
        self.cat=None                    # cat -> category

    def get_queryset(self):
        self.cat = self.kwargs.get('category')
        if self.cat:
            return Post.objects.filter(categories__name__iexact=self.cat)
        else:
            return super().get_queryset()

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)

        context['cat']=self.cat
        context['categories'] = Category.objects.all()

        return context

showListByCategory=ListBlogByCategory.as_view()


class DeleteBlogsView(DeleteView):
    model=Post
    template_name='blogs/detail_blog.html'
    
    def get_success_url(self):

        return reverse_lazy('home')                                        

deleteBlogsView = DeleteBlogsView.as_view()


def generate_gpt_input_value(request):
    import os
    import ai21
    from ai21 import AI21Client

    AI21_API_KEY = os.environ.get('AI21_API_KEY')

    def get_safe_completion(prompt):
        print(f'inside completion {prompt}')

        client = AI21Client(
            # api_key='DyCMgHSZnyTAUwD1yKUfqwhUadC4xynU',
            api_key = AI21_API_KEY
        )
        completion = client.completion.create(
                model="j2-ultra",
                prompt=prompt,
                max_tokens=17,
                temperature=0.8,
            )
        
        first_completion = completion.completions[0]
        completion_text = first_completion.data.text

        print(f"completion text {completion_text}")

        return completion_text

    # ai21.api_key = 'DyCMgHSZnyTAUwD1yKUfqwhUadC4xynU'
    if request.method == "POST":
        print('inside post')
        blog_post = request.POST.get('gpt-body')

        prompt = f"No pretext or explanations. Write a concise website blog post title for the following blog post:{blog_post}"
        completion = get_safe_completion(prompt)
        
        return render(request, 'blogs/ai_res.html', {'ai_title':completion})
    return render(request, 'blogs/ai_res.html', {'ai_title':'not generated'})