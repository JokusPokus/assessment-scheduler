data google_project project {
  project_id = var.project
}

resource "google_storage_bucket" "media" {
  name     = "${var.project}-media"
  location = "europe-west3"
  storage_class = "REGIONAL"
}

data "google_iam_policy" "mediaaccess" {
  binding {
    role = "roles/storage.objectAdmin"
    members = [local.cloudrun_sa, local.cloudbuild_sa]
  }

  binding {
    role = "roles/storage.legacyBucketOwner"
    members = ["projectOwner:${var.project}", "projectEditor:${var.project}"]
  }
  binding {
    role = "roles/storage.legacyBucketReader"
    members = ["projectViewer:${var.project}"]
  }
}

resource "google_storage_bucket_iam_policy" "policy" {
  bucket = google_storage_bucket.media.name
  policy_data = data.google_iam_policy.mediaaccess.policy_data
}

resource "google_storage_bucket_access_control" "public_rule" {
  bucket = google_storage_bucket.media.name
  role   = "READER"
  entity = "allUsers"
}