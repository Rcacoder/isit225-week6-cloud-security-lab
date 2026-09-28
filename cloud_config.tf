# ============================================================================
# cloud_config.tf
#
# This is teaching-only HCL for a static-analysis exercise. It is never
# deployed (no `terraform apply` is run) — the grader reads this file as text
# and checks specific fields, so you can fix it with a plain text editor.
#
# Scenario: a contractor set up this deployment for "Northgate Retail" and
# left before finishing security review. Six controls are wrong. Fix them.
# ============================================================================

resource "storage_bucket" "app_data" {
  bucket_name = "app-data-public"     # FIX 1: must be "app-data-<your-github-username>"
  acl         = "public-read"         # FIX 1: must be "private"
  encryption  = "disabled"            # FIX 5: must be "enabled"
  logging_enabled = false             # FIX 6: must be true
}

resource "compute_instance" "web_server" {
  name       = "northgate-web-01"
  image      = "ubuntu-22-04"
  db_password = "SuperSecret123!"     # FIX 2: never commit a real secret — use a variable reference instead
}

resource "firewall_rule" "allow_ssh" {
  name        = "allow-ssh-admin"
  protocol    = "tcp"
  from_port   = 22
  to_port     = 22
  cidr_blocks = ["0.0.0.0/0"]         # FIX 3: SSH must not be open to the entire internet
}

resource "iam_policy" "app_service_account" {
  role = "app-service-account"
  actions   = ["*"]                   # FIX 4: grant only the specific actions the app needs
  resources = ["*"]                   # FIX 4: scope to the specific bucket, not everything
}
