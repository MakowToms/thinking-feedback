from classes.models import Stage
from thinking_feedback import settings


def dev_processor(request):
    dev = settings.DEV
    return {'dev': dev}


def stages_processor(request):
    stages = Stage.objects.filter(teacher__pk=request.user.pk, is_active=True)
    return {'stages': stages, "chosen_stage": False}
