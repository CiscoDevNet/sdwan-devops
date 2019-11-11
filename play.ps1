#! /usr/bin/pwsh
<#
For testing script add "TEST" as an argument to the script. 
For Example:
C:>powershell.exe ./play.ps1 TEST <playbook> <options>
#>

$final_args = $args
if ($args[0] -eq "TEST")
{
    $final_args = @()
    foreach ($arg in $args)
    {
        if ($arg -ne "TEST")
	    {
	    $final_args += $arg
	    }
	}
	$env:ANSIBLE_VAULT_PASSWORD_FILE="AAAAA"
    $env:VIRL_HOST="BBBBB"
    $env:VIRL_USERNAME="CCCCC"
    $env:VIRL_PASSWORD="DDDDD"
    $env:VIRL_LAB="EEEEE"
    $env:VMANAGE_HOST="FFFFF"
    $env:VMANAGE_ORG="GGGGG"
    $env:VMANAGE_USERNAME="HHHHH"
    $env:VMANAGE_PASSWORD="IIIII"
	Write-Host "Below are your testing environment variables"
	gci env:* | sort-object name
}
else
{
    Write-Host "Below are your current environment variables"
	gci env:* | sort-object name
}

$OPTIONS=""

if ($env:ANSIBLE_VAULT_PASSWORD_FILE)
{
$OPTIONS += " --env ANSIBLE_VAULT_PASSWORD_FILE=/tmp/vault.pw -v " + $env:ANSIBLE_VAULT_PASSWORD_FILE + ":/tmp/vault.pw"
}
if ($env:VIRL_HOST)
{
$OPTIONS += " --env VIRL_HOST=" + $env:VIRL_HOST
}
if ($env:VIRL_USERNAME)
{
$OPTIONS += " --env VIRL_USERNAME=" + $env:VIRL_USERNAME
}
if ($env:VIRL_PASSWORD)
{
$OPTIONS += " --env VIRL_PASSWORD=" + $env:VIRL_PASSWORD
}
if ($env:VIRL_LAB)
{
$OPTIONS += " --env VIRL_LAB=" + $env:VIRL_LAB
}
if ($env:VMANAGE_HOST)
{
$OPTIONS += " --env VMANAGE_HOST=" + $env:VMANAGE_HOST
}
if ($env:VMANAGE_ORG)
{
$OPTIONS += " --env VMANAGE_ORG=" + $env:VMANAGE_ORG
}
if ($env:VMANAGE_USERNAME)
{
$OPTIONS += " --env VMANAGE_SESSION=" + $env:VMANAGE_USERNAME
}
if ($env:VMANAGE_PASSWORD)
{
$OPTIONS += " --env VIRL_SESSION=" + $env:VMANAGE_PASSWORD
}
$OPTIONS += " --env ANSIBLE_ROLES_PATH=/ansible/roles"

$DOCKER_CMD="docker run -it --rm -v " + $PSScriptRoot + ":/ansible --env PWD=" + "/ansible" + " --env USER=" + $env:USERNAME + $OPTIONS + " ansible-sdwan ansible-playbook " + $final_args

if ($args[0] -eq "TEST")
{
Write-Host "Below is the resulting ansible command: "
echo $DOCKER_CMD
}
else
{
Write-Host "Executing below docker command: "
echo $DOCKER_CMD
$DOCKER_CMD
}