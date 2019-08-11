
# file : userinfo/forms.py

from django import forms

class RegForm(forms.Form):
    username = forms.CharField(label='请输入姓名')
    password = forms.CharField(label='请输入密码')
    password2 = forms.CharField(label='请输入重复密码')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise forms.ValidationError("用户名太短")
        return username

    def clean(self):
        pwd1 = self.cleaned_data['password']
        pwd2 = self.cleaned_data['password2']
        if pwd1 != pwd2:
            raise forms.ValidationError('两次密码不一致')
        return self.cleaned_data


# class RegForm(forms.Form):
#     username = forms.CharField(label='请输入姓名',
#                                initial='XXXX',
#                                # widget=forms.Textarea,
#                                required = False)
#     password = forms.CharField(label='请输入密码',
#                                widget=forms.PasswordInput(
#                                    attrs={
#                                        "myattr1": 'value1',
#                                        'myattr2': 'value2'
#                                    }
#                                ))
#     password2 = forms.CharField(label='请输入重复密码')
#
