Vagrant.configure("2") do |config|
 config.vm.box = "hashicorp/bionic64"
 config.vm.network "forwarded_port", guest: 5000, host: 5000
    config.vm.provision "shell",privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y build-essential
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init --path)"' >> ~/.profile
    source ~/.profile
    pyenv install 3.8.5
	pyenv global 3.8.5
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    SHELL
    config.trigger.after :up do |trigger|
        trigger.name = "Launching App"
        trigger.info = "Running the TODO app setup script"
        trigger.run_remote = {privileged: false, inline: "
        # Install dependencies and launch
        # <your script here>
        cd /vagrant
        poetry install
        nohup poetry run flask run --host 0.0.0.0 > logs.txt 2>&1 &
        "}
    end
end