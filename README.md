Habitat
=========

This role helps with the following items:
  - Installing Habitat
  - Opening Habitat tcp/udp ports using iptables or firewalld
  - Configuring the Habitat supervisor to run using initd or systemd
  - Installing Habitat packages
  - Loading Habitat packages to start on Supervisor start

Requirements
------------

easy_install (to get requests), curl required on nodes

Role Variables
--------------

service_manager: systemd|init
habitat_gossip_port: 9631 
habitat_http_port: 9638

Dependencies
------------

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - role: habitat
             __habitat:
               core/prometheus:
                 group: monitoring
                 bind: prom:prometheus.monitoring
                 topology: leader
                 channel: unstable

License
-------

BSD

Author Information
------------------

james.sewell@jirotech.com
