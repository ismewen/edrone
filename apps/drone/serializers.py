from rest_framework import serializers

from apps.drone.models import Repos, Builds
from dutils.fields import NestedModelField


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repos
        fields = "__all__"


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builds
        fields = "__all__"


class BuildCreateSerializer(serializers.ModelSerializer):
    repo = NestedModelField(Repos, lookup_field="pk")

    class Meta:
        model = Builds
        fields = "__all__"
