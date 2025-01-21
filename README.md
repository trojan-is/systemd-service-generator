# systemd-service-generator

_Description:_

This playbook will prepare linux `systemd` services as per `systemd_services` <br>
vars and install neccesary packages from `packages` dictionary. <br>

_Available tags and Extra variables:_

```yaml
Tags: NA
Extra_vars:
  full_init: false # Default: false
                   # If `true` the playbook will trigger .
                   # `init -> pre_shell_commands` and `init -> post_shell_commands` command list.
                   # It will be usefull in case of fresh installaion.
                   # NEVER use this variable if for already initialised services because
                   # you may pottentilally affect the runtime
  ansible_call:    # Default: name: "", init: false
    name: ""       # Will be usefull if we need add new systemd service
    init: false    # and initialise it (`init -> pre_shell_commands` and `init -> post_shell_commands` )
                   # without affecting rest services
```

_Playbook_goal:_

Configure `postfix + dovecot` services with side services <br>
like `opendkim, opendmarc, fail2ban, postgrey`

__!!! IT will NOT configure the mail accounts (/etc/postfix/virtual) and SSL part__

_Links_

Special thanks to [linuxbabe.com](https://www.linuxbabe.com) for giving such a fulfilled tutorials!

- https://www.postfix.org/documentation.html
- https://www.postfix.org/postconf.5.html
- https://www.linuxbabe.com/mail-server/build-email-server-from-scratch-debian-postfix-smtp
- https://www.linuxbabe.com/mail-server/block-email-spam-postfix