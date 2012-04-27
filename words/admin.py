from models import Poem, Author
from django.contrib import admin

class AuthorInline(admin.StackedInline):
    model = Author
    extra = 3
    
class PoemAdmin(admin.ModelAdmin):
    list_display = ('name', 'circularity', 'disruption', 'sound', 'semantics', 'pub_date')
    list_filter = ['pub_date']
    inlines = [AuthorInline]
    fieldsets = [
        (None,                  {'fields': ['name', 'pub_date']}),
        ('Scoring Weights',     {'fields': ['circularity', 'disruption', 'sound', 'semantics'], 'classes': ['collapse']})
                ]
    

admin.site.register(Poem, PoemAdmin)

