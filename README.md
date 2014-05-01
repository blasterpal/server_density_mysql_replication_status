#MySqlReplicationStatus Server Density Plugin

Tested and simple MySQL replication status Server Density plugin that uses `mysql` client and the shell.

#Metrics

The plugin will report two metrics, `seconds_behind_master` and `status`. 

## 'seconds_behind_master' 

This metric is a good indication of how healthy your replication is AND if it has failed. If the replication has failed, usually the `Seconds_Behind_Master` will be `NULL`. This metric reports that as `-1`.

## 'status'

The second metric is informative based on whether `Slave_IO_Running` or `Slave_SQL_Running` report 'Yes'.


Both of these metrics allows you to easily set thresholds in Server Density to alert if the slave is behind OR if it stops. 

##Assumptions

* Requires `mysql` in `$PATH`
* You must set the user and password in your server density config file. This user must have SUPER or REPLICATION CLIENT privilege (so yes this script presumes a high level of access, but it runs on the DB server directly anyway).
* It can write a temp file to `/tmp/slave.status`

##Installation

* Copy `MySQLReplicationStatus.py` plugin to your `sd-agent` plugins folder (`/usr/bin/sd-agent/plugins`). Create the plugins folder if it doesn't exist.

* Add `mysql_status` section to your Server Density config.

    [mysql_status]
    user: 'replication'
    password: 'password1'

* Restart the agent.


