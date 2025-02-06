terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 3.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_record" "task_tracker" {
  zone_id = var.cloudflare_zone_id
  name    = var.record_name       # e.g., "app" for app.yourdomain.com
  content = var.record_content    # For an A record, this is the IP address of your Render app
  type    = var.record_type       # Typically "A" (or "CNAME" if desired)
  ttl     = var.record_ttl        # e.g., 300 seconds
  proxied = var.proxied           # true or false, depending on your preference
}
