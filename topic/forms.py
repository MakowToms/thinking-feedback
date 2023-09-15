from django import forms

from .models import Topic, Skill, SkillLevel
from classes.models import Stage


class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "stage"]

    def __init__(self, user, *args, **kwargs):
        super(TopicModelForm, self).__init__(*args, **kwargs)
        self.fields["stage"].queryset = Stage.objects.filter(teacher=user)


class SkillModelForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["title"]


class SkillLevelModelForm(forms.ModelForm):
    class Meta:
        model = SkillLevel
        fields = ["level", "description"]
