#!/usr/bin/env bash
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.
#
# Bash script to install the Oracle Cloud Infrastructure CLI
# Example invocation: bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
#
# Use --help to show a help message for this script and its parameters and exit.
#
# The order of precedence in which this scripts applies input parameters is as follows:
#           individual params > accept_all_defaults > interactive inputs
#
SHELL_INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh"
INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/oracle/oci-cli/v2.6.12/scripts/install/install.py"
FALLBACK_INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/oracle/oci-cli/v2.6.11/scripts/install/install.py"
_TTY=/dev/tty

# Below is the usage text to be printed when --help is invoked on this script.
usage="$(basename "$0") [--help] [--accept-all-defaults] [--python-install-location directory_name] [--optional-features feature1,feature2]
        -- Bash script to install the Oracle Cloud Infrastructure CLI. The
           script when run without any options runs in interactive mode
           requesting for user inputs.

The following options are available:
    --accept-all-defaults
        When specified, skips all interactive prompts by selecting the default
        response.  This is a non-interactive mode which can be used in conjunction
        with other parameters that follow.
    --python-install-location
        Optionally specifies where to install python on systems where it is
        not present. This must be an absolute path and it will be created if
        it does not exist. This value will only be used on systems where a
        valid version of Python is not present on the system PATH.
    --optional-features
        This input param is used to specify any optional features
        that need to be installed as part of OCI CLI install .e.g. to run
        dbaas script 'create_backup_from_onprem', users need to install
        optional 'db' feature which will install dependent cxOracle package.
    --install-dir
        This input parameter allows the user to specify the directory where
        CLI installation is done.
    --exec-dir
        This input parameter allows the user to specify the directory where CLI executable is stored.
    --update-path-and-enable-tab-completion
        If this flag is specified, the PATH environment variable is updated to
        include CLI executable and tab auto completion of CLI commands is enabled.
        It does require rc file path in *NIX systems which can be either given
        interactively or using the --rc-file-path option.
    --rc-file-path
        This input param is used in *NIX systems to update the corresponding shell rc file with command
        auto completion and modification to PATH environment variable with CLI executable path. It
        requires shell's rc file path. e.g. ~/.bashrc. Ideally, should be used with the
        --update-path-and-enable-tab-completion option.
    --oci-cli-version
        The version of CLI to install, e.g. 2.5.12. The default is the latest from pypi.
    --help
        show this help text and exit.

The order of precedence in which this scripts applies input parameters is as follows:
individual params > accept_all_defaults > interactive inputs"

# detect if the script is able to prompt for user input from stdin
# if it is being run by piping the script content into bash (cat install.sh | bash) prompts will fail
# (-t fd True if file descriptor fd is open and refers to a terminal)
if ! [ -t 0 ]; then
    echo "WARNING: Some interactive prompts may not function correctly if this script is piped into bash (e.g. 'curl \"$SHELL_INSTALL_SCRIPT_URL\" | bash)'"
    echo "WARNING: Script should either be downloaded and invoked directly, or be run with the following command: bash -c \"\$(curl -L $SHELL_INSTALL_SCRIPT_URL)\""
fi

