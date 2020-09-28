from django.db import models


class Builds(models.Model):
    build_id = models.AutoField(primary_key=True)
    build_repo_id = models.IntegerField(blank=True, null=True)
    build_config_id = models.IntegerField(blank=True, null=True)
    build_trigger = models.CharField(max_length=250, blank=True, null=True)
    build_number = models.IntegerField(blank=True, null=True)
    build_parent = models.IntegerField(blank=True, null=True)
    build_status = models.CharField(max_length=50, blank=True, null=True)
    build_error = models.CharField(max_length=500, blank=True, null=True)
    build_event = models.CharField(max_length=50, blank=True, null=True)
    build_action = models.CharField(max_length=50, blank=True, null=True)
    build_link = models.CharField(max_length=2000, blank=True, null=True)
    build_timestamp = models.IntegerField(blank=True, null=True)
    build_title = models.CharField(max_length=2000, blank=True, null=True)
    build_message = models.CharField(max_length=2000, blank=True, null=True)
    build_before = models.CharField(max_length=50, blank=True, null=True)
    build_after = models.CharField(max_length=50, blank=True, null=True)
    build_ref = models.CharField(max_length=500, blank=True, null=True)
    build_source_repo = models.CharField(max_length=250, blank=True, null=True)
    build_source = models.CharField(max_length=500, blank=True, null=True)
    build_target = models.CharField(max_length=500, blank=True, null=True)
    build_author = models.CharField(max_length=500, blank=True, null=True)
    build_author_name = models.CharField(max_length=500, blank=True, null=True)
    build_author_email = models.CharField(max_length=500, blank=True, null=True)
    build_author_avatar = models.CharField(max_length=2000, blank=True, null=True)
    build_sender = models.CharField(max_length=500, blank=True, null=True)
    build_deploy = models.CharField(max_length=500, blank=True, null=True)
    build_params = models.CharField(max_length=4000, blank=True, null=True)
    build_started = models.IntegerField(blank=True, null=True)
    build_finished = models.IntegerField(blank=True, null=True)
    build_created = models.IntegerField(blank=True, null=True)
    build_updated = models.IntegerField(blank=True, null=True)
    build_version = models.IntegerField(blank=True, null=True)
    build_cron = models.CharField(max_length=50)
    build_deploy_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'builds'
        unique_together = (('build_repo_id', 'build_number'),)


class Cron(models.Model):
    cron_id = models.AutoField(primary_key=True)
    cron_repo = models.ForeignKey('Repos', models.DO_NOTHING, blank=True, null=True)
    cron_name = models.CharField(max_length=50, blank=True, null=True)
    cron_expr = models.CharField(max_length=50, blank=True, null=True)
    cron_next = models.IntegerField(blank=True, null=True)
    cron_prev = models.IntegerField(blank=True, null=True)
    cron_event = models.CharField(max_length=50, blank=True, null=True)
    cron_branch = models.CharField(max_length=250, blank=True, null=True)
    cron_target = models.CharField(max_length=250, blank=True, null=True)
    cron_disabled = models.BooleanField(blank=True, null=True)
    cron_created = models.IntegerField(blank=True, null=True)
    cron_updated = models.IntegerField(blank=True, null=True)
    cron_version = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cron'
        unique_together = (('cron_repo', 'cron_name'),)


