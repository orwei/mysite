from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.urls import reverse
import markdown
# Create your models here.

class User(AbstractUser):
	user_image = models.CharField('头像', max_length=500, blank=True)
	signature = models.CharField('签名', max_length=200, blank=True)
	age = models.IntegerField('年龄', default=0)
	sex = models.CharField('性别',max_length=10)
	address = models.CharField('住址', max_length=100, blank=True)
	register_ip = models.GenericIPAddressField('注册IP地址', default='0.0.0.0')

	class Meta(AbstractUser.Meta):
		pass


# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
	# Django 要求模型必须继承 models.Model 类。
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Tag(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Post(models.Model):
	# 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
	title = models.CharField(max_length=100)  # 标题
	excerpt = models.CharField(max_length=200, blank=True)  # 摘要
	body = models.TextField()  # 正文
	created_time = models.DateTimeField(auto_now_add=True)  # 创作时间
	modified_time = models.DateTimeField()  # 修改时间
	category = models.ForeignKey(Category)	# 分类
	tag = models.ManyToManyField(Tag, blank=True)  # 标签
	author = models.ForeignKey(User)  # 作者
	visit = models.PositiveIntegerField(default=0)  # 访问次数，默认为0
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# blog 应用下的 name=detail 的函数
		'''
		如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
		那么 get_absolute_url 函数返回的就是 /post/255/ ，
		这样 Post 自己就生成了自己的 URL
		'''
		return reverse('blog:detail', kwargs={'pk':self.pk})

	def increase_visit(self):
		self.visit += 1
		self.save(update_fields=['visit'])

	def save(self, *args, **kwargs):
		if not self.excerpt:
			md = markdown.Morkdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
			self.excerpt = strip_tags(md.convert(self.body))[:40]
		super(Post, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Comment(models.Model):
	commentator = models.CharField(max_length=100)
	comment_ip = models.GenericIPAddressField(default='0.0.0.0')
	text = models.TextField()
	created_time = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(Post)

	def __str__(self):
		return self.text[:20]

@python_2_unicode_compatible
class Contact(models.Model):
	contact_name = models.CharField(max_length=100)
	contact_email = models.CharField(max_length=100)
	contact_ip = models.GenericIPAddressField(default='0.0.0.0')
	text = models.TextField()
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text[:50]
