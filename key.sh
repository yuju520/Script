#!/bin/bash

# 创建SSH Key
if [! -f ~/.ssh/id_rsa ]; then
    echo "创建SSH Key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -q -N ""
fi

# 授权密钥
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# 修改SSH相关配置
sudo sed -i '/^#\?\(PubkeyAuthentication\s*\).*$/\1yes/' /etc/ssh/sshd_config
sudo sed -i '/^#\?\(PasswordAuthentication\s*\).*$/\1no/' /etc/ssh/sshd_config
sudo sed -i '/^#\?\(ChallengeResponseAuthentication\s*\).*$/\1no/' /etc/ssh/sshd_config

# 重启SSH服务
sudo systemctl restart sshd

# 输出生成的私钥
cat ~/.ssh/id_rsa
