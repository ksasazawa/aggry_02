from django import forms
from .models import Jobs

class JobSearchForm(forms.Form):
    # 職種の選択肢を作成
    job_choices = [('', ''), ('土木施工管理', '土木施工管理'), ('建築施工管理', '建築施工管理')]
    # 勤務地の選択肢を作成
    location_choices = [('', '')]
    for value in Jobs.objects.values_list('mod_location', flat=True).distinct():
        location_choices.append((value, value))
        
    job = forms.ChoiceField(choices=job_choices)
    location = forms.ChoiceField(choices=location_choices)
