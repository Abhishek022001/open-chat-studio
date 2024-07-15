from functools import cached_property

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from field_audit import audit_fields
from field_audit.models import AuditingManager
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase

from apps.teams.models import BaseTeamModel, Team
from apps.users.models import CustomUser


class TagCategories(models.TextChoices):
    BOT_RESPONSE = "bot_response", _("Bot Response")


@audit_fields("name", "slug", "created_by", "team", audit_special_queryset_writes=True)
class Tag(TagBase, BaseTeamModel):
    name = models.CharField(verbose_name=pgettext_lazy("A tag name", "name"), max_length=100)
    created_by = models.ForeignKey("users.CustomUser", on_delete=models.DO_NOTHING, null=True, default=None)
    is_system_tag = models.BooleanField(default=False)
    category = models.CharField(choices=TagCategories.choices, blank=True, default="")

    objects = AuditingManager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        unique_together = ("team", "name", "is_system_tag", "category")
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("annotations:tag_edit", args=[self.team.slug, self.id])


@audit_fields("user", "team", "tag", "object_id", "content_type", audit_special_queryset_writes=True)
class CustomTaggedItem(GenericTaggedItemBase, BaseTeamModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.DO_NOTHING, null=True, default=None)
    tag = models.ForeignKey(Tag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE)

    objects = AuditingManager()

    class Meta:
        indexes = [
            models.Index(
                fields=["content_type", "object_id"],
            )
        ]

        constraints = [
            models.UniqueConstraint(
                fields=("content_type", "object_id", "tag"),
                name="content_type_object_id_tag_id_4bb97a8e_uniq",
            )
        ]


class AnnotationMixin:
    @cached_property
    def object_info(self):
        import json

        return json.dumps(
            {
                "id": self.id,
                "app": self._meta.app_label,
                "model_name": self._meta.model_name,
            }
        )


class TaggedModelMixin(models.Model, AnnotationMixin):
    """Models supporting `tags` should use this mixin"""

    class Meta:
        abstract = True

    tags = TaggableManager(through=CustomTaggedItem)

    def add_tags(self, tags: list[str], team: Team, added_by: CustomUser):
        tag_objs = Tag.objects.filter(team=team, name__in=tags)
        for tag in tag_objs:
            self.tags.add(tag, through_defaults={"team": team, "user": added_by})

    @property
    def get_linked_tags(self):
        # return [{"user": item.user.username, "tag": item.tag.name} for item in self.tagged_items.all()]
        return [item.tag.name for item in self.tagged_items.all()]

    @property
    def get_system_tags(self):
        return self.tags.filter(is_system_tag=True)


class UserComment(BaseTeamModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.DO_NOTHING)
    comment = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    @transaction.atomic()
    @staticmethod
    def add_for_model(model, comment: str, added_by: CustomUser, team: Team) -> "UserComment":
        if model._meta.get_field("comments"):
            UserComment.objects.create(content_object=model, user=added_by, comment=comment, team=team)

    def __str__(self):
        return f'<{self.user.username}>: "{self.comment}"'


class UserCommentsMixin(models.Model, AnnotationMixin):
    comments = GenericRelation(UserComment)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def get_user_comments(self) -> UserComment:
        return self.comments.prefetch_related("user").all()

    @property
    def comment_count_element_id(self) -> str:
        """Returns the id of the element that contains the number of user comments on this object"""
        return f"{self._meta.model_name}-{self.id}-comment-count"
