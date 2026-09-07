from django.shortcuts import render, redirect
from .models import Rubric, Goods, Comment
from user.models import Profile
from .forms import CommentForm, GoodsForm
from user.forms import ProfileForm
from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


class RubricList(ListView):
    model = Rubric
    template_name = 'main.html'
    context_object_name = 'rubric'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['goods'] = Goods.objects.filter()
        return context

# class GoodsForMainPage(DetailView):
#     model = Goods
#     template_name = 'comment_goods.html'
#     context_object_name = 'goods'

class RubricDetailView(DetailView):
    model = Rubric
    template_name = 'detail_goods.html'
    context_object_name = 'rubric'

    def get_context_data(self, **kwargs):
        rubric = self.get_object()
        context = super().get_context_data()
        context['goods'] = Goods.objects.filter(rubric=rubric)
        return context

    def get_success_url(self):
        rub = self.get_object()

        return reverse('shop:detail_goods', kwargs={'pk': rub.id})


class GoodsView(DetailView, FormMixin):
    model = Goods
    template_name = 'comment_goods.html'
    context_object_name = 'goods'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        goods = self.get_object()
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(goods=goods)
        return context

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        goods = self.get_object()
        form.goods = goods
        form.name = self.request.user.name
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        goods = self.get_object()

        return reverse('shop:comment_goods', kwargs={'pk': goods.id})




class Goods_add(PermissionRequiredMixin, View):
    template_name = 'add_goods.html'

    def get(self, request, *args, **kwargs):
        context = {'form': GoodsForm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            goods = form.save(commit=False) # Мы ПОЛУЧАЕМ эту форму и сохраняем в переменную goods, а туда уже
            # добавляем значения
            created_by = self.request.user
            goods.created_by = created_by
            goods.save()
            return redirect('shop:main')
        context = {'form': form}
        return render(request, template_name='add_goods.html', context=context)

    def has_permission(self):
        if self.request.user.groups.filter(name='Vendor').exists():
            return True
        else:
            return False


class UpdateGoodView(UpdateView):
    model = Goods
    form_class = GoodsForm
    template_name = 'edit_goods.html'

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/profile/')

        # return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        goods = self.get_object()
        return reverse('shop:comment_goods', kwargs={'pk': goods.id})



class DeleteGoodView(DeleteView):
    model = Goods
    template_name = 'delete_goods.html'
    success_url = '/'

class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'comment_goods.html'
    success_url = '/'

class OrderView(FormMixin, DetailView):
    model = Goods
    template_name = 'add_order.html'
    context_object_name = 'goods'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        profile = self.get_object
        context = super().get_context_data()
        context['user'] = self.request.user
        return context

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        profile_user = self.request.user
        good = self.get_object()
        profile_user.order.create(title=good.title)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        goods = self.get_object()

        return reverse('shop:add_order', kwargs={'pk': goods.id})


def AgreementFunc(request):
    return render(request, 'agreement.html')