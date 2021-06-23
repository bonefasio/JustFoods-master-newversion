from django.shortcuts import render
from main.models import *
from django.contrib import messages
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.decorators import *
from django.db.models import Sum

# Create your views here.


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'image', 'description', 'price',
              'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'staff/item_form.html'
    success_url = 'staff/item_list'
    fields = ['title', 'image', 'description', 'price',
              'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'staff/item_confirm_delete.html'
    success_url = 'staff/item_list'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.created_by:
            return True
        return False


@login_required(login_url='/accounts/login/')
@admin_only
def admin_view(request):
    cart_items = OrderItems.objects.filter(
        ordered=True, status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'staff/admin_view.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def pending_orders(request):
    items = OrderItems.objects.filter(
        ordered=True, isPaid=True, status="Active").order_by('-ordered_date')
    context = {
        'items': items,
    }
    return render(request, 'staff/pending_orders.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def order_delivery_details(request):

    cart_items = OrderItems.objects.filter(
        ordered=True, status="Active", isPaid=True)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'staff/paid_delivery_details.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def admin_dashboard(request):
    cart_items = OrderItems.objects.filter(
        ordered=True)
    pending_total = OrderItems.objects.filter(
        ordered=True, status="Active").count()
    completed_total = OrderItems.objects.filter(
        ordered=True, status="Delivered").count()
    count1 = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, item="3").count()
    count2 = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, item="4").count()
    count3 = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True, item="5").count()
    total = OrderItems.objects.filter(
        item__created_by=request.user, ordered=True).aggregate(Sum('item__price'))
    income = total.get("item__price__sum")
    context = {
        'pending_total': pending_total,
        'completed_total': completed_total,
        'income': income,
        'count1': count1,
        'count2': count2,
        'count3': count3,
    }
    return render(request, 'staff/admin_dashboard.html', context)


@login_required
@admin_only
def update_status(request, pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = OrderItems.objects.filter(
        ordered=True, status="Active", pk=pk)
    delivery_date = timezone.now()
    if status == 'Delivered':
        cart_items.update(
            status=status, delivery_date=delivery_date, isDelivered=True)
    return render(request, 'staff/pending_orders.html')


@login_required(login_url='/accounts/login/')
@admin_only
def item_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'staff/item_list.html', context)
