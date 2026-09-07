from django.shortcuts import render, redirect
from .forms import VendorForm, BuyerForm, ProfileForm, OrderForm
from .models import Profile, Order
from shop.models import Goods
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
from django.views import View
from django.urls import reverse
from django.contrib.auth import logout
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
# Create your views here.


class VendorView(View):
    template_name = 'registration/vendor_reg.html'

    def get(self, request, *args, **kwargs):
        context = {'form': VendorForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("Это запрос:", request)
        form = VendorForm(request.POST)
        print("Это запрос 2:", form)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            login(request, user)
            group = Group.objects.get(name='Vendor')
            user.groups.add(group)
            user.save()
            return redirect('user:add_profile')
        context = {'form': form}
        return render(request, template_name='registration/vendor_reg.html', context=context)


class BuyerView(View):
    template_name = 'registration/buyer_reg.html'

    def get(self, request, *args, **kwargs):
        context = {'form': BuyerForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("Это запрос:", request)
        form = BuyerForm(request.POST)
        print("Это запрос 2:", form)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            login(request, user)
            group = Group.objects.get(name='Buyer')
            user.groups.add(group)
            user.save()
            return redirect('user:add_profile')
        context = {'form': form}
        return render(request, template_name='registration/buyer_reg.html', context=context)


class MyOwnLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('shop:main'))

class ProfileListView(ListView):
    model = Profile
    template_name = 'profile.html'
    # context_object_name = 'pro'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data()
        context['profile_user'] = Profile.objects.filter(user=user)
        return context


class AddProfileView(View):
    template_name = 'registration/add_profile.html'

    def get(self, request, *args, **kwargs):
        context = {'form': ProfileForm()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.name = request.user.name
            if request.user.groups.filter(name='Vendor').exists():
                form.group = 'Vendor'
            else:
                form.group = 'Buyer'
            form.save()
            return redirect('shop:main')
        context = {'form': form}
        return render(request, 'registration/add_profile.html', context=context)


class OrderView(DetailView, FormMixin):
    model = Goods
    template_name = 'order.html'
    context_object_name = 'goods'
    form_class = OrderForm

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        goods = self.get_object()
        user = self.request.user
        form.save()
        form.goods.add(goods)
        form.user.add(user)
        return super().form_valid(form)


    def get_success_url(self):
        goods = self.get_object()
        return reverse('shop:comment_goods', kwargs={'pk': goods.id})

    # def get(self, request, *args, **kwargs):
    #     context = {'form': OrderForm()}
    #     return render(request, self.template_name, context)
    #
    # def post(self, request, *args, **kwargs):
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         form = form.save(commit=False)
    #         goods = self.get_object()
    #         form.user = request.user
    #         form.goods = goods
    #         form.save()
    #         return redirect('shop:main')
    #     context = {'form': form}
    #     return render(request, 'user:order.html', context=context)
