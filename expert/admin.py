from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from import_export import fields, resources
from import_export.admin import ImportMixin
from import_export.widgets import ForeignKeyWidget

from . import models


class ExpertResource(resources.ModelResource):
    username = fields.Field(column_name=_("User Name"), attribute="username")
    phone = fields.Field(column_name=_("Phone Number"), attribute="phone")
    sector = fields.Field(
        column_name=_("Sector"),
        attribute="sector",
        widget=ForeignKeyWidget(models.Sector, field="name"),
    )
    company = fields.Field(column_name=_("Company"), attribute="company")
    weight = fields.Field(column_name=_("Weight"), attribute="weight")

    def before_import_row(self, row, row_number=None, **kwargs):
        columns = {
            _("User Name"): "username",
            _("Phone Number"): "phone",
            _("Sector"): "sector",
            _("Company"): "company",
            _("Weight"): "weight",
        }
        for k, v in columns.items():
            if k in row:
                row[v] = row[k]

        sector_name = row["sector"]
        models.Sector.objects.get_or_create(
            name=sector_name, defaults=dict(name=sector_name)
        )
        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = models.Expert
        fields = ("username", "phone", "sector", "company", "weight")
        import_id_fields = ("username", "phone")


@admin.register(models.Expert)
class ExpertAdmin(ImportMixin, admin.ModelAdmin):
    resource_classes = [ExpertResource]
    list_display = ("username", "phone", "sector", "company")


@admin.register(models.Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.ProjectBlackList)
class ProjectBlackListAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectItem)
class ProjectBlackListAdmin(admin.ModelAdmin):
    pass


class ProjectBlackListInline(admin.TabularInline):
    model = models.ProjectBlackList
    exclude = ("experts",)


class ProjectItemInline(admin.TabularInline):
    model = models.ProjectItem
    exclude = ("experts",)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (
        ProjectBlackListInline,
        ProjectItemInline,
    )
    actions = ["display_experts_action"]

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            {
                "show_save_and_add_another": False,
                "show_save_and_continue": False,
            }
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    def display_experts_view(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(
                request, self.model._meta, object_id
            )

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied

        rows = []
        errors = []
        for item in obj.projectitem_set.all():
            count = 0
            for expert in item.experts.all():
                count += 1
                rows.append(expert)

            if count < item.count:
                errors.append(
                    _("The number of %s experts is not enough.") % item.sector.name
                )

        context = {
            **self.admin_site.each_context(request),
            "title": _("Display Experts: %s") % obj,
            "subtitle": None,
            "rows": rows,
            "errors": errors,
            "object": obj,
            "opts": self.model._meta,
            "preserved_filters": self.get_preserved_filters(request),
        }

        request.current_app = self.admin_site.name
        return TemplateResponse(request, "admin/expert/display_experts.html", context)

    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        my_urls = [
            path(
                "<path:object_id>/display_experts/",
                self.admin_site.admin_view(self.display_experts_view),
                name="%s_%s_display_experts" % info,
            ),
        ]
        return my_urls + urls

    def _response_post_save(self, request, obj):
        print(f"-- generate random experts: {obj}")
        block_companies = [x.company for x in obj.projectblacklist_set.all()]
        for item in obj.projectitem_set.all():
            experts = item.random_experts(
                item.sector, item.count, companies=block_companies
            )
            item.experts.clear()
            item.experts.add(*experts)
            item.save()

        opts = self.model._meta
        if self.has_view_or_change_permission(request):
            post_url = reverse(
                "admin:%s_%s_display_experts" % (opts.app_label, opts.model_name),
                kwargs=dict(object_id=obj.pk),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, post_url
            )
        else:
            post_url = reverse("admin:index", current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    @admin.action(description=_("View Experts"))
    def display_experts_action(self, request, queryset):
        if queryset.count() == 1 and self.has_view_or_change_permission(request):
            opts = self.model._meta
            post_url = reverse(
                "admin:%s_%s_display_experts" % (opts.app_label, opts.model_name),
                kwargs=dict(object_id=queryset.first().pk),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, post_url
            )
            return HttpResponseRedirect(post_url)

        self.message_user(
            request,
            ngettext("Please choose only one project to display experts."),
            messages.WARNING,
        )
