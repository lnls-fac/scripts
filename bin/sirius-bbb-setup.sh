#!/bin/bash
# Execute as sudo

# Functions
function get_hash {
    if [ -f "$1/.git/refs/heads/master" ]; then 
        cat "$1/.git/refs/heads/master"
    else 
        echo '-1'
    fi
}

home='/home/fac'


if [ ! -f /usr/local/bin/python3.6 ]; then
    echo 'Python 3.6 not found'
    exit 1
fi

# Create python-sirius symbolic link
if [ ! -L /usr/bin/python-sirius ]; then
    echo 'python-sirius symbolic link not found'
    ln -s /usr/local/bin/python3.6 /usr/bin/python-sirius
fi

# Create fac_files folder
if [ ! -d '/home/fac_files' ]; then
    echo 'Creating fac_files folder'
    mkdir /home/fac_files
fi

# Create lnls-sirius folder
if [ ! -d '/home/fac_files/lnls-sirius' ]; then
    echo 'Creating lnls-sirius folder'
    mkdir /home/fac_files/lnls-sirius
fi

# Create /usr/local/etc
if [ ! -d "/usr/local/etc" ]; then
    mkdir /usr/local/etc
fi

if [ ! -L "/opt/epics" -a -d "/opt/epics-R3.15.5/" ]; then
    echo 'Creating /opt/epics symobolic link'
    ln -s /opt/epics-R3.15.5/ /opt/epics
fi

alias='10.0.7.55 sirius-consts.lnls.br'
# Config hosts
if ! grep -Fxq "$alias" /etc/hosts; then
    echo 'Appending aliases to /etc/hosts'
    echo '# Sirius constants server alias' >> /etc/hosts
    echo "$alias" >> /etc/hosts
fi

# Get bashrc sirius
if [ ! -f '/usr/local/etc/bashrc-sirius' ]; then
    cd $home
    if [ ! -d "$home/scripts" ]; then
        echo 'Cloning lnls-fac scripts repository'
        git clone https://github.com/lnls-fac/scripts.git &> /dev/null

        if [ -f "$home/scripts/etc/bashrc-sirius" ]; then
            cp $home/scripts/etc/bashrc-sirius /usr/local/etc/bashrc-sirius
            sed -i -e '5i #Sirius bashrc' $home/.bashrc
            sed -i -e '6i SIRIUSBASHRC=/usr/local/etc/bashrc-sirius' $home/.bashrc
            sed -i -e '7i if [ -f "$SIRIUSBASHRC" ] ; then' $home/.bashrc
            sed -i -e '8i \ \ \ \ source "$SIRIUSBASHRC"' $home/.bashrc
            sed -i -e '9i fi\n' $home/.bashrc
        fi
    else
        echo 'lnls-fac scripts repository already cloned'
    fi

    rm -r $home/scripts
fi
# Source appended bashrc
sed -i 's/linux-x86_64/linux-arm/g' /usr/local/etc/bashrc-sirius
source $home/.bashrc


# Clone dev-packages and machine-applications
repos=(dev-packages machine-applications pru-serial485)
repos_path=/home/fac_files/lnls-sirius
for repo in ${repos[@]}; do
    cd $repos_path
    if [ ! -d "$repos_path/$repo" ]; then
        echo "Cloning $repo"
        git clone "https://github.com/lnls-sirius/$repo.git" &> /dev/null
        if [ $? ]; then
            echo "$repo cloned"
        else
            echo "Failed to clone $repo"
            exit 1
        fi
    fi
done

chown -R fac /home/fac_files/lnls-sirius

# Install dev-packages
remote="https://github.com/lnls-sirius/dev-packages.git"
repo="/home/fac_files/lnls-sirius/dev-packages"
setup="$repo/siriuspy"
if [ -d $setup ]; then
    package="$remote@$(get_hash $repo)"
    echo -n "Checking if siriuspy is installed: "
    pip3.6 -q freeze | grep $package &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Developing dev-packages"
        cd $setup
        python-sirius setup.py develop &> /dev/null
        if [ $? -eq 0 ]; then
            echo 'dev-packages developed'
        else
            echo 'dev-packages failed to develop'
            exit 1
        fi
    else
        echo 'ok'
    fi
else
    echo "dev-packages not found"
    exit 1
fi

# Install machine applications as-ps package
remote="https://github.com/lnls-sirius/machine-applications.git"
repo="/home/fac_files/lnls-sirius/machine-applications"
setup="$repo/as-ps"
if [ -d $setup ]; then
    package="$remote@$(get_hash $repo)"
    echo -n "Checking if as_ps is installed: "
    pip3.6 -q freeze | grep $package &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Developing machine-applications as-ps package"
        cd $setup
        python-sirius setup.py develop &> /dev/null
        if [ $? -eq 0 ]; then
            echo 'as-ps package developed'
        else
            echo 'as-ps package failed to develop'
            exit 1
        fi
    else
        echo 'ok'
    fi
else
    echo 'machine-application as-ps package not found'
    exit 1
fi

# Develop PRUserial485?

exit 0
