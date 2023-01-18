from functools import partial
from secrets import token_urlsafe
from typing import List, Dict, Any, Optional, Iterable, Union
from enum import Enum
from pathlib import Path
from ipaddress import IPv4Network, IPv6Network, IPv4Interface, IPv4Address
from pydantic import BaseModel, BaseSettings, Field, validator, root_validator, constr, conint
from passlib.hash import sha512_crypt
from sshpubkeys import SSHKey, InvalidKeyError
from .validators import (formatted_string, unique_system_ip, constrained_cidr, cidr_subnet, subnet_interface,
                         subnet_address)


#
# Common
#

class CloudInitEnum(str, Enum):
    v1 = 'v1'
    v2 = 'v2'


class InfraProviderOptionsEnum(str, Enum):
    aws = 'aws'
    gcp = 'gcp'
    azure = 'azure'
    vmware = 'vmware'


class InfraProviderControllerOptionsEnum(str, Enum):
    aws = 'aws'


class ComputeInstanceModel(BaseModel):
    image_id: str
    instance_type: Optional[str] = None


#
# global_config block
#

def resolve_ssh_public_key(pub_key: Union[str, None], pub_key_file: Union[str, None]) -> str:
    if pub_key is None and pub_key_file is not None:
        try:
            with open(pub_key_file) as f:
                return f.read()
        except FileNotFoundError as ex:
            raise ValueError(f"Error loading 'ssh_public_key_file': {ex}") from None

    if pub_key is not None and pub_key_file is None:
        return pub_key

    raise ValueError("Either 'ssh_public_key_file' or 'ssh_public_key' must be provided")


class GlobalConfigModel(BaseSettings):
    """
    GlobalConfigModel is a special config block as field values can use environment variables as their default value
    """
    home_dir: str = Field(..., env='HOME')
    project_root: str = Field(..., env='PROJ_ROOT')
    ubuntu_image: str
    ssh_public_key_file: str = Field(None, description='Can use python format string syntax to reference other '
                                                       'previous fields in this model')
    ssh_public_key: Optional[str] = None

    _validate_formatted_strings = validator('ssh_public_key_file', allow_reuse=True)(formatted_string)

    @validator('ssh_public_key', always=True)
    def resolve_ssh_public_key(cls, v, values: Dict[str, Any]):
        pub_key = resolve_ssh_public_key(v, values.get('ssh_public_key_file'))
        try:
            ssh_key = SSHKey(pub_key, strict=True)
            ssh_key.parse()
        except InvalidKeyError as ex:
            raise ValueError(f"Invalid SSH key: {ex}") from None
        except NotImplementedError as ex:
            raise ValueError(f"Invalid SSH key type: {ex}") from None

        return pub_key

    @validator('project_root')
    def resolve_project_root(cls, v: str) -> str:
        return str(Path(v).resolve())

    class Config:
        case_sensitive = True


#
# infra providers block
#
class InfraProviderConfigModel(BaseModel):
    ntp_server: constr(regex=r'^[a-zA-Z0-9.-]+$')


class GCPConfigModel(InfraProviderConfigModel):
    project: str


class VmwareConfigModel(InfraProviderConfigModel):
    vsphere_server: str
    vsphere_user: str = "administrator@vsphere.local"
    vsphere_password: str


class InfraProvidersModel(BaseModel):
    aws: Optional[InfraProviderConfigModel] = None
    gcp: Optional[GCPConfigModel] = None
    azure: Optional[InfraProviderConfigModel] = None
    vmware: Optional[VmwareConfigModel] = None


#
# controllers block
#

class ControllerCommonInfraModel(BaseModel):
    provider: InfraProviderControllerOptionsEnum
    region: str
    dns_domain: constr(regex=r'^[a-zA-Z0-9.-]+$') = Field(
        '', description="If set, add A records for control plane element external addresses in AWS Route 53")
    sw_version: constr(regex=r'^\d+(?:\.\d+)+$')
    cloud_init_format: CloudInitEnum = CloudInitEnum.v1

    class Config:
        use_enum_values = True


class ControllerCommonConfigModel(BaseModel):
    organization_name: str
    site_id: conint(ge=0, le=4294967295)
    acl_ingress_ipv4: List[IPv4Network]
    acl_ingress_ipv6: List[IPv6Network]
    cidr: IPv4Network
    vpn0_gateway: IPv4Address

    @validator('acl_ingress_ipv4', 'acl_ingress_ipv6')
    def acl_str(cls, v: Iterable[IPv4Network]) -> str:
        return ', '.join(f'"{entry}"' for entry in v)

    _validate_cidr = validator('cidr', allow_reuse=True)(constrained_cidr(max_length=23))


class CertAuthModel(BaseModel):
    passphrase: str = Field(default_factory=partial(token_urlsafe, 15))
    cert_dir: str
    ca_cert: str = '{cert_dir}/myCA.pem'

    _validate_formatted_strings = validator('ca_cert', always=True, allow_reuse=True)(formatted_string)


class ControllerConfigModel(BaseModel):
    system_ip: IPv4Address
    vpn0_interface_ipv4: IPv4Interface

    # Validators
    _validate_system_ip = validator('system_ip', allow_reuse=True)(unique_system_ip)


