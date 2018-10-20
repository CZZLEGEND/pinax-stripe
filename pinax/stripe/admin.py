from django.contrib import admin
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from .models import (
    Event,
    EventProcessingException
)


class ModelAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Adjust change_view title ("View" instead of "Change")."""
        opts = self.model._meta

        extra_context = extra_context or {}
        extra_context["title"] = _("View %s" % force_text(opts.verbose_name))
        return super(ModelAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def has_change_permission(self, request, obj=None):
        if request.method == "POST":
            return False
        return True


class EventProcessingExceptionAdmin(ModelAdmin):
    list_display = [
        "message",
        "event",
        "created_at"
    ]
    search_fields = [
        "message",
        "traceback",
        "data"
    ]
    raw_id_fields = [
        "event"
    ]


class EventAdmin(ModelAdmin):
    list_display = [
        "stripe_id",
        "kind",
        "livemode",
        "valid",
        "processed",
        "created_at",
        "account_id",
        "customer_id"
    ]
    list_filter = [
        "kind",
        "created_at",
        "valid",
        "processed"
    ]
    search_fields = [
        "stripe_id",
        "customer_id",
        "validated_message",
        "account_id",
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(EventProcessingException, EventProcessingExceptionAdmin)
