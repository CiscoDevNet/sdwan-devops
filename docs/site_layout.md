# Site Layout

## Site IDs

```
Site ID Format
[Region][Site]

Region
    1: East
    2: West
    3: Cloud East
    4: Cloud West
    5: AzureStack
    6: Azure
    7: Google

Site Ranges by Type
    00-09 - DCs, Co-Los, Hubs
    10-19 - Branch Type 1 (Full Mesh, no DIA)
    20-29 - Branch Type 2 (Full Mesh, DIA)
    30-39 - Branch Type 3 (Hub and Spoke)
    40-49 - Branch Type 4 (Hub and Spoke with FW)

Sites IDs
    RTP
    100: RTP Campus
    110: SMC
    120: chocker

    SJC    
    200: SJC Building 18
    
    HRN
    300: Herndon Lab
    
    AWS
    400: AWS us-east-1 Cloud Onramp

    AZS
    500: Herndon AZS
```

## System IPs

```

Each system IP is instantiated as loopback0 and part of the corporate VPN (VPN 11)
```

## VPNs

```
 10: Guest
 11: Corporate
 ```

## Interfaces

```
GE0/0
GE0/1
```

## Colors:

```
Default
```

## Network Services

```
    Domain Name: ciscops.net
    DHCP: 199.66.188.66, 192.133.180.133
    DNS: 199.66.188.66, 192.133.180.133
    NTP: us.pool.ntp.org
    Logging: 
    Netflow: 
    SNMP: 
    SMTP: 
```