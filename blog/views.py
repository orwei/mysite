# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import ListView, DetailView
from .forms import RegisterForm, CommentForm, ContactForm
from .models import Post, Category, User, Contact
from django.contrib.auth import *
from django import template
import markdown


# 获取文章
# def index(request):
# 	post_list = Post.objects.all().order_by('-created_time')
# 	return render(request, 'index.html', context={'post_list':post_list})

# # 归档和分类
# def archive(request, year, month):
# 	post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
# 	return render(request, 'index.html', context={'post_list':post_list})

# def category(request, pk):
# 	cate = get_object_or_404(Category, pk=pk)
# 	post_list = Post.objects.filter(category=cate).order_by('-created_time')
# 	return render(request, 'index.html', context={'post_list':post_list})

class IndexView(ListView):
	model = Post
	template_name = 'index.html'
	context_object_name = 'post_list'
	paginate_by = 3

class ArchiveView(ListView):
	model = Post
	template_name = 'index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		archive = super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month).order_by('-created_time')
		return archive

class CategoryView(ListView):
	model = Post
	template_name = 'index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		category = super(CategoryView, self).get_queryset().filter(category=cate).order_by('-created_time')
		return category


def about(request):
	return render(request, 'blog/about.html')


def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.increase_visit()
	post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc'])
	form = CommentForm()
	comment_list = post.comment_set.all()
	context = {'post':post, 'form':form, 'comment_list':comment_list}
	return render(request, 'blog/detail.html', context=context)

def register(request):
	redirect_to = request.POST.get('next', request.GET.get('next', ''))
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			register = form.save(commit=False)
			register.registerip = request.META['REMOTE_ADDR']
			register.save()
			if redirect_to:
				return redirect(redirect_to)
			else:
				return redirect('/')
	else:
		form = RegisterForm()
	return render(request, 'blog/register.html', context={'form':form, 'next':redirect_to})


# 评论
def comment(request, post_pk):
	post = get_object_or_404(Post, pk=post_pk)
	if request.method == 'POST':	
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.commentator = request.user.username
			comment.commentator_image = request.user.user_image
			comment.comment_ip = request.META['REMOTE_ADDR']
			comment.post = post
			comment.save()
			return redirect(post)
		else:
			comment_list = post.comment_set.all()
			context = {'post':post, 'form':form, 'comment_list':comment_list}
			return render(request, 'blog/detail.html', context=context)
	return redirect(post)

# 联系
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			contact = form.save(commit=False)
			contact.contact_ip = request.META['REMOTE_ADDR']
			contact.save()
			return render(request, 'blog/contact_done.html')
	else:
		form = ContactForm()
	return render(request, 'blog/contact.html', context={'form':form})

