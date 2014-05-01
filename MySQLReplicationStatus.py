#!/usr/bin/env python

import re
import commands

SLAVE_IO = "cat /tmp/slave.status | grep Slave_IO_Running | cut -d ':' -f 2"
SLAVE_SQL = "cat /tmp/slave.status | grep Slave_SQL_Running | cut -d ':' -f 2"
SECS_BEHIND = "cat /tmp/slave.status | grep Seconds_Behind_Master | cut -d ':' -f 2"
OK = 0
ERR = 1
SECS_BEHIND_ERR = -1

class MysqlSlaveMonitor:
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

        if self.agent_config is None:
          self.set_default_config()

        if ('mysql_status' not in self.agent_config):
          self.set_default_config()

    def set_default_config(self):
        self.agent_config = {}
        self.agent_config['mysql_status'] = {'user': 'root', 'password': ''}


    def run(self):
        stats = {}
        stats['status'] = OK
        # generate the status
        user = self.agent_config['mysql']['user']
        password = self.agent_config['mysql']['password']
        command = "mysql -u%(user) -p%(password) -e 'SHOW SLAVE STATUS\G' > /tmp/slave.status" %  locals()
        commands.getoutput(command)
        slave_io_status = commands.getoutput(SLAVE_IO).strip()
        slave_sql_status = commands.getoutput(SLAVE_SQL).strip()
        slave_secs_behind = commands.getoutput(SECS_BEHIND).strip()

        if slave_io_status != 'Yes':
            stats['status'] = ERR
        elif slave_sql_status != 'Yes':
            stats['status'] = ERR

        if slave_secs_behind == 'NULL' :
            stats['seconds_behind_master'] = SECS_BEHIND_ERR
            stats['status'] = ERR
        else:
            stats['seconds_behind_master'] = int(slave_secs_behind)

        return stats

if __name__ == '__main__':
    mysql_slave = MysqlSlaveMonitor(None, None, None)
    print mysql_slave.run()
