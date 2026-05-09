from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Category, Listing, ListingImage
from .forms import ListingForm

class ListingListView(ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
    paginate_by = 20
    queryset = Listing.objects.filter(status='active').select_related('category', 'user').prefetch_related('images')

    def get_queryset(self):
        qs = super().get_queryset()
        city = self.request.GET.get('city')
        sort = self.request.GET.get('sort', '-created_at')
        if city:
            qs = qs.filter(city=city)
        if sort in ['created_at', '-created_at', 'price', '-price']:
            qs = qs.order_by('-is_urgent', sort)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cities'] = Listing.objects.filter(status='active').values_list('city', flat=True).distinct()
        ctx['current_city'] = self.request.GET.get('city', '')
        return ctx

class ListingByCategoryView(ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
    paginate_by = 20

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        children = category.children.all()
        return Listing.objects.filter(
            Q(category=category) | Q(category__in=children),
            status='active'
        ).select_related('category', 'user').prefetch_related('images')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        ctx['cities'] = Listing.objects.filter(status='active').values_list('city', flat=True).distinct()
        return ctx

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        for img in self.request.FILES.getlist('images'):
            try:
                ListingImage.objects.create(listing=self.object, image=img)
            except Exception:
                pass  # skip image save failure (e.g. read-only fs)
        messages.success(self.request, '信息发布成功！')
        return response

    def get_success_url(self):
        return reverse('listings:detail', args=[self.object.slug])

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'listings/listing_form.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse('listings:detail', args=[self.object.slug])

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    template_name = 'listings/listing_confirm_delete.html'
    success_url = reverse_lazy('dashboard:home')

    def test_func(self):
        return self.get_object().user == self.request.user

class SearchView(ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return Listing.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q),
            status='active'
        ).select_related('category', 'user').prefetch_related('images')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx
