from functools import partial
from secrets import token_urlsafe
from typing import List, Dict, Optional, Iterable, Union
from typing_extensions import Annotated
from enum import Enum
from pathlib import Path
from ipaddress import IPv4Network, IPv6Network, IPv4Interface, IPv4Address
from pydantic import field_validator, field_serializer, model_validator, Field, ConfigDict, BaseModel, ValidationInfo
from pydantic_settings import SettingsConfigDict, BaseSettings
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
    model_config = SettingsConfigDict(case_sensitive=True)

    home_dir: Annotated[str, Field(validation_alias='HOME')]
    project_root: Annotated[str, Field(validation_alias='PROJ_ROOT')]
    common_tags: Dict[str, str] = None
    ubuntu_image: str
    ssh_public_key_file: Annotated[Optional[str], Field(description='Can use python format string syntax to reference '
                                                                    'other previous fields in this model')] = None
    ssh_public_key: Annotated[Optional[str], Field(validate_default=True)] = None
    ssh_public_key_fp: Annotated[Optional[str], Field(validate_default=True)] = None

    _validate_formatted_strings = field_validator('ssh_public_key_file')(formatted_string)

    @field_validator('ssh_public_key')
    @classmethod
    def resolve_ssh_public_key(cls, v, info: ValidationInfo):
        pub_key = resolve_ssh_public_key(v, info.data.get('ssh_public_key_file'))
        try:
            ssh_key = SSHKey(pub_key, strict=True)
            ssh_key.parse()
        except InvalidKeyError as ex:
            raise ValueError(f"Invalid SSH key: {ex}") from None
        except NotImplementedError as ex:
            raise ValueError(f"Invalid SSH key type: {ex}") from None

        return pub_key

    @field_validator('ssh_public_key_fp')
    @classmethod
    def resolve_ssh_public_key_fp(cls, v: Union[str, None], info: ValidationInfo) -> str:
        if v is None:
            pub_key = info.data.get('ssh_public_key')
            if pub_key is None:
                raise ValueError("Field 'ssh_public_key' or 'ssh_public_key_file' not present")
            ssh_key = SSHKey(pub_key, strict=True)
            ssh_key.parse()
            fp = ssh_key.hash_md5().replace('MD5:', '').replace(':', '').upper() + " " + ssh_key.comment
        else:
            fp = v

        return fp

    @field_validator('project_root')
    @classmethod
    def resolve_project_root(cls, v: str) -> str:
        return str(Path(v).resolve())


#
# infra providers block
#
class InfraProviderConfigModel(BaseModel):
    ntp_server: Annotated[str, Field(pattern=r'^[a-zA-Z0-9.-]+$')]


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
    model_config = ConfigDict(use_enum_values=True)

    provider: InfraProviderControllerOptionsEnum
    region: str
    dns_domain: Annotated[str, Field(description="If set, add A records for control plane element external "
                                                 "addresses in AWS Route 53", pattern=r'^[a-zA-Z0-9.-]+$')] = ''
    sw_version: Annotated[str, Field(pattern=r'^\d+(?:\.\d+)+$')]
    cloud_init_format: CloudInitEnum = CloudInitEnum.v1


class ControllerCommonConfigModel(BaseModel):
    organization_name: str
    site_id: Annotated[int, Field(ge=0, le=4294967295)]
    acl_ingress_ipv4: List[IPv4Network]
    acl_ingress_ipv6: List[IPv6Network]
    cidr: IPv4Network
    vpn0_gateway: IPv4Address

    @field_serializer('acl_ingress_ipv4', 'acl_ingress_ipv6')
    def acl_str(self, v: Iterable[IPv4Network]) -> str:
        return ', '.join(f'"{entry}"' for entry in v)

    _validate_cidr = field_validator('cidr')(constrained_cidr(max_length=23))


class CertAuthModel(BaseModel):
    passphrase: str = Field(default_factory=partial(token_urlsafe, 15))
    cert_dir: str
    ca_cert: Annotated[str, Field(validate_default=True)] = '{cert_dir}/myCA.pem'

    _validate_formatted_strings = field_validator('ca_cert')(formatted_string)


class ControllerConfigModel(BaseModel):
    system_ip: IPv4Address
    vpn0_interface_ipv4: IPv4Interface

    # Validators
    _validate_system_ip = field_validator('system_ip')(unique_system_ip)


