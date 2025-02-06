variable "cloudflare_api_token" {
  description = "API token for Cloudflare with permissions to manage DNS records"
  type        = string
}

variable "cloudflare_zone_id" {
  description = "Zone ID of your domain in Cloudflare"
  type        = string
}

variable "record_name" {
  description = "The subdomain name for the DNS record (e.g., 'app' for app.yourdomain.com)"
  type        = string
  default     = "app"
}

variable "record_content" {
  description = "The target content for the DNS record (for an A record, this is the IP address of your Render app)"
  type        = string
  default     = "your-render-app-ip"   # Replace with your actual Render app IP or CNAME target if using CNAME records
}

variable "record_type" {
  description = "DNS record type (typically 'A' or 'CNAME')"
  type        = string
  default     = "A"
}

variable "record_ttl" {
  description = "TTL (Time to Live) for the DNS record in seconds"
  type        = number
  default     = 300
}

variable "proxied" {
  description = "Whether the record is receiving the performance and security benefits of Cloudflare"
  type        = bool
  default     = true
}
