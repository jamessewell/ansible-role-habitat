#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule

def install_habitat(module):
    depot_url = ''
    version = ''

    if module.params['depot_url']:
        depot_url='HAB_DEPOT_URL=%s' % (module.params['depot_url'])

    if module.params['version']:
        version='-v %s' % (module.params['depot_url'])

    cmd = "curl %s | %s bash -s -- %s -c %s" % (module.params['install_url'], depot_url, version, module.params['channel'])
        
    try:
        rc, stdout, stderr = module.run_command(cmd, check_rc=True, use_unsafe_shell=True)
    except: 
        module.fail_json(msg="Error with downloading habitat, check channel and version are correct")
    return True

def main():
    module = AnsibleModule(
        argument_spec   = dict(
            state       = dict(default="install", choices=["install", "upgrade"]),
            install_url = dict(default='https://raw.githubusercontent.com/habitat-sh/habitat/master/components/hab/install.sh', type='str'),
            depot_url   = dict(default=None, type='str'),
            version     = dict(default=None, type='str'),
            channel     = dict(default='stable', choices=['stable', 'unstable'])
        ),
        required_one_of=[['state']],
    )

    global HABITAT_PATH
    HABITAT_PATH = module.get_bin_path('hab', required=False)

    p = module.params
    changed = False

    # There isn't any difference between an upgrade and an install, we just don't
    # install if the binary exists
    # This insn't great as the only way to change version etc.. is to upgrade
    if not HABITAT_PATH and p['state'] == 'install':
        install_habitat(module) 
        module.exit_json(changed=True, msg='Installed Habitat')

    if p['state'] == 'upgrade':
        install_habitat(module) 
        module.exit_json(changed=True, msg='Upgraded Habitat')
    
    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
