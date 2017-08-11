#!/usr/bin/pythoN
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule  

try:
    import requests
    HAS_REQUESTS_MODULE = True
except ModuleNotFoundError:
    HAS_REQUESTS_MODULE = False

def check_service_loaded(module):
    try:
        service =  requests.get('http://127.0.0.1:9631/services/%s/%s' %
            (module.params['name'], module.params['group']))
    except:
        module.fail_json(msg="Habitat Supervisor is not running on port 9631")

    if service.status_code != 200:
        return False

    try:
        return service.json()['start_style'] == "Persistent"
    except:
        return False


def construct_args(module):
    args = []
    if module.params['application']:
        args.append('--aplication %s' % module.params['application'])

    if module.params['bind']:
        args.append('--bind "%s"' % module.params['bind'])

    if module.params['channel']:
        args.append('--channel %s' % module.params['channel'])

    if module.params['url']:
        args.append('--url %s' % module.params['url'])

    if module.params['group']:
        args.append('--group %s' % module.params['group'])

    if module.params['override_name']:
        args.append('--override-name %s' % module.params['override_name'])

    if module.params['strategy']:
        args.append('--strategy %s' % module.params['strategy'])

    if module.params['topology']:
        args.append('--topology %s' % module.params['topology'])

    return args

def load_service(module):
    cmd = "%s sup load --no-color %s/%s %s" % (HABITAT_PATH, module.params['origin'], module.params['name'], ' '.join(construct_args(module)))

    try:
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)
    except:
        module.fail_json(msg="Error with loading service %s/%s" %  (module.params['origin'], module.params['name']))


    module.exit_json(changed=True, msg="Habitat service %s/%s loaded" %  (module.params['origin'], module.params['name']),
                     rc=rc, stdout=stdout, stderr=stderr)

def unload_service(module):
    cmd = "%s sup unload --no-color %s/%s" % (HABITAT_PATH,  module.params['origin'], module.params['name'])

    try:
        rc, stdout, stderr = module.run_command(cmd, check_rc=True)
    except:
        module.fail_json(msg="Error with unloading service %s/%s" %  (module.params['origin'], module.params['name']))

    module.exit_json(changed=True, msg="Habitat service %s/%s unloaded" % (module.params['origin'], module.params['name']),
                     rc=rc, stdout=stdout, stderr=stderr)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name          = dict(type='str'),
            origin        = dict(default='core', type='str'),
            state         = dict(default="loaded", choices=["loaded", "unloaded"]),
            application   = dict(default=None, type='str'),
            bind          = dict(default=None, type='str'),
            channel       = dict(default=None, choices=[None, 'stable', 'unstable']),
            url           = dict(default=None, type='str'),
            environment   = dict(default=None, type='str'),
            group         = dict(default='default'),
            override_name = dict(default=None, type='str'),
            strategy      = dict(default=None, choices=[None, 'none', 'at-once', 'rolling']),
            topology      = dict(default=None, choices=[None, 'standalone', 'leader'])
        ),
        required_one_of=[['name']],
    )

    if not HAS_REQUESTS_MODULE:
        module.fail_json(msg="requests Python library is required")

    global HABITAT_PATH
    HABITAT_PATH = module.get_bin_path('hab', required=False)

    changed = False

    loaded = check_service_loaded(module)

    if module.params['state'] == 'loaded' and not loaded:
        load_service(module) 
        # Never reached, function will halt module

    if module.params['state'] == 'unloaded' and loaded:
        unload_service(module) 
        # Never reached, function will halt module

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
