resource "google_cloud_run_service" "examsched" {
  name                       = var.service
  location                   = var.region
  autogenerate_revision_name = true
  template {
    spec {
      service_account_name = google_service_account.examsched.email
      containers {
        image = "gcr.io/${var.project}/examsched"
        env {
          name = "CURRENT_HOST"
          value = "*"
        }
        env {
          name = "APPLICATION_STAGE"
          value = "production"
        }
      }
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale"      = "100"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.postgres.connection_name
        "run.googleapis.com/client-name"        = "terraform"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}
resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.examsched.location
  project     = google_cloud_run_service.examsched.project
  service     = google_cloud_run_service.examsched.name
  policy_data = data.google_iam_policy.noauth.policy_data
}