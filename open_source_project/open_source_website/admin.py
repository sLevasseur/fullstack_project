from django.contrib import admin
from .models import databaseForBlogs, databaseForNewsletter, databaseForCoordinates
from django.http import HttpResponse
import csv


# Register your models here


class InfoColumnGPS(admin.ModelAdmin):
    list_display = ['name_of_locations', 'adresse', 'code_postal', 'localite']


class InfoColumnBlog(admin.ModelAdmin):
    list_display = ['title', 'date']


def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for emails in queryset:
        row = writer.writerow([getattr(emails, field) for field in field_names])

    export_to_csv.short_description = "Export to CSV"
    return response
    # this method can be used to export any tables of your database as a csv file.
    # In this case I used it to export a mailing list. Convenient for the newsletter.


class ExportNewsletter(admin.ModelAdmin):
    list_display = ["email"]
    actions = [export_to_csv]


admin.site.register(databaseForBlogs, InfoColumnBlog)
admin.site.register(databaseForNewsletter, ExportNewsletter)
admin.site.register(databaseForCoordinates, InfoColumnGPS)
