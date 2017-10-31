from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Comment, Contact

class RegisterForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "email")

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']
		# form表单属性修改
		widgets = {
			'text':forms.Textarea(attrs={
				# 'cols':100, 
				'placeholder':'请写上你想说的话',
				# 'style':'backgroud: #111',
			}),
		}

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['contact_name', 'contact_email', 'text']