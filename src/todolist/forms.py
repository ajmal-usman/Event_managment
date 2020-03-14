from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Category,TodoList

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required =True)

    class Meta:
        model = User
        fields = (
            'username','first_name','last_name','email','password1','password2'
        )

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     # for fieldname in ['username','first_name','last_name','email','password1','password2']:
    #         # self.fields[fieldname].help_text = None


    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class TodoForm(forms.ModelForm):

    title = forms.CharField(
                            label='Description : ',
                            required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'What you need to do ?'})
                            )  
    category = forms.ModelChoiceField(queryset = Category.objects.all(),
                        label="Category : ")

    due_date = forms.DateTimeField(
                        input_formats=['%d/%m/%Y %H:%M'],
                        widget=forms.DateTimeInput(attrs={
                            'class': 'form-control datetimepicker-input',
                            'data-target': '#datetimepicker1'
                        })
                    )

   
    class Meta:
        model = TodoList
        fields  = ('title','category','due_date',)