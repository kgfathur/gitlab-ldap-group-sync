import ldap
import yaml

config_file = 'config.yaml'
conf = []
with open(config_file, 'r') as file:
    configs = yaml.safe_load_all(file)

    # print(configs)
    for cf in configs:
        # print(cf)
        conf = cf

    print("\n# - - - - - - - - - - - - -")
    print("# - - - - - CONFIG  - - - -")
    print(conf)

try:
  # Open a connection to the server. LDAP url.
  # No need to specify if port is 389
  ldap_url = "ldap://{}:{}".format(conf['config']['ldap']['host'], conf['config']['ldap']['port'])
  bind_dn = conf['config']['ldap']['bind_dn']
  bind_pass = conf['config']['ldap']['bind_pass']

  print("\n# - - - - - - - - - - - - -")
  print("# - - - - CONNECTION  - - -")
  print("Connecting to: {}".format(ldap_url))
  ldap_con = ldap.initialize(ldap_url)
  # l = ldap.initialize
  # If any other port, Use
  # l = ldap.open("ldap.example.com:PORT")

  ## searching doesn't require a bind in LDAP V3.
except ldap.LDAPError as e:
  print("Error connecting:")
  print(e)


# Bind to the server
ldap_con.protocol_version = ldap.VERSION3
ldap_con.simple_bind_s(bind_dn, bind_pass)  # myldap.simple_bind_s() if anonymous binding is desired

## The next lines will also need to be changed to accroding to the search requirements
# and the ldap directory structure.
# For this example, lets use
base_dn = conf['config']['ldap']['base_dn']
# SCOPE_ONELEVEL to search for immediate children
# ldap.SCOPE_SUBTREE to search the object and all its descendants.
search_scope = ldap.SCOPE_SUBTREE
## retrieve specified attributes.
# retrieve_attributes = ['dn', 'mail']
# To retrieve all attributes, Use
# retrieve_attributes = None
retrieve_attributes = ['sAMAccountName', 'member']
# retrieve_attributes = ['cn', 'sAMAccountName', 'userPrincipalName', 'memberOf']
# search_filter = "(&(ObjectCategory=Person)(objectclass=User))"
search_filter = conf['config']['ldap']['filter']

try:
  ldap_search = ldap_con.search(base_dn, search_scope, search_filter, retrieve_attributes)
  # result_status, result_data = ldap_con.result(ldap_search, 0)
  # print(result_status)
  # print(result_data)
  # for data in result_data:
  #    print(data)

  print("\n# - - - - - - - - - - - - -")
  print("# - - - - - RESULT  - - - -")
  result_set = []
  while True:
    result_status, result_data = ldap_con.result(ldap_search, 0)
    if result_data == []:
        break
    else:
        if result_status == ldap.RES_SEARCH_ENTRY:
            # print(result_data[0])
            # print(result_data[0][1]['cn'][0].decode('utf-8'))
            print(result_data[0])
            # print(result_data)
            result_set.append(result_data[0])
  
  print("# - - - -")
  # print(result_set)

except ldap.LDAPError as e:
  print(e)

# Unbind from server
ldap_con.unbind_s()