class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    log_data = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class Migrations(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'migrations'


class Nodes(models.Model):
    node_id = models.AutoField(primary_key=True)
    node_uid = models.CharField(max_length=500, blank=True, null=True)
    node_provider = models.CharField(max_length=50, blank=True, null=True)
    node_state = models.CharField(max_length=50, blank=True, null=True)
    node_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    node_image = models.CharField(max_length=500, blank=True, null=True)
    node_region = models.CharField(max_length=100, blank=True, null=True)
    node_size = models.CharField(max_length=100, blank=True, null=True)
    node_os = models.CharField(max_length=50, blank=True, null=True)
    node_arch = models.CharField(max_length=50, blank=True, null=True)
    node_kernel = models.CharField(max_length=50, blank=True, null=True)
    node_variant = models.CharField(max_length=50, blank=True, null=True)
    node_address = models.CharField(max_length=500, blank=True, null=True)
    node_capacity = models.IntegerField(blank=True, null=True)
    node_filter = models.CharField(max_length=2000, blank=True, null=True)
    node_labels = models.CharField(max_length=2000, blank=True, null=True)
    node_error = models.CharField(max_length=2000, blank=True, null=True)
    node_ca_key = models.BinaryField(blank=True, null=True)
    node_ca_cert = models.BinaryField(blank=True, null=True)
    node_tls_key = models.BinaryField(blank=True, null=True)
    node_tls_cert = models.BinaryField(blank=True, null=True)
    node_tls_name = models.CharField(max_length=500, blank=True, null=True)
    node_paused = models.BooleanField(blank=True, null=True)
    node_protected = models.BooleanField(blank=True, null=True)
    node_created = models.IntegerField(blank=True, null=True)
    node_updated = models.IntegerField(blank=True, null=True)
    node_pulled = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nodes'


class Orgsecrets(models.Model):
    secret_id = models.AutoField(primary_key=True)
    secret_namespace = models.CharField(max_length=50, blank=True, null=True)
    secret_name = models.CharField(max_length=200, blank=True, null=True)
    secret_type = models.CharField(max_length=50, blank=True, null=True)
    secret_data = models.BinaryField(blank=True, null=True)
    secret_pull_request = models.BooleanField(blank=True, null=True)
    secret_pull_request_push = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orgsecrets'
        unique_together = (('secret_namespace', 'secret_name'),)


class Perms(models.Model):
    perm_user_id = models.IntegerField(primary_key=True)
    perm_repo_uid = models.CharField(max_length=250)
    perm_read = models.BooleanField(blank=True, null=True)
    perm_write = models.BooleanField(blank=True, null=True)
    perm_admin = models.BooleanField(blank=True, null=True)
    perm_synced = models.IntegerField(blank=True, null=True)
    perm_created = models.IntegerField(blank=True, null=True)
    perm_updated = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perms'
        unique_together = (('perm_user_id', 'perm_repo_uid'),)


class Repos(models.Model):
    repo_id = models.AutoField(primary_key=True)
    repo_uid = models.CharField(unique=True, max_length=250, blank=True, null=True)
    repo_user_id = models.IntegerField(blank=True, null=True)
    repo_namespace = models.CharField(max_length=250, blank=True, null=True)
    repo_name = models.CharField(max_length=250, blank=True, null=True)
    repo_slug = models.CharField(unique=True, max_length=250, blank=True, null=True)
    repo_scm = models.CharField(max_length=50, blank=True, null=True)
    repo_clone_url = models.CharField(max_length=2000, blank=True, null=True)
    repo_ssh_url = models.CharField(max_length=2000, blank=True, null=True)
    repo_html_url = models.CharField(max_length=2000, blank=True, null=True)
    repo_active = models.BooleanField(blank=True, null=True)
    repo_private = models.BooleanField(blank=True, null=True)
    repo_visibility = models.CharField(max_length=50, blank=True, null=True)
    repo_branch = models.CharField(max_length=250, blank=True, null=True)
    repo_counter = models.IntegerField(blank=True, null=True)
    repo_config = models.CharField(max_length=500, blank=True, null=True)
    repo_timeout = models.IntegerField(blank=True, null=True)
    repo_trusted = models.BooleanField(blank=True, null=True)
    repo_protected = models.BooleanField(blank=True, null=True)
    repo_synced = models.IntegerField(blank=True, null=True)
    repo_created = models.IntegerField(blank=True, null=True)
    repo_updated = models.IntegerField(blank=True, null=True)
    repo_version = models.IntegerField(blank=True, null=True)
    repo_signer = models.CharField(max_length=50, blank=True, null=True)
    repo_secret = models.CharField(max_length=50, blank=True, null=True)
    repo_no_forks = models.BooleanField()
    repo_no_pulls = models.BooleanField()
    repo_cancel_pulls = models.BooleanField()
    repo_cancel_push = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'repos'


class Secrets(models.Model):
    secret_id = models.AutoField(primary_key=True)
    secret_repo = models.ForeignKey(Repos, models.DO_NOTHING, blank=True, null=True)
    secret_name = models.CharField(max_length=500, blank=True, null=True)
    secret_data = models.BinaryField(blank=True, null=True)
    secret_pull_request = models.BooleanField(blank=True, null=True)
    secret_pull_request_push = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secrets'
        unique_together = (('secret_repo', 'secret_name'),)


class Stages(models.Model):
    stage_id = models.AutoField(primary_key=True)
    stage_repo_id = models.IntegerField(blank=True, null=True)
    stage_build_id = models.IntegerField(blank=True, null=True)
    stage_number = models.IntegerField(blank=True, null=True)
    stage_name = models.CharField(max_length=100, blank=True, null=True)
    stage_kind = models.CharField(max_length=50, blank=True, null=True)
    stage_type = models.CharField(max_length=50, blank=True, null=True)
    stage_status = models.CharField(max_length=50, blank=True, null=True)
    stage_error = models.CharField(max_length=500, blank=True, null=True)
    stage_errignore = models.BooleanField(blank=True, null=True)
    stage_exit_code = models.IntegerField(blank=True, null=True)
    stage_limit = models.IntegerField(blank=True, null=True)
    stage_os = models.CharField(max_length=50, blank=True, null=True)
    stage_arch = models.CharField(max_length=50, blank=True, null=True)
    stage_variant = models.CharField(max_length=10, blank=True, null=True)
    stage_kernel = models.CharField(max_length=50, blank=True, null=True)
    stage_machine = models.CharField(max_length=500, blank=True, null=True)
    stage_started = models.IntegerField(blank=True, null=True)
    stage_stopped = models.IntegerField(blank=True, null=True)
    stage_created = models.IntegerField(blank=True, null=True)
    stage_updated = models.IntegerField(blank=True, null=True)
    stage_version = models.IntegerField(blank=True, null=True)
    stage_on_success = models.BooleanField(blank=True, null=True)
    stage_on_failure = models.BooleanField(blank=True, null=True)
    stage_depends_on = models.TextField(blank=True, null=True)
    stage_labels = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stages'
        unique_together = (('stage_build_id', 'stage_number'),)


class Steps(models.Model):
    step_id = models.AutoField(primary_key=True)
    step_stage_id = models.IntegerField(blank=True, null=True)
    step_number = models.IntegerField(blank=True, null=True)
    step_name = models.CharField(max_length=100, blank=True, null=True)
    step_status = models.CharField(max_length=50, blank=True, null=True)
    step_error = models.CharField(max_length=500, blank=True, null=True)
    step_errignore = models.BooleanField(blank=True, null=True)
    step_exit_code = models.IntegerField(blank=True, null=True)
    step_started = models.IntegerField(blank=True, null=True)
    step_stopped = models.IntegerField(blank=True, null=True)
    step_version = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'steps'
        unique_together = (('step_stage_id', 'step_number'),)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_login = models.CharField(unique=True, max_length=250, blank=True, null=True)
    user_email = models.CharField(max_length=500, blank=True, null=True)
    user_admin = models.BooleanField(blank=True, null=True)
    user_active = models.BooleanField(blank=True, null=True)
    user_machine = models.BooleanField(blank=True, null=True)
    user_avatar = models.CharField(max_length=2000, blank=True, null=True)
    user_syncing = models.BooleanField(blank=True, null=True)
    user_synced = models.IntegerField(blank=True, null=True)
    user_created = models.IntegerField(blank=True, null=True)
    user_updated = models.IntegerField(blank=True, null=True)
    user_last_login = models.IntegerField(blank=True, null=True)
    user_oauth_token = models.CharField(max_length=500, blank=True, null=True)
    user_oauth_refresh = models.CharField(max_length=500, blank=True, null=True)
    user_oauth_expiry = models.IntegerField(blank=True, null=True)
    user_hash = models.CharField(unique=True, max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
