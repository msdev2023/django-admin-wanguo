import numpy as np
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

EXPERT_WEIGHT = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (9999, 5),
)


class Sector(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Sector Name"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")


class Expert(models.Model):
    username = models.CharField(
        max_length=32, db_index=True, verbose_name=_("User Name")
    )
    phone = models.BigIntegerField(db_index=True, verbose_name=_("Phone Number"))
    sector = models.ForeignKey(
        Sector, db_index=True, on_delete=models.PROTECT, verbose_name=_("Sector")
    )
    company = models.CharField(max_length=128, default="", verbose_name=_("Company"))
    weight = models.SmallIntegerField(
        default=1,
        choices=EXPERT_WEIGHT,
        help_text=_(
            "The higher the number, the higher the probability of being selected"
        ),
        verbose_name=_("Weight"),
    )

    def __str__(self):
        return f"{self.username} - {self.sector}"

    class Meta:
        verbose_name = _("Expert")
        verbose_name_plural = _("Experts")
        unique_together = ("username", "phone")


class Project(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name=_("Project Name"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class ProjectBlackList(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.CharField(
        max_length=128, verbose_name=_("Select a company to block")
    )

    def __str__(self):
        return f"#{self.id}-{self.company}"

    class Meta:
        verbose_name = _("Project BlackList")
        verbose_name_plural = _("Project BlackList")


class ProjectItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sector = models.ForeignKey(
        Sector, on_delete=models.PROTECT, verbose_name=_("Select a sector")
    )
    count = models.PositiveIntegerField(verbose_name=_("Select the number of experts"))
    experts = models.ManyToManyField(Expert)

    def __str__(self):
        return f"{self.sector} x{self.count}"

    class Meta:
        verbose_name = _("Project Item")
        verbose_name_plural = _("Project Items")

    @classmethod
    def random_experts(cls, sector, count, companies=None):
        q = Expert.objects.filter(sector=sector)
        if companies:
            q = q.filter(~Q(company__in=companies))
        if q.count() <= count:
            return [x for x in q]

        populations = [x for x in q]
        weights = [x.weight for x in populations]
        total = sum(weights)
        weights = [i / total for i in weights]
        return np.random.choice(populations, count, False, weights)
