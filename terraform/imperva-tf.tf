data "external" "fetch_ips" {
  program = ["./fetch_ips.sh"]
}

resource "aws_security_group" "imperva_sg" {
  name        = "imperva_sg"
  description = "Security group for Imperva IPs"

  dynamic "ingress" {
    for_each = data.external.fetch_ips.result.ip_ranges
    content {
      from_port   = 0
      to_port     = 65535
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }

  dynamic "ingress" {
    for_each = data.external.fetch_ips.result.ipv6_ranges
    content {
      from_port   = 0
      to_port     = 65535
      protocol    = "tcp"
      ipv6_cidr_blocks = [ingress.value]
    }
  }
}
