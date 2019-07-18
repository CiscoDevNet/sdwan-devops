# Public Sector Cloud Ready Network Introduction

## Introduction

There have been several impactful architectural shifts in IT over the past several years, but none larger than the
public cloud.  The benefits and strategic “cloud first” mandates within the US Federal agencies have created a new set
of requirements as the applications move from the on-prem data center, to the remote, less controlled public cloud
(IaaS/SaaS).  This transformation of application “location” is having an impact on several indirect factors,
specifically how agencies approach next-generation WAN designs requirements, but also security, specifically controlling
the access to these applications that reside in locations with far less visibility and control (i.e. the public cloud)
as they once did in their localized on-prem data centers.

## Cloud Ready Network (CRN) Overview

The CRN architecture can be divided into two general domains, each of which support critical components for securing and
maintaining the Quality of Experience (QoE) needed as the applications relocate to the public cloud

![CRN Overvirew](images/crn_overview.png)

The two key components include, per the diagram above, (1) the secure WAN domain, and (2) the introduction of the
CoLocation center domain for the newly defined “Cloud Edge” demarcation.

### CoLocation Center

The CoLocation center domain introduces a newer concept we define as “cloud edge”, leveraging a private cage within the
CoLo facility for hosting both the WAN routers (discussed above) and the remote security stack for securing and
controlling access to the public cloud IaaS/SaaS resources.  

![CRN Overvirew](images/colo_overview.png)

Colocation facilities provide cross connection
services that simplify the interconnection to the transport and public cloud service providers.  This architecture 
proposes a government agency leverages a private cage/rack within the CoLo to establish a new “cloud edge” demarcation
point for security and visibility controls for agency traffic going to, or coming from, the applications residing in
public cloud Iaas/SaaS services.  This concept establishes a tighter security domain closer to the public cloud exchange
point.  Furthermore, this new “cloud edge” in the CoLo establishes the security controls and visibility closer to the
applications (e.g. in the cloud) eliminating the need for back-haul to the security stack at the agency location not
inline to the cloud edge.  The strategic location of using Colocation facilities greatly reduces “hair-pinning” traffic and reduces
latency and overall application performance to the cloud services, specifically for multi-cloud environments (e.g. traffic traversing from cloud provider 1 to cloud provider 2).

Finally, for the purposes of this proposal, the security guidelines are based on the [DHS Trusted Internet Connection
Reference Architecture Document v2.2 design recommendations](https://www.dhs.gov/sites/default/files/publications/TIC_Ref_Arch_v2.2_2017.pdf)
and follow all of the required services for
“External Connection Security Pattern” as stated by DHS policy.

### Wan Domain

The WAN domain can leverage any new or existing WAN solutions.  [Cisco SD-WAN](https://www.cisco.com/c/en/us/solutions/enterprise-networks/sd-wan/index.html) is transforming into a preferred
solution for this CRN design because of its application intelligent routing awareness over any transport
(MPLS, Internet, 4G/LTE/5G).  This applies either to the CoLocation center and through the security stack, or extending
the WAN edge router directly into the public cloud provider via [cloud On-Ramp capabilities for IaaS and SaaS](https://www.cisco.com/c/dam/en/us/solutions/collateral/enterprise-networks/sd-wan/cloud-onramp.pdf).
Alternative WAN solutions for extending the agency WAN into the CoLocation center can also include private IP, MPLS, or
Segment Routing, and Cisco is recommending the use of [WAN MACsec](https://www.cisco.com/c/dam/en/us/td/docs/solutions/Enterprise/Security/MACsec/WP-High-Speed-WAN-Encrypt-MACsec.pdf) for securing the WAN links terminating into the
agency rack inside the CoLocation centers. 

![CRN Overvirew](images/sdwan_overview.png)


Cisco's SD-WAN Fabric offers the following benefits:
* Segmentation: Topology-driven network-wide segmentation
* Service Chaining: Insertion of security services into the traffic flow, including firewalls, IDS, as well as third-party solutions.
* End-to-End Encryption: Secure, zero-trust, authenticated transport, the ability to extend the SD-WAN encrypted fabric into public cloud providers (such as AWS and Azure) by automatically instantiating virtual SD-WAN endpoints in the enterprise customer’s cloud region.
* Application Aware Routing: Intelligent traffic steering based on application awareness of the application’s locations (on-premise, public cloud like Amazon Web Services (AWS) and Azure, or SaaS) and SLA requirements needed over a specific WAN link, including application brownout mitigation.
* High-Availability: East/West COLO presence for geographic load-balancing and redundancy
* Transport independence: Major cost reduction relating to WAN, including circuit cost, operational expenditure, and the ability to leverage lower-cost bandwidth services, through transport optimization.
* Analytics: Advanced analytics for both real-time insight to the WAN fabric’s behavior, as well as future-looking “what-if” analysis for billing, capacity planning, all cloud managed.