class VmanageConfigModel(ControllerConfigModel):
    username: str = 'admin'
    password: str = Field(default_factory=partial(token_urlsafe, 12))
    password_hashed: Optional[str] = None

    @validator('password_hashed', always=True)
    def hash_password(cls, v: Union[str, None], values: Dict[str, Any]) -> str:
        if v is None:
            clear_password = values.get('password')
            if clear_password is None:
                raise ValueError("Field 'password' is not present")
            # Using 'openssl passwd -6' recipe
            hashed = sha512_crypt.hash(clear_password, rounds=5000)
        else:
            hashed = v

        return hashed


class ControllerModel(BaseModel):
    infra: ComputeInstanceModel
    config: ControllerConfigModel


class VmanageModel(ControllerModel):
    config: VmanageConfigModel


class ControllersModel(BaseModel):
    infra: ControllerCommonInfraModel
    config: ControllerCommonConfigModel
    certificate_authority: CertAuthModel
    vmanage: VmanageModel
    vbond: ControllerModel
    vsmart: ControllerModel


#
# wan_edges block
#

class InfraVmwareModel(BaseModel):
    datacenter: str
    cluster: str
    datastore: str
    folder: str = ''
    vpn0_portgroup: str
    vpn512_portgroup: str
    servicevpn_portgroup: str


class EdgeInfraModel(ComputeInstanceModel):
    provider: InfraProviderOptionsEnum
    region: Optional[str] = None
    zone: Optional[str] = None
    sw_version: constr(regex=r'^\d+(?:\.\d+)+')
    cloud_init_format: CloudInitEnum = CloudInitEnum.v1
    sdwan_model: str
    sdwan_uuid: str
    vmware: Optional[InfraVmwareModel] = None

    @validator('region', always=True)
    def region_validate(cls, v, values: Dict[str, Any]):
        if v is None and values['provider'] != InfraProviderOptionsEnum.vmware:
            raise ValueError(f"{values['provider']} provider requires 'region' to be defined")
        if v is not None and values['provider'] == InfraProviderOptionsEnum.vmware:
            raise ValueError(f"'region' is not allowed when provider is {InfraProviderOptionsEnum.vmware}")

        return v

    @validator('zone', always=True)
    def zone_validate(cls, v, values: Dict[str, Any]):
        if v is None and values['provider'] == InfraProviderOptionsEnum.gcp:
            raise ValueError("GCP requires zone to be defined")

        return v

    @validator('vmware', always=True)
    def vmware_section(cls, v, values: Dict[str, Any]):
        if v is None and values['provider'] == InfraProviderOptionsEnum.vmware:
            raise ValueError(f"{InfraProviderOptionsEnum.vmware} provider requires 'vmware' section to be defined")
        if v is not None and values['provider'] != InfraProviderOptionsEnum.vmware:
            raise ValueError(f"'vmware' section is only allowed when provider is {InfraProviderOptionsEnum.vmware}")

        return v

    @root_validator
    def instance_type_validate(cls, values: Dict[str, Any]):
        if values['instance_type'] is None and values['provider'] != InfraProviderOptionsEnum.vmware:
            raise ValueError(f"{values['provider']} provider requires 'instance_type' to be defined")
        if values['instance_type'] is not None and values['provider'] == InfraProviderOptionsEnum.vmware:
            raise ValueError(f"'instance_type' is not allowed when provider is {InfraProviderOptionsEnum.vmware}")

        return values

    class Config:
        use_enum_values = True


class EdgeConfigModel(BaseModel):
    site_id: conint(ge=0, le=4294967295)
    system_ip: IPv4Address
    cidr: Optional[IPv4Network] = None
    vpn0_range: Optional[IPv4Network] = None
    vpn0_interface_ipv4: Optional[IPv4Interface] = None
    vpn0_gateway: Optional[IPv4Address] = None
    vpn1_range: Optional[IPv4Network] = None
    vpn1_interface_ipv4: Optional[IPv4Interface] = None

    # Validators
    _validate_system_ip = validator('system_ip', allow_reuse=True)(unique_system_ip)
    _validate_cidr = validator('cidr', allow_reuse=True)(constrained_cidr(max_length=23))
    _validate_vpn_range = validator('vpn0_range', 'vpn1_range', always=True, allow_reuse=True)(
        cidr_subnet(cidr_field='cidr', prefix_len=24)
    )
    _validate_vpn0_ipv4 = validator('vpn0_interface_ipv4', always=True, allow_reuse=True)(
        subnet_interface(subnet_field='vpn0_range', host_index=10)
    )
    _validate_vpn1_ipv4 = validator('vpn1_interface_ipv4', always=True, allow_reuse=True)(
        subnet_interface(subnet_field='vpn1_range', host_index=10)
    )
    _validate_vpn0_gw = validator('vpn0_gateway', always=True, allow_reuse=True)(
        subnet_address(subnet_field='vpn0_range', host_index=0)
    )


class EdgeModel(BaseModel):
    infra: EdgeInfraModel
    config: EdgeConfigModel


#
# Top-level ConfigModel
#

class ConfigModel(BaseModel):
    global_config: GlobalConfigModel
    infra_providers: InfraProvidersModel
    controllers: ControllersModel
    wan_edges: Dict[str, EdgeModel]
