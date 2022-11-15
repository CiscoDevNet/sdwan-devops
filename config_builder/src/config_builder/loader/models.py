from functools import partial
from secrets import token_urlsafe
from typing import List
from ipaddress import IPv4Network, IPv6Network
from pydantic import BaseModel, Field, validator, constr


class CertAuthModel(BaseModel):
    passphrase: str = Field(default_factory=partial(token_urlsafe, 15))
    cert_dir: str = '/ansible/myCA'
    ca_cert: str = f'{cert_dir}/myCA.pem'


class ComputeInstanceModel(BaseModel):
    image_id: str
    instance_type: str = 't2.medium'


class VmanageConfigModel(BaseModel):
    username: str = 'admin'
    password: str = Field(default_factory=partial(token_urlsafe, 12))
    organization_name: str


class VmanageModel(ComputeInstanceModel):
    sw_version: constr(regex=r'^\d+(?:\.\d+)+')
    config: VmanageConfigModel
    instance_type: str = 't2.2xlarge'


class ControlPlaneInfraModel(BaseModel):
    provider: str
    datacenter: str
    certificate_authority: CertAuthModel
    acl_ingress_ipv4: List[IPv4Network]
    acl_ingress_ipv6: List[IPv6Network]
    cidr: IPv4Network
    vmanage: VmanageModel
    vbond: ComputeInstanceModel
    vsmart: ComputeInstanceModel

    @validator('acl_ingress_ipv4', 'acl_ingress_ipv6')
    def acl_str(cls, v):
        return ', '.join(f'"{entry}"' for entry in v)


class GlobalConfigModel(BaseModel):
    tf_vars_folder: str = ''
    csr1000v_image: str
    ubuntu_image: str


class EdgeInfraModel(BaseModel):
    iosxe_sdwan_image: str


class ConfigModel(BaseModel):
    global_config: GlobalConfigModel
    control_plane_infra: ControlPlaneInfraModel
    wan_edge_infra: EdgeInfraModel
