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


class BuildCreateSerializer(serializers.Serializer):
    repo = NestedModelField(Repos, lookup_field="pk")
    branch = serializers.CharField()

    def create(self, validated_data):
        repo = validated_data.get("repo")
        branch = validated_data.get("branch")
        res = repo.create_build(branch=branch)
        build = Builds.objects.all().get(pk=res.get_id())
        return build