class VmanageConfigModel(ControllerConfigModel):
    username: str = 'admin'
    password: str = Field(default_factory=partial(token_urlsafe, 12))
    password_hashed: Annotated[Optional[str], Field(validate_default=True)] = None

    @field_validator('password_hashed')
    @classmethod
    def hash_password(cls, v: Union[str, None], info: ValidationInfo) -> str:
        if v is None:
            clear_password = info.data.get('password')
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
    model_config = ConfigDict(use_enum_values=True)

    provider: InfraProviderOptionsEnum
    region: Annotated[Optional[str], Field(validate_default=True)] = None
    zone: Annotated[Optional[str], Field(validate_default=True)] = None
    sw_version: Annotated[str, Field(pattern=r'^\d+(?:\.\d+)+')]
    cloud_init_format: CloudInitEnum = CloudInitEnum.v1
    sdwan_model: str
    sdwan_uuid: str
    vmware: Annotated[Optional[InfraVmwareModel], Field(validate_default=True)] = None

    @field_validator('region')
    @classmethod
    def region_validate(cls, v, info: ValidationInfo):
        if v is None and info.data['provider'] != InfraProviderOptionsEnum.vmware:
            raise ValueError(f"{info.data['provider']} provider requires 'region' to be defined")
        if v is not None and info.data['provider'] == InfraProviderOptionsEnum.vmware:
            raise ValueError(f"'region' is not allowed when provider is {InfraProviderOptionsEnum.vmware}")

        return v

    @field_validator('zone')
    @classmethod
    def zone_validate(cls, v, info: ValidationInfo):
        if v is None and info.data['provider'] == InfraProviderOptionsEnum.gcp:
            raise ValueError("GCP requires zone to be defined")

        return v

    @field_validator('vmware')
    @classmethod
    def vmware_section(cls, v, info: ValidationInfo):
        if v is None and info.data['provider'] == InfraProviderOptionsEnum.vmware:
            raise ValueError(f"{InfraProviderOptionsEnum.vmware} provider requires 'vmware' section to be defined")
        if v is not None and info.data['provider'] != InfraProviderOptionsEnum.vmware:
            raise ValueError(f"'vmware' section is only allowed when provider is {InfraProviderOptionsEnum.vmware}")

        return v

    @model_validator(mode='after')
    def instance_type_validate(self) -> 'EdgeInfraModel':
        if self.instance_type is None and self.provider != InfraProviderOptionsEnum.vmware:
            raise ValueError(f"{self.provider} provider requires 'instance_type' to be defined")
        if self.instance_type is not None and self.provider == InfraProviderOptionsEnum.vmware:
            raise ValueError(f"'instance_type' is not allowed when provider is {InfraProviderOptionsEnum.vmware}")

        return self


class EdgeConfigModel(BaseModel):
    site_id: Annotated[int, Field(ge=0, le=4294967295)]
    system_ip: IPv4Address
    cidr: Optional[IPv4Network] = None
    vpn0_range: Annotated[Optional[IPv4Network], Field(validate_default=True)] = None
    vpn0_interface_ipv4: Annotated[Optional[IPv4Interface], Field(validate_default=True)] = None
    vpn0_gateway: Annotated[Optional[IPv4Address], Field(validate_default=True)] = None
    vpn1_range: Annotated[Optional[IPv4Network], Field(validate_default=True)] = None
    vpn1_interface_ipv4: Annotated[Optional[IPv4Interface], Field(validate_default=True)] = None

    # Validators
    _validate_system_ip = field_validator('system_ip')(unique_system_ip)
    _validate_cidr = field_validator('cidr')(constrained_cidr(max_length=23))
    _validate_vpn_range = field_validator('vpn0_range', 'vpn1_range')(cidr_subnet(cidr_field='cidr', prefix_len=24))
    _validate_vpn0_ipv4 = field_validator('vpn0_interface_ipv4')(subnet_interface(subnet_field='vpn0_range',
                                                                                  host_index=10))
    _validate_vpn1_ipv4 = field_validator('vpn1_interface_ipv4')(subnet_interface(subnet_field='vpn1_range',
                                                                                  host_index=10))
    _validate_vpn0_gw = field_validator('vpn0_gateway')(subnet_address(subnet_field='vpn0_range', host_index=0))


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