# Initialize install args. Populate it with command line arguments
install_args=""
# parse script arguments
while [[ $# -gt 0 ]];do
key="$1"

# Rules for local vs. remote install.py:
# This is useful for testing specific versions of the installer.
# 1) if we have --use-local-cli-installer, then it will use a local install.py.
#
# These are useful for the full-install zip bundle install.
# 2) If we have a whl file, cli-deps directory and local install.py, use the local install.py.
# 3) If we have --oci-cli-version with a "preview" version and we have a local install.py, use local install.py.
#
# This is what most customers will end up doing.
# 4) Otherwise download and use the remote install.py.
case $key in
    --python-install-location)
    PYTHON_INSTALL_LOCATION="$2"
    shift # past argument
    shift # past value
    ;;
    --accept-all-defaults)
    ACCEPT_ALL_DEFAULTS=true
    install_args="$install_args --accept-all-defaults"
    shift # past argument
    ;;
    --install-dir)
    CLI_INSTALL_DIR="$2"
    install_args="$install_args --install-dir $CLI_INSTALL_DIR"
    shift # past argument
    shift # past value
    ;;
    --exec-dir)
    CLI_EXECUTABLE_DIR="$2"
    install_args="$install_args --exec-dir $CLI_EXECUTABLE_DIR"
    shift # past argument
    shift # past value
    ;;
    --update-path-and-enable-tab-completion)
    install_args="$install_args --update-path-and-enable-tab-completion"
    shift # past argument
    ;;
    --rc-file-path)
    RC_FILE_PATH="$2"
    install_args="$install_args --rc-file-path $RC_FILE_PATH"
    shift # past argument
    shift # past value
    ;;
    --optional-features)
    OPTIONAL_PACKAGE_NAME="$2"
    install_args="$install_args --optional-features $OPTIONAL_PACKAGE_NAME"
    shift # past argument
    shift # past value
    ;;

    # For Internal Use: This is helpful for doing image testing installs.
    # The --use-local-cli-installer option forces use of a local version of install.py rather than downloading it from GitHub.
    # Even without this option specified, install.sh may still prefer local over remote based on
    # implicit rules for full install zip bundles.
    --use-local-cli-installer)
    base=$(basename $0)
    script_dir=$(echo $0 | sed -e "s/$base//g")
    cd ${script_dir}
    if [ -f ./install.py ];then
        install_script="./install.py"
    else
        echo "install.py script could not be found."
        exit 1
    fi
    shift # past argument
    ;;

    # When oci-cli-version is used with a remote install.py, it retrieves a specific version of install.py from GitHub.
    # Also when a remote install.py is being used, it tells install.py which oci-cli version to get from pypi.
    # When oci-cli-version is used with --use-local-cli-installer or an implicit full zip bundle install,
    # it "tells" install.py which version of the oci_cli whl file to use.
    # If we have a "preview" version and local install.py, use the local install.py.
    --oci-cli-version)
    version="$2"
    install_args="$install_args --oci-cli-version $version"
    if [[ $version == *"preview"* ]]; then
        if [ -f ./install.py ];then
            install_script="./install.py"
        fi
    else
        INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/oracle/oci-cli/v${version}/scripts/install/install.py"
    fi
    shift # past argument
    shift # past value
    ;;
    --dry-run)
    install_args="$install_args --dry-run"
    shift # past argument
    ;;
    --verify-native-dependencies)
    install_args="$install_args --verify-native-dependencies"
    shift # past argument
    ;;
    # Help text for this script. This option takes precedence over all other options
    --help|-h)
    echo "$usage"
    exit 0
    ;;
    *)    # unknown option
    echo "Failed to run install script. Unrecognized argument: $1"
    exit 1
    ;;
esac
done

# Some implicit logic to handle full-install packages such as preview installs.
ls ./oci_cli*.whl 2> /dev/null
if [ $? -eq 0 ];then
    if [[ -f ./install.py ]] && [[ -d ./cli-deps ]];then
        install_script="./install.py"
    fi
fi

yum_opts=""
apt_get_opts=""
if [ "$ACCEPT_ALL_DEFAULTS" = true ]; then
    yum_opts="-y"
    apt_get_opts="-y"
    echo "Running with --accept-all-defaults"
else
    echo "
    ******************************************************************************
    You have started the OCI CLI Installer in interactive mode. If you do not wish
    to run this in interactive mode, please include the --accept-all-defaults option.
    If you have the script locally and would like to know more about
    input options for this script, then you can run:
    ./install.sh -h
    If you would like to know more about input options for this script, refer to:
    https://github.com/oracle/oci-cli/blob/master/scripts/install/README.rst
    ******************************************************************************"
fi


if [ "${install_script}" == "" ];then
    install_script=$(mktemp -t oci_cli_install_tmp_XXXX) || exit
    echo "Downloading Oracle Cloud Infrastructure CLI install script from $INSTALL_SCRIPT_URL to $install_script."
    curl -# -f $INSTALL_SCRIPT_URL > $install_script
    if [ $? -ne 0 ]; then
        INSTALL_SCRIPT_URL=$FALLBACK_INSTALL_SCRIPT_URL
        curl -# -f $INSTALL_SCRIPT_URL > $install_script || exit
        echo "Falling back to previous install.py script URL - $INSTALL_SCRIPT_URL"
    fi
fi

# use default system executable on path unless we have to install one below
python_exe=python

