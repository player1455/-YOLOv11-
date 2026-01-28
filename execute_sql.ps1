# MySQL连接配置
$mysqlServer = "localhost"
$mysqlUser = "root"
$mysqlPassword = "123456"
$mysqlDatabase = "yolo"

# 连接到MySQL并执行SQL命令
$mysqlPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$sqlFile = "D:\codde\python\-YOLOv11-\add_drone.sql"

# 执行MySQL命令
& $mysqlPath -h $mysqlServer -u $mysqlUser -p$mysqlPassword $mysqlDatabase < $sqlFile

Write-Host "执行完成"
