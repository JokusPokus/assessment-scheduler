terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }

  backend "remote" {
    organization = "CODEScheduler"

    workspaces {
      name = "examsched"
    }
  }
}

provider "google" {
  project = var.project
}

data "google_project" "project" {
  project_id = var.project
}

resource "google_service_account" "examsched" {
  account_id   = var.service
  display_name = "${var.service} service account"

  depends_on = [google_project_service.iam]
}

locals {
  examsched_sa   = "serviceAccount:${google_service_account.examsched.email}"
  cloudbuild_sa = "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
}

resource google_project_iam_binding service_permissions {
  for_each = toset([
    "run.admin", "cloudsql.client"
  ])

  project    = var.project
  role       = "roles/${each.key}"
  members    = [local.cloudbuild_sa, local.examsched_sa]
  depends_on = [google_service_account.examsched]
}

resource google_service_account_iam_binding cloudbuild_sa {
  service_account_id = google_service_account.examsched.name
  role               = "roles/iam.serviceAccountUser"

  members = [local.cloudbuild_sa]
}