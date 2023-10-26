package main


#
# Functions
#

# Given a full SD-WAN version, get just the version train
get_version_train(version) := v {
    parts = split(version, ".")
    x := parts[0]
    y := parts[1]
    v := sprintf("%s.%s", [x, y])
}


#
# Inputs
#

sdwan_version_train := get_version_train(input.controllers.infra.sw_version)
infra := input.controllers.infra.provider
vmanage_accepted_types := data.instance_type_support_matrix[sdwan_version_train][infra].vmanage
controller_accepted_types := data.instance_type_support_matrix[sdwan_version_train][infra].controllers

contains_vmanage_accepted_types {
    input.controllers.vmanage.infra.instance_type == vmanage_accepted_types[_]
}

contains_vbond_accepted_types {
    input.controllers.vbond.infra.instance_type == controller_accepted_types[_]
}

contains_vsmart_accepted_types {
    input.controllers.vsmart.infra.instance_type == controller_accepted_types[_]
}


#
# Rules
#

# Make sure we're using a supported instance type for vManage for the given SD-WAN version
deny[msg] {
    not contains_vmanage_accepted_types

    msg := sprintf("Instance type '%s' is not supported for vManage %s.x on '%s' infra, please use one of %s",
        [input.controllers.vmanage.infra.instance_type, sdwan_version_train, infra, vmanage_accepted_types])
}

# Make sure we're using a supported instance type for vBond for the given SD-WAN version
deny[msg] {
    not contains_vbond_accepted_types

    msg := sprintf("Instance type '%s' is not supported for vBond %s.x on '%s' infra, please use one of %s",
        [input.controllers.vbond.infra.instance_type, sdwan_version_train, infra, controller_accepted_types])
}

# Make sure we're using a supported instance type for vSmart for the given SD-WAN version
deny[msg] {
    not contains_vsmart_accepted_types

    msg := sprintf("Instance type '%s' is not supported for vSmart %s.x on '%s' infra, please use one of %s",
        [input.controllers.vsmart.infra.instance_type, sdwan_version_train, infra, controller_accepted_types])
}
