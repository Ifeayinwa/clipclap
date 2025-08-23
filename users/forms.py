from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field attributes if needed
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'

class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text='Tell us about yourself'
    )
    website = forms.URLField(
        required=False,
        help_text='Your personal website or blog'
    )
    profile_pic = forms.ImageField(
        required=False,
        help_text='Upload a profile picture'
    )

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Handle password field properly for admin
        password = self.fields.get('password')
        if password:
            password.help_text = (
                "Raw passwords are not stored, so there is no way to see "
                "this user's password, but you can change the password using "
                '<a href="../password/">this form</a>.'
            )
            # You can also make the field readonly if preferred
            # password.widget.attrs['readonly'] = True

        # Customize other fields as needed
        self.fields['email'].required = True
        self.fields['user_type'].required = True

class SignUpForm(CustomUserCreationForm):
    """If you need a separate signup form with additional customizations"""
    terms_accepted = forms.BooleanField(
        required=True,
        label='I accept the terms and conditions'
    )

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('terms_accepted',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional customizations for signup form
        self.fields['password1'].help_text = 'Your password must be at least 8 characters long.'