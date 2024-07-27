#!/bin/bash

# 创建SSH Key
if [ -f ~/.ssh/id_rsa ]; then
    echo "SSH Key已经存在"
else
    echo "创建SSH Key..."
    ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -N ""
fi

# 授权密钥
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# 修改SSH相关配置
sudo sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config

# 重启SSH服务
sudo systemctl restart sshd

# 输出生成的私钥
echo "您的SSH Key为，请牢记！"
cat ~/.ssh/id_rsa
