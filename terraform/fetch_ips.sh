#!/bin/bash

RESPONSE=$(curl -s --data "resp_format=json" https://my.imperva.com/api/integration/v1/ips)

IP_RANGES=$(echo $RESPONSE | jq -c '.ipRanges')
IPV6_RANGES=$(echo $RESPONSE | jq -c '.ipv6Ranges')

echo "{\"ip_ranges\": $IP_RANGES, \"ipv6_ranges\": $IPV6_RANGES}"
