from functools import partial
from secrets import token_urlsafe
from typing import List, Dict, Any, Optional
from enum import Enum
from ipaddress import IPv4Network, IPv6Network, IPv4Interface, IPv4Address
from pydantic import BaseModel, BaseSettings, Field, validator, constr
from passlib.hash import sha512_crypt


#
# Reusable validators
#

def formatted_string(v: str, values: Dict[str, Any]) -> str:
    """
    Process v as a python formatted string
    :param v: Value to be validated
    :param values: {<field name>: <field value> ...} dict of previously validated model fields
    :return: Expanded formatted string
    """
    try:
        return v.format(**values) if v is not None else v
    except KeyError as ex:
        raise ValueError(f"Variable not found: {ex}") from None


#
# global_config block
#

class GlobalConfigModel(BaseSettings):
    """
    GlobalConfigModel is a special config block as field values can use environment variables as their default value
    """
    home_dir: str = Field(..., env='HOME')
    tf_vars_folder: str = ''
    csr1000v_image: str
    ubuntu_image: str
    ssh_public_key_file: str = Field(None, description='Can use python format string syntax to reference other '
                                                       'previous fields in this model')
    ssh_public_key: Optional[str] = None

    _validate_formatted_strings = validator('ssh_public_key_file', allow_reuse=True)(formatted_string)

    @validator('ssh_public_key', always=True)
    def resolve_ssh_public_key(cls, v: str, values: Dict[str, Any]) -> str:
        pub_key_file = values.get('ssh_public_key_file')

        if v is None and pub_key_file is not None:
            try:
                with open(pub_key_file) as f:
                    return f.read()
            except FileNotFoundError as ex:
                raise ValueError(f"Error loading 'ssh_public_key_file': {ex}") from None

        if v is not None and pub_key_file is None:
            return v

        raise ValueError("Either 'ssh_public_key_file' or 'ssh_public_key' must be provided")

    class Config:
        case_sensitive = True


#
# control_plane_infra block
#

class CertAuthModel(BaseModel):
    passphrase: str = Field(default_factory=partial(token_urlsafe, 15))
    cert_dir: str
    ca_cert: str = '{cert_dir}/myCA.pem'

    _validate_formatted_strings = validator('ca_cert', always=True, allow_reuse=True)(formatted_string)


class ComputeInstanceModel(BaseModel):
    image_id: str
    instance_type: str = 't2.medium'


class VmanageConfigModel(BaseModel):
    username: str = 'admin'
    password: str = Field(default_factory=partial(token_urlsafe, 12))
    password_hashed: Optional[str] = None
    organization_name: str

    @validator('password_hashed', always=True)
    def hash_password(cls, v: str, values: Dict[str, Any]) -> str:
        if v is None:
            clear_password = values.get('password')
            if clear_password is None:
                raise ValueError("Field 'password' is not present")
            # Using 'openssl passwd -6' recipe
            hashed = sha512_crypt.hash(clear_password, rounds=5000)
        else:
            hashed = v

        return hashed


class VmanageModel(ComputeInstanceModel):
    sw_version: constr(regex=r'^\d+(?:\.\d+)+$')
    config: VmanageConfigModel
    instance_type: str = 't2.2xlarge'


class VbondConfigModel(BaseModel):
    vpn0_interface_ipv4: IPv4Interface


class VbondModel(ComputeInstanceModel):
    config: VbondConfigModel


class ControlPlaneInfraModel(BaseModel):
    provider: str
    datacenter: str
    dns_domain: constr(regex=r'^[a-zA-Z0-9.-]+$') = Field(
        '', description="If set, add A records for control plane element external addresses in AWS Route 53")
    ntp_server: IPv4Address
    certificate_authority: CertAuthModel
    acl_ingress_ipv4: List[IPv4Network]
    acl_ingress_ipv6: List[IPv6Network]
    cidr: IPv4Network
    vmanage: VmanageModel
    vbond: VbondModel
    vsmart: ComputeInstanceModel

    @validator('acl_ingress_ipv4', 'acl_ingress_ipv6')
    def acl_str(cls, v):
        return ', '.join(f'"{entry}"' for entry in v)


#
# wan_edge_infra block
#

class CloudInitEnum(str, Enum):
    v1 = 'v1'
    v2 = 'v2'


class EdgeModel(ComputeInstanceModel):
    provider: str
    datacenter: str
    sw_version: constr(regex=r'^\d+(?:\.\d+)+')
    iosxe_sdwan_image: str = Field(None, description="The default value is 'iosxe-sdwan-<sw_version>'")
    cloud_init_format: CloudInitEnum = CloudInitEnum.v2
    instance_type: str = 't3.medium'

    @validator('iosxe_sdwan_image', always=True)
    def resolve_iosxe_sdwan_image(cls, v: str, values: Dict[str, Any]) -> str:
        if v is None:
            try:
                return f"iosxe-sdwan-{values['sw_version']}"
            except KeyError:
                raise ValueError("Field 'sw_version' is not present") from None

        return v

    class Config:
        use_enum_values = True


class EdgeInfraModel(BaseModel):
    wan_edge_defaults: EdgeModel


#
# Top-level ConfigModel
#

class ConfigModel(BaseModel):
    global_config: GlobalConfigModel
    control_plane_infra: ControlPlaneInfraModel
    wan_edge_infra: EdgeInfraModel
