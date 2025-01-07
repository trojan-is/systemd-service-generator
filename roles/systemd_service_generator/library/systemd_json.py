#!/usr/bin/python ?????

# Copyright: (c) 2025, Vladimir Glazunov <trojanis@itsfine.cloud>
# GNU General Public License v3.0+ 
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: systemd_json

short_description: systemd show -> JSON output

description: This is module transform "systemd show `service_name`"
into JSON format.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.errors import AnsibleError
import subprocess, json, pprint

def run_module():
    module_args = dict(
        name=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        output=list(),
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    cmd = ["systemctl show --no-page {}".format(module.params['name'])]
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        output, errors = proc.communicate(timeout=10)
    except subprocess.SubprocessError as errors:
        proc.kill()
        raise AnsibleError("Error: {}".format(errors))
    
    output_pretty = output.decode().split('\n')
    pprint.pprint(output_pretty)
    exit(0)
    j = dict()
    result['output'].append(
        dict(
            map(
                lambda x:
                {
                    x[0]: x[1]
                }, output_pretty.split('=')
            )
        )
    )

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['output'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
