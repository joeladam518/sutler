#!/usr/bin/env bash

# Variables
CWD="$(pwd)"
script_dir="$(cd "$(dirname "$0")" >/dev/null 2>&1 && pwd -P)"
bin_dir="$(cd "${script_dir}/../bin" >/dev/null 2>&1 && pwd -P)"
platform="debian"

# Option variables
testmode="0"
verbosity="0"

# Functions
show_help() {
cat << EOF
Usage: ${0##*/} [-htv] [PROVISION_TYPE]...
    -h      Display this help and exit.
    -t      Testing mode. Just echo it.
    -p      Platoform. Defualts to "debian".
    -v      Verbose mode. Can be used multiple times for increased verbosity.
EOF
}

invalid_option_message() {
    cmsg -r "${0##*/} invalid option: -${1}\n" 1>&2
    show_help
    exit 1
}

invalid_provision_type_message() {
    cmsg -r "${0##*/} invalid provision type \"${1}\"\n" 1>&2
    exit 1
}

# echo "Platform:   ${platform}"
# echo "Script Dir: ${script_dir}"
# echo "Bin Dir:    ${bin_dir}"

# Add the current bin dir to path if it's not there
if [[ ! "$PATH" =~ (^|:)"$bin_dir"(:|$) ]]; then
    export PATH="${PATH}:${bin_dir}"
fi

# Check if the user is running this script as root.
if [ $(id -u) -ne "0" ]; then
    cmsg -y "This install script needs root privileges to do it's job." 1>&2
    exit 1
fi

# Parse the options for this script
while getopts ":hp:tv" opt; do
    case "${opt}" in
        h)  show_help; exit 0                ;;
        p)  platform="${OPTARG,,}"           ;;
        t)  testmode="1"                     ;;
        v)  verbosity=$(($verbosity+1))      ;;
        \?) invalid_option_message "$OPTARG" ;;
    esac
done
shift $((OPTIND-1))

# validate the platform chosen
case "$platform" in
    debian|ubuntu|rpi)
        # Do nothing
        ;;
    *)
        cmsg -r "Invaild platform \"${platform}\"." 1>&2
        exit 1
        ;;
esac

# Input Variables
provision_type=${1}

# Parse the provision type
provision_script_path=""
case "${provision_type}" in
    desktop) provision_script_path="${script_dir}/desktop.sh" ;;
    lamp)    provision_script_path="${script_dir}/lamp.sh"    ;; 
    lemp)    provision_script_path="${script_dir}/lemp.sh"    ;;
    mqtt)    provision_script_path="${script_dir}/mqtt.sh"    ;;
    \?)      invalid_provision_type_message "$OPTARG"         ;;
esac

if ! ([ -n "$provision_script_path" ] && [ -f "$provision_script_path" ]); then
    cmsg -r "Can not provision a ${provision_type} machine. No provisioning script exists." 1>&2
    exit 1
fi

cmsg -c "I will now start provisioning your ${provision_type} ${platform^} machine."

if [ $testmode = "1" ]; then
    cmsg -a "           CWD: ${CWD}"
    cmsg -a "    script dir: ${script_dir}"
    cmsg -a "       bin dir: ${bin_dir}"
    cmsg -a "      platform: ${platform}"
    cmsg -a "      testmode: ${testmode}"
    cmsg -a "       verbose: ${verbosity}"
    cmsg -a "          type: ${provision_type}"
    cmsg
fi

apt-update-upgrade

source "$provision_script_path"

exit