# if python is not installed or is less than the required version, then install Python
need_to_install_python=true
command -v python >/dev/null 2>&1
if [ $? -eq 0 ]; then
    # python is installed so check if the version is valid
    # this python command returns an exit code of 0 if the system version is sufficient, and 1 if it is not
    python -c "import sys; v = sys.version_info; valid = v >= (2, 7, 5) if v[0] == 2 else v >= (3, 5, 0); sys.exit(0) if valid else sys.exit(1)"
    if [ $? -eq 0 ]; then
        # if python is installed and meets the version requirements then we dont need to install it
        need_to_install_python=false
    else
        echo "System version of Python must be either a Python 2 version >= 2.7.5 or a Python 3 version >= 3.5.0."
    fi
else
    echo "Python not found on system PATH"
fi

# some OSes have python3 as a command but not 'python' (example: Ubuntu 16.04)
# if both python and python3 exist and are a sufficiently recent version, we will prefer python3
command -v python3 >/dev/null 2>&1
if [ $? -eq 0 ]; then
    # python is installed so check if the version is valid
    # this python command returns an exit code of 0 if the system version is sufficient, and 1 if it is not
    python3 -c "import sys; v = sys.version_info; valid = v >= (2, 7, 5) if v[0] == 2 else v >= (3, 5, 0); sys.exit(0) if valid else sys.exit(1)"
    if [ $? -eq 0 ]; then
        python_exe=python3
        # if python is installed and meets the version requirements then we dont need to install it
        need_to_install_python=false
    else
        echo "System version of Python must be either a Python 2 version >= 2.7.5 or a Python 3 version >= 3.5.0."
    fi
else
    echo "Python3 not found on system PATH"
fi

sudo_cmd="sudo"
if [ "$(whoami)" == "root" ];then
    sudo_cmd=""
fi

if [ "$need_to_install_python" = true ]; then
    # Many docker containers won't have sudo installed since they are already run as root.
    if command -v yum
    then
        echo "Attempting to install Python."
        $sudo_cmd yum $yum_opts check-update
        $sudo_cmd yum $yum_opts install gcc libffi-devel python-devel openssl-devel
        $sudo_cmd yum $yum_opts install make
        if [ $? -ne 0 ]; then
            echo "ERROR: Required native dependencies were not installed, exiting install script. If you did not receive a prompt to install native dependencies please ensure you are not piping the script into bash and are instead using the following command: bash -c \"\$(curl -L $SHELL_INSTALL_SCRIPT_URL)\""
            exit 1
        fi
        curl --tlsv1.2 -O https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
        tar -xvzf Python-3.6.5.tgz
        cd Python-3.6.5
        python_exe=/usr/local/bin/python3.6
        if [ -n "$PYTHON_INSTALL_LOCATION" ]; then
            configure_args="prefix=$PYTHON_INSTALL_LOCATION"
            python_exe="$PYTHON_INSTALL_LOCATION/bin/python3.6"
        fi
        ./configure $configure_args
        make
        $sudo_cmd make install
        cd ..
    elif command -v apt-get
    then
        echo "Attempting to install Python."
        $sudo_cmd apt-get $apt_get_opts update
        $sudo_cmd apt-get $apt_get_opts install python3-pip
        if [ $? -ne 0 ]; then
            echo "ERROR: Python was not installed, exiting install script. If you did not receive a prompt to install python please ensure you are not piping the script into bash and are instead using the following command: bash -c \"\$(curl -L $SHELL_INSTALL_SCRIPT_URL)\""
            exit 1
        fi
        python_exe=python3
    else
        echo "ERROR: Could not install Python based on operating system. Please install Python manually and re-run this script."
        exit 1
    fi
fi

# In the future native dependency setup will be done in this script.
cat /etc/os-release | grep "Ubuntu 18"
if [ "$?" = "0" ];then
    $sudo_cmd apt-get $apt_get_opts update
    $sudo_cmd apt-get $apt_get_opts install python3-distutils
fi

chmod 775 $install_script
echo "Running install script."
echo "$python_exe $install_script $install_args"
if [ "${ACCEPT_ALL_DEFAULTS}" == "true" ];then
    # By removing the tty requirement, users will be able to install non-interactively over ssh
    # and in docker containers more easily.
    $python_exe $install_script $install_args
else
    $python_exe $install_script $install_args < $_TTY
fi
