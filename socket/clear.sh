#!/bin/bash

mysql -u root -p765885195 < hp.sql 2>/dev/null

echo "成功重置数据库"
