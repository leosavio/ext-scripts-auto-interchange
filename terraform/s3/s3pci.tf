provider "aws" {
  region = "us-west-1" # Change this to your preferred region
}

resource "aws_s3_bucket" "pci_compliant_bucket" {
  bucket = "my-pci-compliant-bucket" # Change this to your preferred bucket name

  # Ensure the bucket is not publicly accessible
  acl    = "private"

  # Enable versioning to preserve, retrieve, and restore every version of every object stored in the S3 bucket
  versioning {
    enabled = true
  }

  # Enable default encryption for the S3 bucket
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
        # kms_master_key_id = "arn:aws:kms:your-region:111122223333:key/abcd1234-a123-456a-a12b-a123b4cd56ef" # Uncomment and provide the KMS key ARN if you want to use a specific KMS key
      }
    }
  }

  # Enable Server Access Logging for the S3 bucket
  logging {
    target_bucket = aws_s3_bucket.log_bucket.bucket
    target_prefix = "log/"
  }
}

resource "aws_s3_bucket" "log_bucket" {
  bucket = "my-pci-compliant-log-bucket" # Change this to your preferred log bucket name
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_public_access_block" "public_access_block" {
  bucket = aws_s3_bucket.pci_compliant_bucket.bucket

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_config_configuration_recorder" "s3_recorder" {
  name     = "s3-pci-compliance-recorder"
  role_arn = aws_iam_role.config_role.arn

  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
}

resource "aws_config_delivery_channel" "s3_channel" {
  name           = "s3-pci-compliance-channel"
  s3_bucket_name = aws_s3_bucket.pci_compliant_bucket.bucket
  s3_key_prefix  = "config"

  snapshot_delivery_properties {
    delivery_frequency = "TwentyFour_Hours"
  }
}

resource "aws_iam_role" "config_role" {
  name = "aws-config-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "config.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "config_attach" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSConfigRole"
  role       = aws_iam_role.config_role.name
}
