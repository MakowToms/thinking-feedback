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
        fields = ["title", "required_passes"]


class SkillLevelNewSkillModelForm(forms.ModelForm):
    class Meta:
        model = SkillLevel
        fields = ["skills"]

    def __init__(self, topic, *args, **kwargs):
        super(SkillLevelNewSkillModelForm, self).__init__(*args, **kwargs)
        self.fields["skills"].queryset = Skill.objects.filter(topic=topic)


class SkillLevelModelForm(forms.ModelForm):
    class Meta:
        model = SkillLevel
        fields = ["level", "description", "required_passes"]

    def __init__(self, skill, level=None, *args, **kwargs):
        super(SkillLevelModelForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # If it's a new instance (not being edited)
            self.fields['required_passes'].initial = skill.required_passes
            if level is not None:
                self.fields['level'].initial = level
