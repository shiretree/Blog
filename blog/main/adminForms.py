from django import forms

class PostAdminForm(forms.ModelForm):

    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)   #将原来摘要的CharField改成Textarea