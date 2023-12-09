from django.contrib import admin

from .models import question
from .models import IWanna
from .models import Comments

admin.site.register(question)
admin.site.register(IWanna)
admin.site.register(Comments)
