#
"""
This module is methods for Ixia tester, while will be bound to the RT object from toby init
"""
import ipaddress
import re


def close(self):
    """
    :param self:                RT object
    :return:
    """
    return self.ixiangpf.cleanup_session()


def reboot_port(self, port_list):
    """
    reboot port cpu
    :param self:
    :param port_list:            the tester port_list
    :return:
    """
    port_handle_list = []
    if isinstance(port_list, str):
        ports = []
        ports.append(port_list)
        port_list = ports
    for port in port_list:
        port_handle = self.port_to_handle_map[port]
        port_handle_list.append(port_handle)
    self.ixiangpf.reboot_port_cpu(port_list=port_handle_list)
    self.ixiangpf.interface_config(port_handle=port_handle_list, phy_mode='fiber')


def initialize(self, port_list):
    """
    :param self:                RT object
    :param port_list:           list of RT ports
    :return:
    """
    self.handles = {}
    self.bgp_handle = []
    self.dhcpv4_client_handle = []
    self.dhcpv6_client_handle = []
    self.pppox_client_handle = []
    self.device_group_handle = []
    self.dhcpv4_server_handle = []
    self.dhcpv6_server_handle = []
    self.lac_handle = []
    self.lns_handle = []
    self.l2tp_client_handle = []
    self.l2tp_server_session_handle = []
    self.link_ip_handle = []
    self.link_ipv6_handle = []
    self.link_gre_handle = []
    self.remote_id = {}
    self.circuit_id = {}
    self.interface_id = {}
    self.v6_remote_id = {}
    self.enterprise_id = {}
    self.dhcpv4_index = 0
    self.dhcpv6_index = 0
    self.pppoev4_index = 0
    self.pppoev6_index = 0
    self.traffic_item = []
    self.stream_id = []
    self.igmp_handles = {}
    self.igmp_handle_to_group = {}
    self.mld_handles = {}
    self.mld_handle_to_group = {}
    self.device_to_dhcpv4_index = dict()
    self.device_to_dhcpv6_index = dict()
    self.device_to_pppoe_index = dict()
    self.port_to_dhcp_index = dict()
    self.port_to_pppoe_index = dict()
    self.topology = []
    for port in port_list:
        port_handle = self.port_to_handle_map[port]
        topology_status = self.ixiangpf.topology_config(port_handle=port_handle)
        self.topology.append(topology_status['topology_handle'])
        self.handles[port] = {}
        self.handles[port]['topo'] = topology_status['topology_handle']
        self.handles[port]['device_group_handle'] = []
        self.handles[port]['ethernet_handle'] = []
        self.handles[port]['ipv4_handle'] = []
        self.handles[port]['ipv6_handle'] = []
        self.handles[port]['dhcpv4_client_handle'] = []
        self.handles[port]['dhcpv6_client_handle'] = []
        self.handles[port]['pppox_client_handle'] = []
        self.handles[port]['port_handle'] = self.port_to_handle_map[port]
        self.handles[port]['dhcpv6_over_pppox_handle'] = {}

# def add_chassis_port(self, **kwargs):
#     """
#     #rt = IxiaTester(reset=1, device='10.9.1.102',ixnetwork_tcl_server='10.9.1.101', port_list='12/2 12/3')
#     :param kwargs:
#     :return:
#     """
#     # connect_args = dict()
#     # connect_args['reset'] = '1'
#     # connect_args['device'] = kwargs['device']
#     # connect_args['ixnetwork_tcl_server'] = kwargs['tcl_server']
#     # connect_args['ixnetwork_license_servers'] = kwargs['license_server']
#     # connect_args['ixnetwork_license_type'] = kwargs.get('ixnetwork_license_type', 'mixed')
#     # connect_args['execution_timeout'] = kwargs.get('execution_timeout', '3600')
#
#     port_list = kwargs.get('port_list')
#     print(kwargs)
#     connect_status = self.ixiangpf.connect(**kwargs)
#     if connect_status['status'] != '1':
#         raise Exception("failed to add port {} to chassis".format(port_list))
#     else:
#         self.session_info = connect_status
#         port_handle = connect_status['vport_list'].split(' ')
#         if not isinstance(port_list, list):
#             port_list = kwargs.get('port_list').split(' ')
#         self.port_list = port_list
#         self.port_to_handle_map = dict(zip(port_list, port_handle))
#         self.handle_to_port_map = dict(zip(port_handle, port_list))
#         self.ixiangpf.interface_config(port_handle=port_handle, phy_mode='fiber')
#         self.device_to_dhcpv4_index = dict()
#         self.device_to_dhcpv6_index = dict()
#         self.device_to_pppoe_index = dict()
#         self.port_to_dhcp_index = dict()
#         self.port_to_pppoe_index =dict()
#         self.topology = []
#         ##creating topology for each port
#         for port in port_list:
#             port_handle = self.port_to_handle_map[port]
#             topology_status = self.ixiangpf.topology_config(port_handle=port_handle)
#             self.topology.append(topology_status['topology_handle'])
#             self.handles[port] = {}
#             self.handles[port]['topo'] = topology_status['topology_handle']
#             self.handles[port]['device_group_handle'] = []
#             self.handles[port]['ethernet_handle'] = []
#             self.handles[port]['ipv4_handle'] = []
#             self.handles[port]['ipv6_handle'] = []
#             self.handles[port]['dhcpv4_client_handle'] = []
#             self.handles[port]['dhcpv6_client_handle'] = []
#             self.handles[port]['pppox_client_handle'] = []
#             self.handles[port]['port_handle'] = self.port_to_handle_map[port]
#             self.handles[port]['dhcpv6_over_pppox_handle']={}


def set_protocol_stacking_mode(self, mode='parallel'):
    """
    :param self:                    RT object
    :param mode:                    parallel or sequential, default is sequential
    :return:
    """
    return self.ixiangpf.topology_config(mode='modify', protocol_stacking_mode=mode, topology_handle=self.topology[0])


def set_custom_pattern(self, **kwargs):
    """
    custom pattern for create vlan/svlan
    :param self:            RT object
    :param kwargs:
    start:                  vlan start num
    step:                   vlan step num
    repeat:                 vlan repeat num
    count:                  vlan squence length
    :return:
    multivalue:             multivalue handle for the custom pattern
    """
    _result_ = self.ixiangpf.multivalue_config(
        pattern="custom",
        #nest_step='%s' % ("1"),
        #nest_owner='%s' % (topology_2_handle),
        #nest_enabled='%s' % ("0"),
    )
    multivalue_handle = _result_['multivalue_handle']

    _result_ = self.ixiangpf.multivalue_config(
        multivalue_handle=multivalue_handle,
        custom_start=kwargs.get('start'),
        custom_step="0",
    )

    custom_1_handle = _result_['custom_handle']

    _result_ = self.ixiangpf.multivalue_config(
        custom_handle=custom_1_handle,
        custom_increment_value=kwargs.get('step'),
        custom_increment_count=kwargs.get('count', '4094'),
    )

    increment_1_handle = _result_['increment_handle']

    _result_ = self.ixiangpf.multivalue_config(
        increment_handle=increment_1_handle,
        custom_increment_value="0",
        custom_increment_count=kwargs.get('repeat'),
    )
    #increment_2_handle = _result_['increment_handle']
    return multivalue_handle


def set_v6_option(self, **kwargs):
    """
    dhcpv6 interface_id(option 17) and remote_id (option 38)
    :param self:                    RT object
    :param kwargs:
    handle:                         dhcpv6 device handle
    interface_id:                   interface_id string, if with ? inside it, it means the string will increase based
                                    on the start/step/repeat at that location or default
    interface_id_start:             interface_id_start num
    interface_id_step:              interface_id_step num
    interface_id_repeat:            interface_id_repeat num
    remote_id:                      remote_id string, if with ? inside it, it means the string will increase based on
                                    the start/step/repeat or default
    remote_id_start:                remote_id_start num
    remote_id_step:                 remote_id_step num
    remote_id_repeat:               remote_id_repeat num
    enterprise_id:                  enterprise_id used inside of remote id
    enterprise_id_step:             enterprise_id_step num
    :return:
    status:                         1 or 0
    """
    status = '1'
    if 'handle' in kwargs and 'v6' in kwargs['handle']:
        dhcpv6_handle = kwargs['handle']
        if 'interface_id' in kwargs:
            interface_id = kwargs.get('interface_id')
            if 'interface_id_start' in kwargs:
                start = str(kwargs.get('interface_id_start', '1'))
                step = str(kwargs.get('interface_id_step', '1'))
                repeat = str(kwargs.get('interface_id_repeat', '1'))

                if '?' in interface_id:
                    increment = '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'
                    interface_id = interface_id.replace('?', increment)
                else:
                    interface_id = interface_id + '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'

            if dhcpv6_handle not in self.interface_id:
                _result_ = self.ixiangpf.tlv_config(
                    handle=dhcpv6_handle,
                    mode="create_tlv",
                    tlv_name="""[18] Interface-ID""",
                    tlv_include_in_messages="""kSolicit kRequest kInformReq kRelease kRenew kRebind""",
                    tlv_enable_per_session="1",
                    type_name="Type",
                    type_is_editable="0",
                    type_is_required="1",
                    length_name="Length",
                    length_description="""DHCPv6 client TLV length field.""",
                    length_encoding="decimal",
                    length_size="2",
                    length_value="0",
                    length_is_editable="0",
                    length_is_enabled="1",
                    disable_name_matching="1",
                )
                print(_result_)
                #tlv_1_handle = _result_['tlv_handle']
                value_1_handle = _result_['tlv_value_handle']
                #length_1_handle = _result_['tlv_length_handle']
                type_1_handle = _result_['tlv_type_handle']


                _result_ = self.ixiangpf.multivalue_config(
                    pattern="string",
                    string_pattern=interface_id,
                )
                print(_result_)
                multivalue_4_handle = _result_['multivalue_handle']

                _result_ = self.ixiangpf.tlv_config(
                    handle=value_1_handle,
                    mode="create_field",
                    field_name="Interface-ID",
                    field_encoding="string",
                    field_size="0",
                    field_value=multivalue_4_handle,
                    field_is_enabled="1",
                    field_is_editable="1",
                )
                print(_result_)
                if _result_['status'] != '1':
                    status = '0'
                else:
                    self.interface_id[dhcpv6_handle] = _result_['tlv_field_handle']

                _result_ = self.ixiangpf.tlv_config(
                    handle=type_1_handle,
                    mode="create_field",
                    field_name="Code",
                    field_description="""DHCPv6 client TLV type field.""",
                    field_encoding="decimal",
                    field_size="2",
                    field_value="18",
                    field_is_enabled="1",
                    field_is_editable="0",
                )
                print(_result_)
                #field_2_handle = _result_['tlv_field_handle']
            else:
                _result_ = self.ixiangpf.tlv_config(
                    handle=self.interface_id[dhcpv6_handle],
                    mode="modify",
                    field_name="Interface-ID",
                    field_encoding="string",
                    field_size="0",
                    field_value=interface_id,
                    field_is_enabled="1",
                    field_is_editable="1",
                )
                print(_result_)
                if _result_['status'] != '1':
                    status = '0'
        if 'enterprise_id' in kwargs and dhcpv6_handle in self.enterprise_id:
            enterprise_id = kwargs['enterprise_id']
            enterprise_id_step = kwargs.get('enterprise_id_step', '0')
            _result_ = self.ixiangpf.multivalue_config(
                pattern="counter",
                counter_start=enterprise_id,
                counter_step=enterprise_id_step,
                counter_direction="increment",
            )
            print(_result_)
            multivalue_4_handle = _result_['multivalue_handle']
            _result_ = self.ixiangpf.tlv_config(
                handle=self.enterprise_id[dhcpv6_handle],
                mode="modify",
                field_name="""Enterprise number""",
                #field_description="""The vendor's registered Enterprise Number as registered with IANA.""",
                field_encoding="decimal",
                field_size="4",
                field_value=multivalue_4_handle,
                field_is_enabled="1",
                field_is_editable="1",
            )
            if _result_['status'] != '1':
                status = '0'
            print(_result_)

        if 'v6_remote_id' in kwargs:
            remote_id = kwargs['v6_remote_id']
            if 'v6_remote_id_start' in kwargs:
                start = str(kwargs.get('v6_remote_id_start'))
                step = str(kwargs.get('v6_remote_id_step', '1'))
                repeat = str(kwargs.get('v6_remote_id_repeat', '1'))
                if '?' in remote_id:
                    increment = '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'
                    remote_id = remote_id.replace('?', increment)
                else:
                    remote_id = remote_id + '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'

            if dhcpv6_handle not in self.v6_remote_id:
                _result_ = self.ixiangpf.tlv_config(
                    handle=dhcpv6_handle,
                    mode="create_tlv",
                    tlv_name="""[37] Relay Agent Remote-ID""",
                    tlv_is_enabled="1",
                    tlv_include_in_messages="""kSolicit kRequest kInformReq kRelease kRenew kRebind""",
                    tlv_enable_per_session="1",
                    type_name="Type",
                    type_is_editable="0",
                    type_is_required="1",
                    length_name="Length",
                    length_description="""DHCPv6 client TLV length field.""",
                    length_encoding="decimal",
                    length_size="2",
                    length_value="0",
                    length_is_editable="0",
                    length_is_enabled="1",
                    disable_name_matching="1",
                )

                #tlv_2_handle = _result_['tlv_handle']
                value_2_handle = _result_['tlv_value_handle']
                #length_2_handle = _result_['tlv_length_handle']
                type_2_handle = _result_['tlv_type_handle']

                if 'enterprise_id' in kwargs:
                    enterprise_id = kwargs['enterprise_id']
                    enterprise_id_step = kwargs.get('enterprise_id_step', 0)
                    _result_ = self.ixiangpf.multivalue_config(
                        pattern="counter",
                        counter_start=enterprise_id,
                        counter_step=enterprise_id_step,
                        counter_direction="increment",
                        # nest_step='%s' % ("1"),
                        # nest_owner='%s' % (topology_1_handle),
                        # nest_enabled='%s' % ("0"),
                    )
                    print(_result_)
                    multivalue_4_handle = _result_['multivalue_handle']


                    _result_ = self.ixiangpf.tlv_config(
                        handle=value_2_handle,
                        mode="create_field",
                        field_name="""Enterprise number""",
                        field_description="""The vendor's registered Enterprise Number as registered with IANA.""",
                        field_encoding="decimal",
                        field_size="4",
                        field_value=multivalue_4_handle,
                        field_is_enabled="1",
                        field_is_editable="1",
                    )
                    print(_result_)
                    if _result_['status'] != '1':
                        status = '0'
                    else:
                        self.enterprise_id[dhcpv6_handle] = _result_['tlv_field_handle']


                _result_ = self.ixiangpf.tlv_config(
                    handle=value_2_handle,
                    mode="create_field",
                    field_name="""Remote-ID Byte""",
                    field_description="""The opaque value for the remote-id.""",
                    field_encoding="string",
                    field_size="0",
                    field_value=remote_id,
                    field_is_enabled="1",
                    field_is_editable="1",
                )
                print(_result_)
                if _result_['status'] != '1':
                    status = '0'
                else:
                    self.v6_remote_id[dhcpv6_handle] = _result_['tlv_field_handle']


                _result_ = self.ixiangpf.tlv_config(
                    handle=type_2_handle,
                    mode="create_field",
                    field_name="Code",
                    field_description="""DHCPv6 client TLV type field.""",
                    field_encoding="decimal",
                    field_size="2",
                    field_value="37",
                    field_is_enabled="1",
                    field_is_editable="0",
                )
                print(_result_)
                #field_5_handle = _result_['tlv_field_handle']
            else:
                _result_ = self.ixiangpf.tlv_config(
                    handle=self.v6_remote_id[dhcpv6_handle],
                    mode="modify",
                    field_name="""Remote-ID Byte""",
                    #field_description="""The opaque value for the remote-id.""",
                    field_encoding="string",
                    field_size="0",
                    field_value=remote_id,
                    field_is_enabled="1",
                    field_is_editable="1",
                )
                print(_result_)
    return status


def set_option_82(self, **kwargs):
    """
    this is for dhcpv4 option 82
    :param self:                RT object
    :param kwargs:
    handle:                     dhcpv4 client handle
    circuit_id:                 circuit id string( if with ? with the circuit id, it will replace ? with the increase)
    circuit_id_start:           circuit id start num
    circuit_id_step:            circuit id step num
    circuit_id_repeat:          circuit_id_repeat_num
    remote_id:                  remote id string
    remote_id_start:            remote id start num
    remote_id_step:             remote_id_step num
    remote_id_repeat:           remote_id_repeat num
    :return:
    status:                     1 or 0
    """
    status = '1'
    if 'handle' in kwargs and 'v4' in kwargs.get('handle'):
        handle = kwargs.get('handle')
        if 'circuit_id' in kwargs:
            circuit_id = kwargs.get('circuit_id')
            if 'circuit_id_start' in kwargs:
                start = str(kwargs.get('circuit_id_start'))
                step = str(kwargs.get('circuit_id_step', '1'))
                repeat = str(kwargs.get('circuit_id_repeat', '1'))
                if '?' in circuit_id:
                    increment = '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'
                    circuit_id = circuit_id.replace('?', increment)
                else:
                    circuit_id = circuit_id + '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'
            if handle not in self.circuit_id:
                _result_ = self.ixiangpf.tlv_config(
                    handle=kwargs.get('handle'),
                    mode="create_tlv",
                    tlv_name="""[82] DHCP Relay Agent Information""",
                    tlv_is_enabled="1",
                    tlv_include_in_messages="""kDiscover kRequest""",
                    tlv_enable_per_session="1",
                    type_name="Type",
                    type_is_editable="0",
                    type_is_required="1",
                    length_name="Length",
                    #  length_description="""Dhcp client TLV length field.""",
                    length_encoding="decimal",
                    length_size="1",
                    length_value="0",
                    length_is_editable="0",
                    length_is_enabled="1",
                    disable_name_matching="1",
                )
                if _result_['status'] != '1':
                    status = '0'
                #tlv_1_handle = _result_['tlv_handle']
                value_1_handle = _result_['tlv_value_handle']
                #length_1_handle = _result_['tlv_length_handle']
                #type_1_handle = _result_['tlv_type_handle']
                _result_ = self.ixiangpf.tlv_config(
                    handle=value_1_handle,
                    mode="create_tlv",
                    tlv_name="""[1] Agent Circuit ID""",
                    tlv_is_enabled="1",
                    tlv_enable_per_session="1",
                    type_name="Type",
                    type_is_editable="0",
                    type_is_required="1",
                    length_name="Length",
                    #  length_description="""Dhcp client TLV length field.""",
                    length_encoding="decimal",
                    length_size="1",
                    length_value="0",
                    length_is_editable="0",
                    length_is_enabled="1",
                    disable_name_matching="1",
                )
                if _result_['status'] != '1':
                    print(_result_)
                    status = '0'
                #subTlv_1_handle = _result_['subtlv_handle']
                value_2_handle = _result_['tlv_value_handle']
                #length_2_handle = _result_['tlv_length_handle']
                type_2_handle = _result_['tlv_type_handle']
                _result_ = self.ixiangpf.multivalue_config(
                    pattern="string",
                    string_pattern=circuit_id,
                )
                multivalue_4_handle = _result_['multivalue_handle']

                _result_ = self.ixiangpf.tlv_config(
                    handle=value_2_handle,
                    mode="create_field",
                    field_name="""Circuit ID""",
                    field_value=multivalue_4_handle,
                    field_encoding="string",
                    field_is_enabled="1",
                    field_size="0",
                    field_is_editable="1",
                )
                if _result_['status'] != '1':
                    status = '0'
                self.circuit_id[handle] = _result_['tlv_field_handle']
                _result_ = self.ixiangpf.tlv_config(
                    handle=type_2_handle,
                    mode="create_field",
                    field_name="Code",
                    field_description="""Dhcp client TLV type field.""",
                    field_encoding="decimal",
                    field_size="1",
                    field_value="1",
                    field_is_enabled="1",
                    field_is_editable="0",
                    )
                if _result_['status'] != '1':
                    status = '0'
            else:
                _result_ = self.ixiangpf.tlv_config(
                    handle=self.circuit_id[handle],
                    mode="modify",
                    field_name="""Circuit ID""",
                    field_value=circuit_id,
                    field_encoding="string",
                    field_is_enabled="1",
                    field_size="0",
                    field_is_editable="1",
                )
                if _result_['status'] != '1':
                    status = '0'
                print(_result_)

        if 'remote_id' in kwargs:
            remote_id = kwargs.get('remote_id')
            if 'remote_id_start' in kwargs:
                start = str(kwargs.get('remote_id_start'))
                step = str(kwargs.get('remote_id_step', '1'))
                repeat = str(kwargs.get('remote_id_repeat', '1'))
                if '?' in remote_id:
                    increment = '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'
                    remote_id = remote_id.replace('?', increment)
                else:
                    remote_id = remote_id + '{Inc:' + start + ',' + step + ',' + ',' + repeat + '}'
            if handle not in self.remote_id:
                _result_ = self.ixiangpf.tlv_config(
                    handle=value_1_handle,
                    mode="create_tlv",
                    tlv_name="""[2] Agent Remote ID""",
                    tlv_is_enabled="1",
                    tlv_enable_per_session="1",
                    type_name="Type",
                    type_is_editable="0",
                    type_is_required="1",
                    length_name="Length",
                    # length_description="""Dhcp client TLV length field.""",
                    length_encoding="decimal",
                    length_size="1",
                    length_value="0",
                    length_is_editable="0",
                    length_is_enabled="1",
                    disable_name_matching="1",
                )
                if _result_['status'] != '1':
                    status = '0'
                #subTlv_2_handle = _result_['subtlv_handle']
                value_3_handle = _result_['tlv_value_handle']
                #length_3_handle = _result_['tlv_length_handle']
                type_3_handle = _result_['tlv_type_handle']
                _result_ = self.ixiangpf.multivalue_config(
                    pattern="string",
                    string_pattern=remote_id,
                )

                multivalue_5_handle = _result_['multivalue_handle']

                _result_ = self.ixiangpf.tlv_config(
                    handle=value_3_handle,
                    mode="create_field",
                    field_name="""Remote ID""",
                    field_encoding="string",
                    field_size="0",
                    field_value=multivalue_5_handle,
                    field_is_enabled="1",
                    field_is_editable="1",
                )
                if _result_['status'] != '1':
                    status = '0'
                else:
                    self.remote_id[handle] = _result_['tlv_field_handle']
                    _result_ = self.ixiangpf.tlv_config(
                        handle=type_3_handle,
                        mode="create_field",
                        field_name="Code",
                        field_description="""Dhcp client TLV type field.""",
                        field_encoding="decimal",
                        field_size="1",
                        field_value="2",
                        field_is_enabled="1",
                        field_is_editable="0",
                    )
                return status
            else:
                _result_ = self.ixiangpf.tlv_config(
                    handle=self.remote_id[handle],
                    mode="modify",
                    field_name="""Remote ID""",
                    field_encoding="string",
                    field_size="0",
                    field_value=remote_id,
                    field_is_enabled="1",
                    field_is_editable="1",
                )
                print(_result_)
                if _result_['status'] != '1':
                    status = '0'
        return status


def set_vlan(self, **kwargs):
    """
    :param self:                RT object
    :param kwargs:
    handle                      device group handle
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    :return:
    result
    """
    if 'handle' not in kwargs:
        raise Exception("handle is mandatory")
    vlan_args = dict()
    if 'svlan_start' in kwargs:
        vlan_args['start'] = kwargs.get('svlan_start')
        vlan_args['step'] = kwargs.get('svlan_step', '1')
        vlan_args['repeat'] = kwargs.get('svlan_repeat', '1')
        vlan_args['count'] = kwargs.get('svlan_length', '4094')
        svlan_handle = self.set_custom_pattern(**vlan_args)
    if 'vlan_start' in kwargs:
        vlan_args['start'] = kwargs.get('vlan_start')
        vlan_args['step'] = kwargs.get('vlan_step', '1')
        vlan_args['repeat'] = kwargs.get('vlan_repeat', '1')
        vlan_args['count'] = kwargs.get('vlan_length', '4094')
        vlan_handle = self.set_custom_pattern(**vlan_args)

    intf_args = dict()
    intf_args['protocol_handle'] = kwargs.get('handle')
    intf_args['mtu'] = kwargs.get('mtu', '1500')
    if 'mac' in kwargs:
        intf_args['mac'] = kwargs.get('mac')
    if 'vlan_start' in kwargs:
        intf_args['vlan'] = '1'
        intf_args['vlan_id_count'] = '1'
        intf_args['vlan_id'] = vlan_handle
    if 'svlan_start' in kwargs:
        intf_args['vlan_id_count'] = '2'
        intf_args['vlan_id'] = "{},{}".format(svlan_handle, vlan_handle)


    if 'ethernet' in kwargs['handle']:
        intf_args['mode'] = 'modify'

    _result_ = self.ixiangpf.interface_config(**intf_args)
    #print(_result_)
    return _result_


def add_device_group(self, **kwargs):
    """
    :param self:            RT object
    :param kwargs:
    port_handle:            provide a port handle
    topology_handle:        provide a topology handle
    device_handle:          provide a device handle
    device_count:           provide device group multiplier

    :return: a dictionary of status and device handle
    status                  1 or 0
    device_handle
    """
    device_args = dict()
    if 'port_handle' in kwargs:
        port_handle = kwargs.get('port_handle')
        print(port_handle)
        port = self.handle_to_port_map[port_handle]
        topo_handle = self.handles[port]['topo']
        device_args['topology_handle'] = topo_handle
    if 'topology_handle' in kwargs:
        device_args['topology_handle'] = kwargs['topology_handle']
        for key in self.handles.keys():
            if self.handles[key]['topo'] == kwargs['topology_handle']:
                port = key
    if 'device_group_handle' in kwargs:
        device_args['device_group_handle'] = kwargs['device_group_handle']
        for key in self.handles.keys():
            if kwargs['device_group_handle'] in self.handles[key]['device_group_handle']:
                port = key
    device_args['device_group_multiplier'] = kwargs.get('device_count', '1')
    result = dict()
    result['status'] = '1'
    status = self.ixiangpf.topology_config(**device_args)
    if status['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to create device group ")
    else:
        device_handle = status['device_group_handle']
        self.device_group_handle.append(device_handle)
        self.handles[port]['device_group_handle'].append(device_handle)
        result['device_group_handle'] = device_handle
    return result
       # self.handles[device_handle]['mac'] = "00:00:{num:02d}:00:00:01".format(num=len(self.device_group_handle))


def add_dhcp_client(self, **kwargs):
    """
    :param self:                RT object
    :param kwargs:
    mandatory:
    port:                       Tester physical port
    num_sessions:               client counts

    optional:
    ip_type:                    ipv4, ipv4, dual
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    remote_id:                  option82 remote_id string
    remote_id_start:            remote id start number
    remote_id_step:             remote id step number
    remote_id_repeat:           remote id repeat number
    circuit_id:                 option82 circuit id string
    circuit_id_start:           circuit id start number
    circuit_id_step:            circuit id step number
    circuit_id_repeat:          circuit id repeat number
    v6_remote_id:               v6 option 38 remote id string
    v6_remote_id_start:         remote id start number
    v6_remote_id_step:          remote id step number
    v6_remote_id_repeat:        remote id repeat number
    enterprise_id:              v6 enterprise vendor id, used with remote id
    enterprise_id_step:         enterprise id increase step
    interface_id:               v6 option 17 interface id string
    interface_id_start:         v6 interface id start number
    interface_id_step:          v6 interface id step number
    interface_id_repeat:        v6 interface id repeat number
    rapid_commit:               use_rapid_commit value 1 or 0
    dhcp4_broadcast:            dhcpv4 broadcast value 1 or 0
    dhcpv6_ia_type:             dhcpv6 IA type: IANA, IAPD, IANA_IAPD
    v6_max_no_per_client:       The maximum number of addresses/prefixes that can be negotiated by a DHCPv6 Client
    dhcpv6_iana_count:          The number of IANA IAs requested in a single negotiation
    dhcpv6_iapd_count:          The number of IAPD IAs requested in a single negotiation
    softgre:                    softgre feature 1 or 0
    gre_dst_ip:                 softgre tunnel destination address
    gre_local_ip:               softgre tunnel local address
    gre_netmask:                softgre tunnel mask
    gre_gateway:                softgre tunnel gateway address
    gre_vlan_id:                softgre vlan id
    gre_vlan_id_step:           softgre vlan id step


    :return: a dictionary of status and handle
    status:                     1 or 0
    device_group_handle:
    ethernet_handle:
    dhcpv4_client_handle:
    dhcpv6_client_handle:
    """
    result = dict()
    result['status'] = '1'
    dhcp_args = dict()
    if 'port' in kwargs:
        port = kwargs.get('port')
        port_handle = self.port_to_handle_map[port]
        ##create devicegroup
        topo_handle = self.handles[port]['topo']
        if 'softgre' in kwargs:
            gre_args = dict()
            gre_args['port'] = port
            gre_args['ip_addr'] = kwargs['gre_local_ip']
            gre_args['gateway'] = kwargs['gre_gateway']
            gre_args['gre_dst_ip'] = kwargs['gre_dst_ip']
            if 'gre_vlan_id' in kwargs:
                gre_args['vlan_id'] = kwargs['gre_vlan_id']
                gre_args['vlan_id_step'] = kwargs.get('gre_vlan_id_step', '1')
            if 'gre_netmask' in kwargs:
                gre_args['netmask'] = kwargs['gre_netmask']
            config_status = self.add_link(**gre_args)
            device_handle = config_status['device_group_handle']
            topology_status = self.add_device_group(device_group_handle=device_handle,
                                                    device_count=kwargs.get('num_sessions', '1'))
        else:
            topology_status = self.add_device_group(topology_handle=topo_handle,
                                                    device_count=kwargs.get('num_sessions', '1'))
        if topology_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create device group for port handle {}".format(port_handle))

        device_handle = topology_status['device_group_handle']
        result['device_group_handle'] = topology_status['device_group_handle']
        status = self.set_vlan(handle=device_handle, **kwargs)
        if status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create ethernet for device group {}".format(device_handle))
        #dhcp_args = dict()
        #dhcp_args['handle'] = port_handle
        dhcp_args['handle'] = status['ethernet_handle']
        result['ethernet_handle'] = status['ethernet_handle']
        dhcp_args['mode'] = 'create'
    elif 'handle' in kwargs:
        dhcp_args['mode'] = 'modify'
        dhcp_args['handle'] = kwargs['handle']
        if 'num_sessions' in kwargs:
            dhcp_args['num_sessions'] = kwargs['num_sessions']
        if 'vlan_start' in kwargs or 'svlan_start' in kwargs:
            self.set_vlan(**kwargs)

    if 'dhcpv6_ia_type' in kwargs:
        dhcp_args['dhcp6_range_ia_type'] = kwargs.get('dhcpv6_ia_type')

    if 'rapid_commit' in kwargs:
        dhcp_args['use_rapid_commit'] = kwargs.get('rapid_commit')

    if 'dhcp4_broadcast' in kwargs:
        dhcp_args['dhcp4_broadcast'] = kwargs.get('dhcp4_broadcast')

    if 'v6_max_no_per_client' in kwargs:
        dhcp_args['dhcp6_range_max_no_per_client'] = kwargs.get('v6_max_no_per_client')

    if 'dhcpv6_iana_count' in kwargs:
        dhcp_args['dhcp6_range_iana_count'] = kwargs.get('dhcpv6_iana_count')

    if 'dhcpv6_iapd_count' in kwargs:
        dhcp_args['dhcp6_range_iapd_count'] = kwargs.get('dhcpv6_iapd_count')


    if 'ip_type' in kwargs:
        if 'dual' in kwargs['ip_type']:
            config_status = self.ixiangpf.emulation_dhcp_group_config(**dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcp client")
            else:
                if 'dhcpv4client_handle' in config_status:
                    handle = config_status['dhcpv4client_handle']
                    self.dhcpv4_index += 1
                    self.device_to_dhcpv4_index[handle] = self.dhcpv4_index
                    self.dhcpv4_client_handle.append(handle)
                    self.handles[port]['dhcpv4_client_handle'].append(handle)
                    result['dhcpv4_client_handle'] = handle

            dhcp_args['dhcp_range_ip_type'] = 'ipv6'
            config_status = self.ixiangpf.emulation_dhcp_group_config(**dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client for dual stack")
            else:
                if 'dhcpv6client_handle' in config_status:
                    v6handle = config_status['dhcpv6client_handle']
                    self.dhcpv6_index += 1
                    self.device_to_dhcpv6_index[v6handle] = self.dhcpv6_index
                    self.dhcpv6_client_handle.append(v6handle)
                    self.handles[port]['dhcpv6_client_handle'].append(v6handle)
                    result['dhcpv6_client_handle'] = v6handle

        elif kwargs['ip_type'] == "ipv4":
            dhcp_args['dhcp_range_ip_type'] = kwargs.get('ip_type')
            config_status = self.ixiangpf.emulation_dhcp_group_config(**dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcp client")
            else:
                if 'dhcpv4client_handle' in config_status:
                    handle = config_status['dhcpv4client_handle']
                    self.dhcpv4_index += 1
                    self.device_to_dhcpv4_index[handle] = self.dhcpv4_index
                    self.dhcpv4_client_handle.append(handle)
                    self.handles[port]['dhcpv4_client_handle'].append(handle)
                    result['dhcpv4_client_handle'] = handle

        elif kwargs['ip_type'] == "ipv6":
            dhcp_args['dhcp_range_ip_type'] = kwargs.get('ip_type')
            config_status = self.ixiangpf.emulation_dhcp_group_config(**dhcp_args)
            if config_status['status'] != '1':
                result['status'] = '0'
                raise Exception("failed to add dhcpv6 client")
            else:
                if 'dhcpv6client_handle' in config_status:
                    v6handle = config_status['dhcpv6client_handle']
                    self.dhcpv6_index += 1
                    self.device_to_dhcpv6_index[v6handle] = self.dhcpv6_index
                    self.dhcpv6_client_handle.append(v6handle)
                    self.handles[port]['dhcpv6_client_handle'].append(v6handle)
                    result['dhcpv6_client_handle'] = v6handle
    else:
        kwargs['ip_type'] = "ipv4"
        dhcp_args['dhcp_range_ip_type'] = kwargs.get('ip_type')
        config_status = self.ixiangpf.emulation_dhcp_group_config(**dhcp_args)
        if config_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add dhcp client")
        else:
            if 'dhcpv4client_handle' in config_status:
                handle = config_status['dhcpv4client_handle']
                self.dhcpv4_client_handle.append(handle)
                self.handles[port]['dhcpv4_client_handle'].append(handle)
                self.dhcpv4_index += 1
                result['dhcpv4_client_handle'] = handle
                #self.device_to_dhcpv4_index[handle] = self.dhcpv4_index

    if 'remote_id' in kwargs or 'circuit_id' in kwargs:
        if not self.set_option_82(handle=handle, **kwargs):
            result['status'] = '0'

    if 'interface_id' in kwargs or 'v6_remote_id' in kwargs:
        if not self.set_v6_option(handle=v6handle, **kwargs):
            result['status'] = '0'

    return result


def set_dhcp_client(self, **kwargs):
    """
    #rt.ixiangpf.emulation_dhcp_config(handle='/globals', mode='create',request_rate='150',
     release_rate='220', outstanding_releases_count='900',outstanding_session_count='1000', ip_version='4')
    :param self:                RT object
    :param kwargs:
    Mandatory:
     handle:                    dhcp client handle

    Optional:
    type:                       dhcpv4 or v6, can be used for setting login/logout rate only
    msg_timeout:                timeout for a msg like discover
    login_rate:                 request rate (must be a list for all the device/ports
    outstanding:                outstanding size for login(must be a list for all)
    logout_rate:                release rate(must be a list for all the device/ports)
    retry_count:                retry times for msg
    login_rate_mode:            starting scale mode (per port/per device)
    logout_rate_mode:           stop scale mode
    remote_id:                  option82 remote_id string
    remote_id_start:            remote id start number
    remote_id_step:             remote id step number
    remote_id_repeat:           remote id repeat number
    circuit_id:                 option82 circuit id string
    circuit_id_start:           circuit id start number
    circuit_id_step:            circuit id step number
    circuit_id_repeat:          circuit id repeat number
    v6_remote_id:               v6 option 38 remote id string
    v6_remote_id_start:         remote id start number
    v6_remote_id_step:          remote id step number
    v6_remote_id_repeat:        remote id repeat number
    enterprise_id:              v6 enterprise vendor id, used with remote id
    enterprise_id_step:         enterprise id increase step
    interface_id:               v6 option 17 interface id string
    interface_id_start:         v6 interface id start number
    interface_id_step:          v6 interface id step number
    interface_id_repeat:        v6 interface id repeat number

    :return:
    status                      1 or 0
    """

    status = '1'
    if not ('handle' in kwargs or 'type' in kwargs):
        raise Exception("dhcp handle or type  must be provided")
    dhcp_args = dict()

    if 'login_rate' in kwargs:
        dhcp_args['start_scale_mode'] = kwargs.get('login_rate_mode', 'device_group')

        login_rate = self.add_rate_multivalue(kwargs['login_rate'])
        dhcp_args['request_rate'] = login_rate

        dhcp_args['outstanding_session_count'] = '1000'
        dhcp_args['override_global_setup_rate'] = '1'
        if 'outstanding' in kwargs:
            dhcp_args['outstanding_session_count'] = self.add_rate_multivalue(kwargs['outstanding'])
            ##will change to multivalue handle for the rates in the future

    if 'logout_rate' in kwargs:
        dhcp_args['stop_scale_mode'] = kwargs.get('logout_rate_mode', 'device_group')
        logout_rate = self.add_rate_multivalue(kwargs['logout_rate'])
        dhcp_args['release_rate'] = logout_rate
        dhcp_args['outstanding_releases_count'] = '1000'
        dhcp_args['override_global_teardown_rate'] = '1'

    if 'msg_timeout' in kwargs:
        dhcp_args['msg_timeout'] = kwargs['msg_timeout']

    if 'retry_count' in kwargs:
        dhcp_args['retry_count'] = kwargs['retry_count']

    if dhcp_args:
        if 'v4' in kwargs['handle']:
            dhcp_args['dhcp4_arp_gw'] = '1'
            dhcp_args['ip_version'] = '4'
        if 'v6' in kwargs['handle']:
            dhcp_args['dhcp6_ns_gw'] = '1'
            dhcp_args['ip_version'] = '6'
        dhcp_args['handle'] = "/globals"
        dhcp_args['mode'] = "create"
        config_status = self.ixiangpf.emulation_dhcp_config(**dhcp_args)
        if config_status['status'] != '1':
            status = '0'
            raise Exception("failed to change dhcp client {}".format(kwargs['handle']))
    else:
        return self.add_dhcp_client(**kwargs)

    # if 'remote_id' in kwargs or 'circuit_id' in kwargs:
    #     status = self.set_option_82(**kwargs)
    #
    #
    # if 'interface_id' in kwargs or 'v6_remote_id' in kwargs:
    #     status = self.set_v6_option(**kwargs)
    return status


def add_rate_multivalue(self, listitem):
    """
    :param self:                RT object
    :param listitem:            a list of rate values
    :return:
    """
    if isinstance(listitem, list):
        value = ''
        index = ''
        length = len(listitem)
        seq = 0
        for i in listitem:
            seq += 1
            if seq == length:
                value += "{}".format(i)
                index += "{}".format(seq)
            else:
                value += "{},".format(i)
                index += "{},".format(seq)
        print(value)
        print(index)

        _result_ = self.ixiangpf.multivalue_config(
            pattern="single_value",
            single_value="50",
            overlay_value='{}'.format(value),
            # overlay_value_step      = '%s,%s,%s' % ("300", "800", "700"),
            overlay_index='{}'.format(index),
            #   overlay_index_step      = '%s,%s,%s' % ("0", "0", "0"),
            # overlay_count='%s,%s,%s' % ("1", "1", "1"),
        )
        if _result_['status'] != '1':
            raise Exception("failed to create multivalue handle for listitem {}".format(listitem))
        else:
            return  _result_['multivalue_handle']
    else:
        raise Exception("login rate must be a list")


def dhcp_client_action(self, **kwargs):
    """
    :param self:        RT object
    :param kwargs:
    port_handle:        specify a port handle to login all the clients?
    handle:             dhcp handles
    action:             start, stop, renew, abort, restart_down
    :return:
    result              dictionary include status and log message

    #rt.dhcp_client_action(handle=rt.handles['1/1']['dhcpv4_client_handle'][0], action='bind')
    #rt.dhcp_client_action(port_handle='1/1/1', action='bind')
    """
    result = dict()
    dhcp_args = dict()
    result['status'] = '1'
    if 'handle' not in kwargs or 'action' not in kwargs:
        print("mandatory params 'handle/action' not provided ")
        result['status'] = '0'
    else:
        dhcp_args['handle'] = kwargs['handle']
        dhcp_args['action'] = kwargs['action']
        if 'restart' in kwargs['action']:
            dhcp_args['action'] = 'restart_down'
        elif 'start' in kwargs['action']:
            dhcp_args['action'] = 'bind'
        elif 'stop' in kwargs['action']:
            dhcp_args['action'] = 'release'

        result = self.ixiangpf.emulation_dhcp_control(**dhcp_args)
    return result


def dhcp_client_stats(self, **kwargs):
    """
    :param self:        RT object
    :param kwargs:
    port_handle:        specify a port handle to get the aggregated stats
    handle:             specify a dhcp handle to get the stats
    dhcp_version:       dhcp4/dhcp6
    execution_timeout   specify the timeout for the command
    mode:               aggregate_stats/session
    :return:            dictionary
    """
    result = self.ixiangpf.emulation_dhcp_stats(**kwargs)
    return result


def add_pppoe_client(self, **kwargs):
    """
    :param self:               RT object
    :param kwargs:
    port:                      specify a port  for creating a simulation
    num_sessions:              specify the simulation count

    auth_req_timeout:          authentication request timeout
    echo_req:                  echo request 1 or 0
    echo_rsp:                  echo response 1 or 0
    ip_type:                    v4/dual/v6
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    svlan_length:               svlan sequence length
    agent_remote_id:            agent_remote_id string, for example can be "remoteid" or "remoteid?"
    agent_circuit_id:           agent_circuit_id string
    auth_mode:                  authentication mode: pap/chap/pap_or_chap
    username:                   ppp username
    password:                   ppp password
    ipcp_req_timeout:           ipcp request timeout
    max_auth_req:               maximum authentication requests
    max_padi_req:               maximum PADI requests
    max_padr_req:               maximum PADR requests
    max_ipcp_retry:             maximum ipcp retry
    max_terminate_req:          maximum terminate requests
    echo_req_interval:          echo requests interval
    dhcpv6_ia_type:             dhcpv6 ia type: iapd/iana/iana_iapd

    :return:
    result:                     dictionary of status, pppox_client_handle, dhcpv6_client_handle
    """
    result = dict()
    result['status'] = '1'
    pppoe_args = dict()
    if 'port' in kwargs:
        port = kwargs.get('port')
        port_handle = self.port_to_handle_map[port]
        ##create devicegroup
        topo_handle = self.handles[port]['topo']

        topology_status = self.add_device_group(topology_handle=topo_handle,
                                                device_count=kwargs.get('num_sessions', '1'))
        if topology_status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create device group for port handle {}".format(port_handle))

        device_handle = topology_status['device_group_handle']
        result['device_group_handle'] = topology_status['device_group_handle']
        status = self.set_vlan(handle=device_handle, **kwargs)
        if status['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to create ethernet for device group {}".format(device_handle))

        pppoe_args['handle'] = status['ethernet_handle']
        result['ethernet_handle'] = status['ethernet_handle']
        pppoe_args['mode'] = 'add'
        pppoe_args['port_role'] = 'access'
    if 'handle' in kwargs:
        pppoe_args['handle'] = kwargs['handle']
        pppoe_args['mode'] = 'modify'
        if 'num_sessions' in kwargs:
            pppoe_args['num_sessions'] = kwargs['num_sessions']
        if 'vlan_start' in kwargs or 'svlan_start' in kwargs:
            self.set_vlan(**kwargs)
    pppoe_args['port_role'] = 'access'
    if 'auth_req_timeout' in kwargs:
        pppoe_args['auth_req_timeout'] = kwargs['auth_req_timeout']
    if 'echo_req' in kwargs:
        pppoe_args['echo_req'] = kwargs['echo_req']
    if 'echo_rsp' in kwargs:
        pppoe_args['echo_rsp'] = kwargs['echo_rsp']
    if 'ip_type' in kwargs:
        if 'v4' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv4_cp'
        if 'v6' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'ipv6_cp'
            pppoe_args['dhcpv6_hosts_enable'] = '1'
            if 'dhcpv6_ia_type' in kwargs:
                pppoe_args['dhcp6_pd_client_range_ia_type'] = kwargs['dhcpv6_ia_type']
        if 'dual' in kwargs['ip_type']:
            pppoe_args['ip_cp'] = 'dual_stack'
            pppoe_args['dhcpv6_hosts_enable'] = '1'
            if 'dhcpv6_ia_type' in kwargs:
                pppoe_args['dhcp6_pd_client_range_ia_type'] = kwargs['dhcpv6_ia_type']

    if 'ipcp_req_timeout' in kwargs:
        pppoe_args['ipcp_req_timeout'] = kwargs['ipcp_req_timeout']
    if 'max_auth_req' in kwargs:
        pppoe_args['max_auth_req'] = kwargs['max_auth_req']
    if 'max_padi_req' in kwargs:
        pppoe_args['max_padi_req'] = kwargs['max_padi_req']
    if 'max_padr_req' in kwargs:
        pppoe_args['max_padr_req'] = kwargs['max_padr_req']
    if 'max_ipcp_retry' in kwargs:
        pppoe_args['max_ipcp_retry'] = kwargs['max_ipcp_retry']
    if 'max_terminate_req' in kwargs:
        pppoe_args['max_terminate_req'] = kwargs['max_terminate_req']
    if 'echo_req_interval' in kwargs:
        pppoe_args['echo_req_interval'] = kwargs['echo_req_interval']
    if 'auth_mode' in kwargs:
        pppoe_args['auth_mode'] = kwargs['auth_mode']
        if 'username' in kwargs:
            username = kwargs['username'].replace('?', '{Inc:1,,,1}')
            _result_ = self.ixiangpf.multivalue_config(
                pattern="string",
                string_pattern=username,
            )
            multivalue_5_handle = _result_['multivalue_handle']
        if 'pap' in kwargs['auth_mode']:
            if 'username'  in kwargs:
                pppoe_args['username'] = multivalue_5_handle
            if 'password' in kwargs:
                pppoe_args['password'] = kwargs['password']
        if 'chap' in kwargs['auth_mode']:
            if 'username' in kwargs:
                pppoe_args['chap_name'] = multivalue_5_handle
            if 'password' in kwargs:
                pppoe_args['chap_secret'] = kwargs['password']
    if 'agent_circuit_id' in kwargs:
        circuit_id = kwargs['agent_circuit_id'].replace('?', '{Inc:1,,,1}')
        _result_ = self.ixiangpf.multivalue_config(
            pattern="string",
            string_pattern=circuit_id,
        )
        print(_result_)
        multivalue_6_handle = _result_['multivalue_handle']
        pppoe_args['agent_circuit_id'] = multivalue_6_handle
    if 'agent_remote_id' in kwargs:
        remote_id = kwargs['agent_remote_id'].replace('?', '{Inc:1,,,1}')
        _result_ = self.ixiangpf.multivalue_config(
            pattern="string",
            string_pattern=remote_id,
        )
        print(_result_)
        multivalue_7_handle = _result_['multivalue_handle']
        pppoe_args['agent_remote_id'] = multivalue_7_handle

    config_status = self.ixiangpf.pppox_config(**pppoe_args)
    #print(config_status)
    if config_status['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add/modify pppoe client for port {}".format(port))
    else:
        if 'pppox_client_handle' in config_status:
            handle = config_status['pppox_client_handle']
            self.pppox_client_handle.append(handle)
            result['pppox_client_handle'] = handle
            self.handles[port]['pppox_client_handle'].append(handle)
            if 'ip_type' in kwargs:
                if 'v6' in kwargs['ip_type'] or 'dual' in kwargs['ip_type']:
                    v6handle = config_status['dhcpv6_client_handle']
                    self.dhcpv6_client_handle.append(v6handle)
                    result['dhcpv6_client_handle'] = v6handle
                    self.handles[port]['dhcpv6_over_pppox_handle'][handle] = v6handle

    return result


def set_pppoe_client(self, **kwargs):
    """
    :param self:                RT object
    :param kwargs:
    handle:                     specify a pppox handle
    num_sessions:               specify the simulation count
    auth_req_timeout:           authentication request timeout
    echo_req:                   echo request 1 or 0
    echo_rsp:                   echo response 1 or 0
    type:                       v4/dual/v6
    vlan_start:                 the first vlan id
    vlan_step:                  vlan increase step
    vlan_repeat:                vlan repeat number
    vlan_length:                vlan sequence length
    svlan_start:                first svlan id
    svlan_step:                 svlan increase step
    svlan_repeat:               svlan repeat number
    vlan_length:                svlan sequence length
    agent_remote_id:            agent_remote_id string, for example can be "remoteid" or "remoteid?"
    agent_circuit_id:           agent_circuit_id string
    auth_mode:                  authentication mode: pap/chap/pap_or_chap
    ipcp_req_timeout:           ipcp request timeout
    max_auth_req:               maximum authentication requests
    max_padi_req:               maximum PADI requests
    max_padr_req:               maximum PADR requests
    max_ipcp_retry:             maximum ipcp retry
    max_terminate_req:          maximum terminate requests
    echo_req_interval:          echo requests interval
    login_rate:                 login rate
    outstanding:                outstanding size for login
    logout_rate:                logout rate
    :return:
    """
    if not ('login_rate' in kwargs or 'logout_rate' in kwargs):
        status = self.add_pppoe_client(**kwargs)
        return status

    else:
    ##set the login/logout rate
        pppox_args = dict()
        pppox_args['port_role'] = "access"
        pppox_args['handle'] = "/globals"
        pppox_args['mode'] = 'add'
        if 'login_rate' in kwargs:
            login_rate = self.add_rate_multivalue(kwargs['login_rate'])
            pppox_args['attempt_rate'] = login_rate
            pppox_args['attempt_max_outstanding'] = '1000'
            pppox_args['attempt_scale_mode'] = kwargs.get('rate_mode', 'device_group')
            if 'outstanding' in kwargs:
                pppox_args['attempt_max_outstanding'] = self.add_rate_multivalue(kwargs['outstanding'])
        if 'logout_rate' in kwargs:
            logout_rate = self.add_rate_multivalue(kwargs['logout_rate'])
            pppox_args['disconnect_rate'] = logout_rate
            pppox_args['disconnect_max_outstanding'] = '1000'
            pppox_args['disconnect_scale_mode'] = kwargs.get('rate_mode', 'device_group')

        result = self.ixiangpf.pppox_config(**pppox_args)
        return result


def pppoe_client_action(self, **kwargs):
    """
    login/logout pppoe client
    :param self:            RT object
    :param kwargs:
    handle:                 pppox handles/ dhcpv6 over pppox handle
    action:                 start, stop, restart_down, reset, abort
    :return:
    status
    """
    result = dict()
    result['status'] = '1'
    pppoe_args = dict()

    if 'action' not in kwargs or 'handle' not in kwargs:
        print("mandatory params 'handle/action' not provided ")
        result['status'] = '0'
    else:


        pppoe_args['action'] = kwargs.get('action')
        if 'restart' in kwargs['action']:
            pppoe_args['action'] = 'restart_down'
        elif 'start' in kwargs['action']:
            pppoe_args['action'] = 'connect'
        elif 'stop' in kwargs['action']:
            match = re.match('.*pppoxclient:\d+', kwargs['handle'])
            kwargs['handle'] = match.group(0)
            pppoe_args['action'] = 'disconnect'

        pppoe_args['handle'] = kwargs['handle']
        result = self.ixiangpf.pppox_control(**pppoe_args)
    return result


def pppoe_client_stats(self, **kwargs):
    """
    get statistics for pppoe client
    :param self:                RT object
    :param kwargs:
    port_handle:                port handle used to retrieve the statistics
    handle:                     pppox handle used to retrieve the statistics
    mode:                       aggregate /session /session all
    execution_timeout:          the execution timeout setting, default is 1800
    :return:
    status
    """
    status = self.ixiangpf.pppox_stats(**kwargs)
    return status


def add_link(self, **kwargs):
    """
    :param self:                RT object
    :param kwargs:
    port                        physical tester port
    vlan_id                     link vlan id
    vlan_id_step
    svlan_id
    svlan_id_step
    ip_addr
    ip_addr_step
    mask
    gateway
    ipv6_addr
    ipv6_addr_step
    ipv6_prefix_length
    ipv6_gateway
    gre_dst_ip
    gre_dst_ip_step
    count

    :return:
    device group handle
    ethernet handle
    ip handle
    gre handle
    """
    if 'port' not in kwargs:
        raise Exception("port is mandatory when adding link device")
    port = kwargs.get('port')
    #port_handle = self.port_to_handle_map[port]
    count = kwargs.get('count', '1')
    link_args = dict()
    result = dict()
    result['status'] = '1'
    #create device group first
    status_config = self.ixiangpf.topology_config(topology_handle=self.handles[port]['topo'],
                                                  device_group_multiplier=count)
    if status_config['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add device group for port {}".format(port))
    else:
        device_group_handle = status_config['device_group_handle']
        link_args['protocol_handle'] = device_group_handle
        self.device_group_handle.append(device_group_handle)
        self.handles[port]['device_group_handle'].append(device_group_handle)
        result['device_group_handle'] = device_group_handle

    if 'vlan_id' in kwargs:
        link_args['vlan_id'] = kwargs.get('vlan_id')
        link_args['vlan'] = '1'
        link_args['vlan_id_step'] = kwargs.get('vlan_id_step', '1')
    if 'svlan_id' in kwargs:
        svlan_id = kwargs['svlan_id']
        svlan_id_step = kwargs.get('svlan_id_step', '1')
        vlan_id = kwargs.get('vlan_id', '1')
        vlan_id_step = kwargs.get('vlan_id_step', '1')
        link_args['vlan'] = '1'
        link_args['vlan_id'] = "{},{}".format(svlan_id, vlan_id)
        link_args['vlan_id_step'] = "{},{}".format(svlan_id_step, vlan_id_step)
    if 'vlan_user_priority' in kwargs:
        link_args['vlan_user_priority'] = kwargs.get('vlan_user_priority')
        link_args['vlan_user_priority_step'] = kwargs.get('vlan_user_priority_step', '1')

    # create ethernet
    link_args['mtu'] = kwargs.get('mtu', '1500')
    status_config = self.ixiangpf.interface_config(**link_args)
    if status_config['status'] != '1':
        result['status'] = '0'
        raise Exception("failed to add ethernet for device group {}".format(device_group_handle))
    else:
        ethernet_handle = status_config['ethernet_handle']
        self.handles[port]['ethernet_handle'].append(ethernet_handle)
        result['ethernet_handle'] = ethernet_handle

    intf_args = {}
    intf_args['protocol_handle'] = ethernet_handle
    if 'ip_addr' in kwargs:
        intf_args['intf_ip_addr'] = kwargs['ip_addr']
        intf_args['intf_ip_addr_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
        if 'gateway' in kwargs:
            intf_args['gateway'] = kwargs['gateway']
            intf_args['gateway_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
        if 'netmask' in kwargs:
            intf_args['netmask'] = kwargs['netmask']

    if 'ipv6_addr' in kwargs:
        intf_args['ipv6_intf_addr'] = kwargs['ipv6_addr']
        intf_args['ipv6_intf_addr_step'] = kwargs.get('ipv6_addr_step', '00:00:00:01:00:00:00:00')
        if 'ipv6_gateway' in kwargs:
            intf_args['ipv6_gateway'] = kwargs['ipv6_gateway']
            intf_args['ipv6_gateway_step'] = kwargs.get('ipv6_addr_step', '00:00:00:01:00:00:00:00')
        if 'ipv6_prefix_length' in kwargs:
            intf_args['ipv6_prefix_length'] = kwargs.get('ipv6_prefix_length', '64')

    if 'ip_addr' in kwargs or 'ipv6_addr' in kwargs:
        status_config = self.ixiangpf.interface_config(**intf_args)
        if status_config['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add ip/ipv6 address for ethernet {}".format(ethernet_handle))
        else:
            if 'ipv4_handle' in status_config:
                ip_handle = status_config['ipv4_handle']
                self.link_ip_handle.append(ip_handle)
                self.handles[port]['ipv4_handle'] = ip_handle
                result['ipv4_handle'] = ip_handle
            if 'ipv6_handle' in status_config:
                ipv6_handle = status_config['ipv6_handle']
                self.link_ipv6_handle.append(ipv6_handle)
                self.handles[port]['ipv6_handle'].append(ipv6_handle)
                result['ipv6_handle'] = ipv6_handle


    if 'gre_dst_ip' in kwargs:

        ###config gre over ip
        gre_args = dict()
        gre_args['protocol_handle'] = ip_handle
        gre_args['gre_dst_ip_addr'] = kwargs['gre_dst_ip']
        if 'gre_dst_ip_step' in kwargs:
            gre_args['gre_dst_ip_addr_step'] = kwargs['gre_dst_ip_step']

        status_config = self.ixiangpf.interface_config(**gre_args)
        if status_config['status'] != '1':
            result['status'] = '0'
            raise Exception("failed to add gre destination address for ip handle {}".format(ip_handle))
        else:
            gre_handle = status_config['greoipv4_handle']
            self.link_gre_handle.append(gre_handle)
            self.handles[port]['gre_handle'] = gre_handle
            result['gre_handle'] = gre_handle

    return result


def set_link(self, **kwargs):
    """
    :param self:                RT object
    :param kwargs:
    handle:                     protocol handle
    vlan_id                     link vlan id
    vlan_id_step
    svlan_id
    svlan_id_step
    ip_addr
    ip_addr_step
    mask
    gateway
    ipv6_addr
    ipv6_addr_step
    ipv6_prefix_length
    ipv6_gateway
    :return:
    """
    result = '1'
    if 'handle' not in kwargs:
        raise Exception('link handle must be provided')
    link_args = dict()
    link_args['protocol_handle'] = kwargs['handle']
    link_args['mode'] = 'modify'
    if 'vlan_id' in kwargs:
        link_args['vlan_id'] = kwargs.get('vlan_id')
        link_args['vlan'] = '1'
        link_args['vlan_id_step'] = kwargs.get('vlan_id_step', '0')
    if 'svlan_id' in kwargs:
        svlan_id = kwargs['svlan_id']
        svlan_id_step = kwargs.get('svlan_id_step', '0')
        vlan_id = kwargs.get('vlan_id', '1')
        vlan_id_step = kwargs.get('vlan_id_step', '0')
        link_args['vlan'] = '1'
        link_args['vlan_id'] = "{},{}".format(svlan_id, vlan_id)
        link_args['vlan_id_step'] = "{},{}".format(svlan_id_step, vlan_id_step)
    if 'vlan_user_priority' in kwargs:
        link_args['vlan_user_priority'] = kwargs.get('vlan_user_priority')
        link_args['vlan_user_priority_step'] = kwargs.get('vlan_user_priority_step', '0')

    # modify ethernet
    if 'mtu' in kwargs:
        link_args['mtu'] = kwargs.get('mtu')
    if 'vlan_id' in kwargs or 'svlan_id' in kwargs:
        status_config = self.ixiangpf.interface_config(**link_args)
        print(status_config)
        result &= status_config['status']

    intf_args = {}
    intf_args['protocol_handle'] = kwargs['handle']
    intf_args['mode'] = 'modify'
    if 'ip_addr' in kwargs:
        intf_args['intf_ip_addr'] = kwargs['ip_addr']
        intf_args['intf_ip_addr_step'] = kwargs.get('ip_addr_step', '0.0.0.1')
        if 'gateway' in kwargs:
            intf_args['gateway'] = kwargs['gateway']
        if 'netmask' in kwargs:
            intf_args['netmask'] = kwargs['netmask']

    if 'ipv6_addr' in kwargs:
        intf_args['ipv6_intf_addr'] = kwargs['ipv6_addr']
        intf_args['ipv6_intf_addr_step'] = kwargs['ipv6_addr_step', '00:00:00:00:00:00:00:01']
        if 'ipv6_gateway' in kwargs:
            intf_args['ipv6_gateway'] = kwargs['ipv6_gateway']
        if 'ipv6_prefix_length' in kwargs:
            intf_args['ipv6_prefix_length'] = kwargs.get('ipv6_prefix_length', '64')

    if 'ip_addr' in kwargs or 'ipv6_addr' in kwargs:
        status_config = self.ixiangpf.interface_config(**intf_args)
        result &= status_config['status']

    return result


def remove_link(self, device_handle):
    # rt.ixiangpf.topology_config(mode='destroy', device_group_handle='/topology:2/deviceGroup:1')
    """
    :param self:                        RT object
    :param device_handle:               Device handle
    :return:
    """
    status = self.ixiangpf.topology_config(mode='destroy', device_group_handle=device_handle)
    return status


def link_action(self, **kwargs):
    """
    start/stop links
    :param self:                    RT object
    :param kwargs:
    handle:                         device_group/ip handle
    action:                         start/stop/abort
    :return:
    status:                         1 or 0
    """
    control_args = dict()
    control_args['handle'] = kwargs['handle']
    if 'start' in kwargs['action']:
        control_args['action'] = 'start_protocol'
    if 'stop' in kwargs['action']:
        control_args['action'] = 'stop_protocol'
    if 'abort' in kwargs['action']:
        control_args['action'] = 'abort_protocol'
    return self.ixiangpf.test_control(**control_args)


def add_traffic(self, **kwargs):
    #traffic_generator='ixnetwork_540', mode='create', endpointset_count=1,emulation_src_handle=pppoxhandle,
    #  emulation_dst_handle='/topology:4/deviceGroup:1', track_by='trackingenabled0')
    """
    set traffic streams
    :param self:                RT object
    :param kwargs:
    source:                     a list of traffic source handle
    destination:                a list of traffic destination handle
    bidirectional:              1 or 0
    rate:                       traffic rate , can be mbps, pps, percent, for example: 1000mbps, 1000pps, 100%
    type:                       traffic type "ipv4" or "ipv6"
    mesh_type                   traffic mesh type, default is many_to_many, can be one_to_one
    dynamic_update:             dynamic_udate the address values from ppp
    frame_size:                 single value /a list [min max step]
    track_by:                   how to track the statistics,  by default is
                                trafficItem and source destination value pair
    stream_id:                  needed when trying to modify existing traffic streams
    :return:
    status and hash
    """
    traffic_args = dict()
    traffic_args['traffic_generator'] = "ixnetwork_540"
    traffic_args['src_dest_mesh'] = kwargs.get('mesh_type', 'many_to_many')
    traffic_args['bidirectional'] = kwargs.get('bidirectional', '1')
    #import re
    if 'source' in kwargs:
        traffic_args['emulation_src_handle'] = kwargs['source']
    else:
        if 'type' in kwargs and 'v6' in kwargs['type']:
            traffic_args['emulation_src_handle'] = self.dhcpv6_client_handle
        else:
            traffic_args['emulation_src_handle'] = self.dhcpv4_client_handle + self.pppox_client_handle

    if 'destination' in kwargs:
        traffic_args['emulation_dst_handle'] = kwargs['destination']
    else:
        if 'type' in kwargs and 'v6' in kwargs['type']:
            traffic_args['emulation_dst_handle'] = self.link_ipv6_handle
        else:
            traffic_args['emulation_dst_handle'] = self.link_ip_handle

    if 'rate' in kwargs:
        if 'mbps' in kwargs['rate']:
            traffic_args['rate_mbps'] = re.sub('mbps', '', kwargs['rate'])
        if 'pps' in kwargs['rate']:
            traffic_args['rate_pps'] = re.sub('pps', '', kwargs['rate'])
        if '%' in kwargs['rate']:
            traffic_args['rate_percent'] = re.sub('%', '', kwargs['rate'])
    else:
        traffic_args['rate_pps'] = '1000'

    if 'stream_id' in kwargs:
        traffic_args['mode'] = 'modify'
    else:
        traffic_args['mode'] = 'create'

    if 'type' in kwargs:
        traffic_args['circuit_endpoint_type'] = kwargs['type']
    if 'dynamic_update' in kwargs:
        traffic_args['dynamic_update_fields'] = kwargs['dynamic_update']

    if 'frame_size' in kwargs:
        if isinstance(kwargs['frame_size'], list):
            traffic_args['frame_size_min'] = kwargs['frame_size'][0]
            traffic_args['frame_size_max'] = kwargs['frame_size'][1]
            traffic_args['frame_size_step'] = kwargs['frame_size'][2]
    else:
        traffic_args['frame_size'] = kwargs.get('frame_size', '1000')
    ##can also track by sourceDestEndpointPair0
    traffic_args['track_by'] = kwargs.get('track_by', 'sourceDestValuePair0 trackingenabled0')
    if 'traffic_generate' in kwargs:
        traffic_args['traffic_generate'] = kwargs['traffic_generate']

    config_status = self.ixiangpf.traffic_config(**traffic_args)
    if config_status['status'] == '1':
        if traffic_args['mode'] == 'create':
            self.traffic_item.append(config_status['stream_id'])
            self.stream_id.append(config_status['traffic_item'])
    return config_status


def set_traffic(self, **kwargs):
    """
    modify existing trafficitem
    :param self:                RT object
    :param kwargs:
    source:                     a list of traffic source handle
    destination:                a list of traffic destination handle
    bidirectional:              1 or 0
    rate:                       traffic rate , can be bps, pps, percent, for example: 1000000bps, 1000pps, 100%
    type:                       traffic type "ipv4" or "ipv6"
    mesh_type                   traffic mesh type, default is many_to_many, can be one_to_one
    dynamic_update:             dynamic_udate the address values from ppp
    frame_size:                 single value /a list [min max step]
    track_by:                   how to track the statistics,
                                by default is trafficItem and source destination endpoint pair
    stream_id:                  needed when trying to modify existing traffic streams
    :return:
    status:                    1 or 0
    """

    status = '1'
    if 'stream_id' not in kwargs:
        status = '0'
        print("stream_id is mandotory when modifying traffic item")
        return status
    result = self.add_traffic(**kwargs)
    status = result['status']
    return status


def get_traffic_stats(self, **kwargs):
    """

    :param kwargs:
    :param self:         RT object
    mode:                all/traffic_item
    :return:
    """
    stats_status = self.ixiangpf.traffic_stats(**kwargs)
    return stats_status


def get_protocol_stats(self, mode='global_per_protocol'):
    """
    :param self:
    :param mode:        'global_per_protocol'| 'global_per_port', by default is 'global_per_protocol'
    :return:
    """
    stats_status = self.ixiangpf.protocol_info(mode=mode)

    return stats_status[mode]


def traffic_action(self, **kwargs):
    """
    #rt.traffic_action(action='start')
    :param self:            RT object
    :param kwargs:
    action:                 start/stop/delete/poll/regenerate/apply/clearstats/reset
    handle:                 specify a specific traffic item if needed
    :return:
    """
    traffic_args = dict()
    if 'timeout' in kwargs:
        traffic_args['max_wait_timer'] = kwargs['timeout']
    if 'handle' in kwargs:
        traffic_args['handle'] = kwargs['handle']
    traffic_args['action'] = 'run'
    if 'start' in kwargs['action']:
        traffic_args['action'] = 'sync_run'
    if 'stop' in kwargs['action']:
        traffic_args['action'] = 'stop'
    if 'poll' in kwargs['action']:
        traffic_args['action'] = 'poll'
    if 'delete' in kwargs['action']:
        traffic_args['action'] = 'destroy'
    if 'clearstats' in kwargs['action']:
        traffic_args['action'] = 'clear_stats'
    if 'reset' in kwargs['action']:
        traffic_args['action'] = 'reset'
    if 'regenerate' in kwargs['action']:
        traffic_args['action'] = 'regenerate'
    if 'apply' in kwargs['action']:
        traffic_args['action'] = 'apply'
    print(traffic_args)
    result = self.ixiangpf.traffic_control(**traffic_args)
    if result['status'] == '1' and 'delete' in kwargs['action']:
        if 'handle' in kwargs:
            self.traffic_item.remove(kwargs['handle'])
        else:
            self.traffic_item.clear()
    return result

# def remove_traffic(self, **kwargs):
#     """deprecated
#     :param self:                RT object
#     :param kwargs:
#      stream_id:                 the stream_id name to be removed
#     :return:
#     """
#     status = '1'
#     if 'stream_id' in kwargs:
#         return self.ixiangpf.traffic_config(mode='remove', stream_id=kwargs['stream_id'])
#     else:
#         for item in self.traffic_item:
#             result = self.ixiangpf.traffic_config(mode='remove', stream_id=item)
#             if result['status'] != '1':
#                 status = '0'
#             else:
#                 self.traffic_item.remove(item)
#         return status

def start_all(self):
    """
    start all protocols
    :param self:                    RT object
    :return:
    a dictionary of status and other information
    """
    return self.ixiangpf.test_control(action='start_all_protocols')


def stop_all(self):
    """
    stop all protocols
    :param self:                    RT object
    :return:
    a dictionary of status and other information
    """
    return self.ixiangpf.test_control(action='stop_all_protocols')


def add_igmp_client(self, **kwargs):
    """
    :param self:                    RT object
    :param kwargs:
    handle:                         dhcp client handle or pppoe client handle
    version:                        version 2 or 3, default is 2
    filter_mode:                    include/exclude, default is include
    iptv:                           1 or 0, default is 0
    group_range:                    multicast group range, default is 1
    group_range_step:               the pattern that the range start address, default is 0.0.1.0
    group_start_addr:               multicast group start address
    group_step:                     group step pattern
    group_count:                    group counts
    src_grp_range:                  multicast source group range, default is 1
    src_grp_range_step:             multicast source group range step pattern, default is 0.0.1.0
    src_grp_start_addr:             multicast source group start address
    src_grp_step:                   multicast soutce group step pattern, default is 0.0.0.1
    src_grp_count:                  multicast source group count

    :return:
    result                          a dictionary include status, igmp_host_handle, igmp_group_handle, igmp_source_handle
    """
    result = dict()
    result['status'] = '1'
    igmp_param = dict()
    igmp_param['handle'] = kwargs.get('handle')
    igmp_param['mode'] = kwargs.get('mode', 'create')
    igmp_param['active'] = kwargs.get('active', '1')
    igmp_param['filter_mode'] = kwargs.get('filter_mode', 'include')
    igmp_param['enable_iptv'] = kwargs.get('iptv', '0')
    igmp_param['igmp_version'] = 'v' + str(kwargs.get('version', '2'))

    _result_ = self.ixiangpf.emulation_igmp_config(**igmp_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to add igmp client"
        result['status'] = '0'
        return result
    else:
        igmp_handle = _result_['igmp_host_handle']
        self.igmp_handles[kwargs.get('handle')] = igmp_handle
        self.igmp_handle_to_group[igmp_handle] = {}
        result['igmp_host_handle'] = igmp_handle

    addr_param = dict()
    addr_param['start'] = kwargs.get('group_start_addr', '225.0.0.1')
    addr_param['step'] = kwargs.get('group_range_step', "0.0.1.0")
    addr_param['count'] = kwargs.get('group_range', "1")
    multivalue_2_handle = self.add_addr_custom_pattern(**addr_param)

    _result_ = self.ixiangpf.emulation_multicast_group_config(
        mode="create",
        ip_addr_start=multivalue_2_handle,
        ip_addr_step=kwargs.get('group_step', "0.0.0.1"),
        num_groups=kwargs.get('group_count', "1"),
        active=kwargs.get('active', "1")
    )
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        igmp_group_handle = _result_['multicast_group_handle']
        self.igmp_handle_to_group[igmp_handle]['group_handle'] = igmp_group_handle


    src_addr_param = dict()
    src_addr_param['start'] = kwargs.get('src_grp_start_addr', "10.10.10.1")
    src_addr_param['step'] = kwargs.get('src_grp_range_step', "0.0.1.0")
    src_addr_param['count'] = kwargs.get('src_grp_range', "1")
    multivalue_3_handle = self.add_addr_custom_pattern(**src_addr_param)

    _result_ = self.ixiangpf.emulation_multicast_source_config(
        mode="create",
        ip_addr_start=multivalue_3_handle,
        ip_addr_step=kwargs.get('src_grp_step', "0.0.0.1"),
        num_sources=kwargs.get('src_grp_count', "1"),
        active="1",
    )
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        igmp_source_handle = _result_['multicast_source_handle']
        self.igmp_handle_to_group[igmp_handle]['src_group_handle'] = igmp_source_handle
    _result_ = self.ixiangpf.emulation_igmp_group_config(
        mode=kwargs.get('mode', "create"),
        g_filter_mode=kwargs.get('filter_mode', "include"),
        group_pool_handle=igmp_group_handle,
        no_of_grp_ranges=kwargs.get('group_range', "1"),
        no_of_src_ranges=kwargs.get('src_grp_range', "1"),
        session_handle=igmp_handle,
        source_pool_handle=igmp_source_handle,
    )
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to config the igmp group and src group set"
    else:
        result['igmp_group_handle'] = _result_['igmp_group_handle']
        result['igmp_source_handle'] = _result_['igmp_source_handle']
        self.igmp_handle_to_group[igmp_handle]['igmp_group_handle'] = _result_['igmp_group_handle']
        self.igmp_handle_to_group[igmp_handle]['igmp_source_handle'] = _result_['igmp_source_handle']

    return result


def set_igmp_client(self, **kwargs):
    """
    :param self:                    RT object
    :param kwargs:
    handle:                         igmp host handle
    version:                        version 2 or 3, default is 2
    filter_mode:                    include/exclude, default is include
    iptv:                           1 or 0, default is 0
    group_range:                    multicast group range, default is 1
    group_range_step:               the pattern that the range start address, default is 0.0.1.0
    group_start_addr:               multicast group start address
    group_step:                     group step pattern
    group_count:                    group counts
    src_grp_range:                  multicast source group range, default is 1
    src_grp_range_step:             multicast source group range step pattern, default is 0.0.1.0
    src_grp_start_addr:             multicast source group start address
    src_grp_step:                   multicast soutce group step pattern, default is 0.0.0.1
    src_grp_count:                  multicast source group count


    :return:
    status
    """
    result = dict()
    result['status'] = '1'
    igmp_param = dict()
    if 'handle' in kwargs:
        igmp_param['handle'] = kwargs.get('handle')
        igmp_group_handle = self.igmp_handle_to_group[kwargs.get('handle')]['group_handle']
        igmp_source_handle = self.igmp_handle_to_group[kwargs.get('handle')]['src_group_handle']
    else:
        raise Exception("handle is mandatory for modifying configuration")

    igmp_param['mode'] = kwargs.get('mode', 'modify')
    if 'active' in kwargs:
        igmp_param['active'] = kwargs.get('active')
    if 'filter_mode' in kwargs:
        igmp_param['filter_mode'] = kwargs.get('filter_mode')
    if 'iptv' in kwargs:
        igmp_param['enable_iptv'] = kwargs.get('iptv')
    if 'version' in kwargs:
        igmp_param['igmp_version'] = 'v' + str(kwargs.get('version', '2'))

    _result_ = self.ixiangpf.emulation_igmp_config(**igmp_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to set igmp client"
        result['status'] = '0'
        return result
    elif igmp_param['mode'] == 'delete':
        return result

    if 'group_start_addr'  in kwargs:
        addr_param = dict()
        addr_param['start'] = kwargs.get('group_start_addr')
        addr_param['step'] = kwargs.get('group_range_step', "0.0.1.0")
        addr_param['count'] = kwargs.get('group_range', "1")
        multivalue_2_handle = self.add_addr_custom_pattern(**addr_param)
        group_param = {}
        group_param['mode'] = 'modify'
        group_param['handle'] = igmp_group_handle
        group_param['ip_addr_start'] = multivalue_2_handle
        if 'group_step' in kwargs:
            group_param['ip_addr_step'] = kwargs.get('group_step')
        if 'group_count' in kwargs:
            group_param['num_groups'] = kwargs['group_count']
        if 'active' in kwargs:
            group_param['active'] = kwargs['active']
        _result_ = self.ixiangpf.emulation_multicast_group_config(**group_param)

        print(_result_)
        if _result_['status'] != '1':
            result['status'] = '0'

    if 'src_grp_start_addr' in kwargs:
        src_addr_param = dict()
        src_addr_param['start'] = kwargs.get('src_grp_start_addr', "10.10.10.1")
        src_addr_param['step'] = kwargs.get('src_grp_range_step', "0.0.1.0")
        src_addr_param['count'] = kwargs.get('src_grp_range', "1")
        multivalue_3_handle = self.add_addr_custom_pattern(**src_addr_param)
        src_grp_param = {}
        src_grp_param['mode'] = 'modify'
        src_grp_param['handle'] = igmp_source_handle
        src_grp_param['ip_addr_start'] = multivalue_3_handle
        if 'src_grp_step' in kwargs:
            src_grp_param['ip_addr_step'] = kwargs['src_grp_step']
        if 'src_grp_count' in kwargs:
            src_grp_param['num_sources'] = kwargs['src_grp_count']
        _result_ = self.ixiangpf.emulation_multicast_source_config(**src_grp_param)

        print(_result_)
        if _result_['status'] != '1':
            result['status'] = '0'
    igmp_group_param = {}
    igmp_group_param['mode'] = kwargs.get('mode', "modify")
    igmp_group_param['handle'] = self.igmp_handle_to_group[kwargs['handle']]['igmp_group_handle']
    igmp_group_param['session_handle'] = kwargs['handle']
    igmp_group_param['group_pool_handle'] = igmp_group_handle
    igmp_group_param['source_pool_handle'] = igmp_source_handle
    if 'group_range' in kwargs:
        igmp_group_param['no_of_grp_ranges'] = kwargs['group_range']
    if 'src_grp_range' in kwargs:
        igmp_group_param['no_of_src_ranges'] = kwargs['src_grp_range']
    _result_ = self.ixiangpf.emulation_igmp_group_config(**igmp_group_param)

    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to modify the igmp group and src group set"

    return result


def igmp_client_action(self, **kwargs):
    """
    :param self:                                RT object
    :param kwargs:
    handle:                                     igmp host handle
    action:                                     start/stop/join/leave/igmp_send_specific_query
    start_group_addr:                           only used for igmp_send_secific_query
    group_count:                                only used for igmp_send_secific_query
    start_source_addr:                          only used for igmp_send_secific_query
    source_count:                               only used for igmp_send_secific_query
    :return:
    """
    action_param = dict()
    action_param['handle'] = kwargs['handle']
    if 'action' in kwargs:
        action_param['mode'] = kwargs['action']
    if 'start_group_addr' in kwargs:
        action_param['start_group_address'] = kwargs['start_group_addr']
    if 'group_count' in kwargs:
        action_param['group_count'] = kwargs['group_count']
    if 'start_source_addr' in kwargs:
        action_param['start_source_address'] = kwargs['start_source_addr']
    if 'source_count' in kwargs:
        action_param['source_count'] = kwargs['source_count']
    return self.ixiangpf.emulation_igmp_control(**action_param)


def igmp_client_stats(self, **kwargs):
    """
    :param self:                    RT object
    :param kwargs:
    :return:
    """
    pass


def add_addr_custom_pattern(self, **kwargs):
    """
    :param self:
    :param kwargs:
    :return:
    """

    if 'type' not in kwargs:
        ip_type = 'v4'
    else:
        ip_type = kwargs['type']

    _result_ = self.ixiangpf.multivalue_config(pattern="custom")
    print(_result_)
    multivalue_handle = _result_['multivalue_handle']
    if 'v4' in ip_type:
        custom_step = "0.0.0.0"
        custom_start = kwargs.get('start')
        increment_value = kwargs.get('step')

    else:
        custom_step = ipaddress.IPv6Address('::').exploded
        custom_start = ipaddress.IPv6Address(kwargs['start']).exploded
        increment_value = ipaddress.IPv6Address(kwargs['step']).exploded
    _result_ = self.ixiangpf.multivalue_config(
        multivalue_handle=multivalue_handle,
        custom_start=custom_start,
        custom_step=custom_step,
    )
    print(_result_)
    custom_1_handle = _result_['custom_handle']

    _result_ = self.ixiangpf.multivalue_config(
        custom_handle=custom_1_handle,
        custom_increment_value=increment_value,
        custom_increment_count=kwargs.get('count'),
    )
    print(_result_)
    return multivalue_handle


def add_mld_client(self, **kwargs):
    """
    :param self:                     RT object
    :param kwargs:
     handle:                         dhcpv6 client handle
     version:                        version 1 or 2, default is 1
     filter_mode:                    include/exclude, default is include
     iptv:                           1 or 0, default is 0
     group_range:                    multicast group range, default is 1
     group_range_step:               the pattern that the range start address, default is ::1:0
     group_start_addr:               multicast group start address
     group_step:                     group step pattern, default is ::1
     group_count:                    group counts
     src_grp_range:                  multicast source group range, default is 1
     src_grp_range_step:             multicast source group range step pattern, default is ::1:0
     src_grp_start_addr:             multicast source group start address
     src_grp_step:                   multicast soutce group step pattern, default is ::1
     src_grp_count:                  multicast source group count

     :return:
     result                          a dictionary include status, mld_host_handle, mld_group_handle, mld_source_handle
     """
    result = dict()
    result['status'] = '1'
    mld_param = dict()
    mld_param['handle'] = kwargs.get('handle')
    mld_param['mode'] = kwargs.get('mode', 'create')
    mld_param['active'] = kwargs.get('active', '1')
    mld_param['filter_mode'] = kwargs.get('filter_mode', 'include')
    mld_param['enable_iptv'] = kwargs.get('iptv', '0')
    mld_param['mld_version'] = 'v' + str(kwargs.get('version', '1'))

    _result_ = self.ixiangpf.emulation_mld_config(**mld_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to add mld client"
        result['status'] = '0'
        return result
    else:
        mld_handle = _result_['mld_host_handle']
        self.mld_handles[kwargs.get('handle')] = mld_handle
        self.mld_handle_to_group[mld_handle] = {}
        result['mld_host_handle'] = mld_handle

    addr_param = dict()
    addr_param['start'] = ipaddress.IPv6Address(kwargs.get('group_start_addr', 'ff03::1')).exploded
    addr_param['step'] = ipaddress.IPv6Address(kwargs.get('group_range_step', "0:0:0:0:0:0:1:0")).exploded
    addr_param['count'] = kwargs.get('group_range', "1")
    addr_param['type'] = 'v6'
    multivalue_2_handle = self.add_addr_custom_pattern(**addr_param)

    _result_ = self.ixiangpf.emulation_multicast_group_config(
        mode="create",
        ip_addr_start=multivalue_2_handle,
        ip_addr_step=ipaddress.IPv6Address(kwargs.get('group_step', "0:0:0:0:0:0:0:1")).exploded,
        num_groups=kwargs.get('group_count', "1"),
        active=kwargs.get('active', "1")
    )
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        mld_group_handle = _result_['multicast_group_handle']
        self.mld_handle_to_group[mld_handle]['group_handle'] = mld_group_handle

    src_addr_param = dict()
    src_addr_param['start'] = ipaddress.IPv6Address(kwargs.get('src_grp_start_addr', "200::1")).exploded
    src_addr_param['step'] = ipaddress.IPv6Address(kwargs.get('src_grp_range_step', "0:0:0:0:0:0:1:0")).exploded
    src_addr_param['count'] = kwargs.get('src_grp_range', "1")
    src_addr_param['type'] = 'v6'
    multivalue_3_handle = self.add_addr_custom_pattern(**src_addr_param)

    _result_ = self.ixiangpf.emulation_multicast_source_config(
        mode="create",
        ip_addr_start=multivalue_3_handle,
        ip_addr_step=ipaddress.IPv6Address(kwargs.get('src_grp_step', "0:0:0:0:0:0:0:1")).exploded,
        num_sources=kwargs.get('src_grp_count', "1"),
        active="1",
    )
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
    else:
        mld_source_handle = _result_['multicast_source_handle']
        self.mld_handle_to_group[mld_handle]['src_group_handle'] = mld_source_handle
    _result_ = self.ixiangpf.emulation_mld_group_config(
        mode=kwargs.get('mode', "create"),
        g_filter_mode=kwargs.get('filter_mode', "include"),
        group_pool_handle=mld_group_handle,
        no_of_grp_ranges=kwargs.get('group_range', "1"),
        no_of_src_ranges=kwargs.get('src_grp_range', "1"),
        session_handle=mld_handle,
        source_pool_handle=mld_source_handle,
    )
    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to config the mld group and src group set"
    else:
        result['mld_group_handle'] = _result_['mld_group_handle']
        result['mld_source_handle'] = _result_['mld_source_handle']
        self.mld_handle_to_group[mld_handle]['mld_group_handle'] = _result_['mld_group_handle']
        self.mld_handle_to_group[mld_handle]['mld_source_handle'] = _result_['mld_source_handle']

    return result


def set_mld_client(self, **kwargs):
    """
    :param self:                    RT object
    :param kwargs:
    handle:                         mld host handle
    version:                        version 1 or 2, default is 1
    filter_mode:                    include/exclude, default is include
    iptv:                           1 or 0, default is 0
    group_range:                    multicast group range, default is 1
    group_range_step:               the pattern that the range start address, default is ::1:0
    group_start_addr:               multicast group start address
    group_step:                     group step pattern
    group_count:                    group counts
    src_grp_range:                  multicast source group range, default is 1
    src_grp_range_step:             multicast source group range step pattern, default is ::1:0
    src_grp_start_addr:             multicast source group start address
    src_grp_step:                   multicast soutce group step pattern, default is ::1
    src_grp_count:                  multicast source group count


    :return:
    status
    """
    result = dict()
    result['status'] = '1'
    mld_param = dict()
    if 'handle' in kwargs:
        mld_param['handle'] = kwargs.get('handle')
        mld_group_handle = self.mld_handle_to_group[kwargs.get('handle')]['group_handle']
        mld_source_handle = self.mld_handle_to_group[kwargs.get('handle')]['src_group_handle']
    else:
        raise Exception("handle is mandatory for modifying configuration")

    mld_param['mode'] = kwargs.get('mode', 'modify')
    if 'active' in kwargs:
        mld_param['active'] = kwargs.get('active')
    if 'filter_mode' in kwargs:
        mld_param['filter_mode'] = kwargs.get('filter_mode')
    if 'iptv' in kwargs:
        mld_param['enable_iptv'] = kwargs.get('iptv')
    if 'version' in kwargs:
        mld_param['mld_version'] = 'v' + str(kwargs.get('version', '1'))

    _result_ = self.ixiangpf.emulation_mld_config(**mld_param)
    print(_result_)
    if _result_['status'] != '1':
        result['log'] = "failed to set mld client"
        result['status'] = '0'
        return result
    elif mld_param['mode'] == 'delete':
        return result

    if 'group_start_addr' in kwargs:
        addr_param = dict()
        addr_param['start'] = ipaddress.IPv6Address(kwargs['group_start_addr']).exploded
        addr_param['step'] = ipaddress.IPv6Address(kwargs.get('group_range_step', "0:0:0:0:0:0:1:0")).exploded
        addr_param['count'] = kwargs.get('group_range', "1")
        addr_param['type'] = 'ipv6'
        multivalue_2_handle = self.add_addr_custom_pattern(**addr_param)
        group_param = {}
        group_param['mode'] = 'modify'
        group_param['handle'] = mld_group_handle
        group_param['ip_addr_start'] = multivalue_2_handle
        if 'group_step' in kwargs:
            group_param['ip_addr_step'] = ipaddress.IPv6Address(kwargs['group_step']).exploded
        if 'group_count' in kwargs:
            group_param['num_groups'] = kwargs['group_count']
        if 'active' in kwargs:
            group_param['active'] = kwargs['active']
        _result_ = self.ixiangpf.emulation_multicast_group_config(**group_param)

        print(_result_)
        if _result_['status'] != '1':
            result['status'] = '0'

    if 'src_grp_start_addr' in kwargs:
        src_addr_param = dict()
        src_addr_param['start'] = ipaddress.IPv6Address(kwargs.get('src_grp_start_addr', "200::2")).exploded
        src_addr_param['step'] = ipaddress.IPv6Address(kwargs.get('src_grp_range_step', "0:0:0:0:0:0:1:0")).exploded
        src_addr_param['count'] = kwargs.get('src_grp_range', "1")
        src_addr_param['type'] = 'ipv6'
        multivalue_3_handle = self.add_addr_custom_pattern(**src_addr_param)
        src_grp_param = {}
        src_grp_param['mode'] = 'modify'
        src_grp_param['handle'] = mld_source_handle
        src_grp_param['ip_addr_start'] = multivalue_3_handle
        if 'src_grp_step' in kwargs:
            src_grp_param['ip_addr_step'] = ipaddress.IPv6Address(kwargs['src_grp_step']).exploded
        if 'src_grp_count' in kwargs:
            src_grp_param['num_sources'] = kwargs['src_grp_count']
        _result_ = self.ixiangpf.emulation_multicast_source_config(**src_grp_param)

        print(_result_)
        if _result_['status'] != '1':
            result['status'] = '0'
    mld_group_param = {}
    mld_group_param['mode'] = kwargs.get('mode', "modify")
    #based on ixia theresa kong, the handle should be the session handle, others are not needed
    #mld_group_param['handle'] = self.mld_handle_to_group[kwargs['handle']]['mld_group_handle']
    #mld_group_param['session_handle'] = kwargs['handle']
    mld_group_param['handle'] = kwargs['handle']
    mld_group_param['group_pool_handle'] = mld_group_handle
    mld_group_param['source_pool_handle'] = mld_source_handle
    if 'group_range' in kwargs:
        mld_group_param['no_of_grp_ranges'] = kwargs['group_range']
    if 'src_grp_range' in kwargs:
        mld_group_param['no_of_src_ranges'] = kwargs['src_grp_range']
    _result_ = self.ixiangpf.emulation_mld_group_config(**mld_group_param)

    print(_result_)
    if _result_['status'] != '1':
        result['status'] = '0'
        result['log'] = "failed to modify the mld group and src group set"

    return result


def mld_client_action(self, **kwargs):
    """
    :param self:                                RT object
    :param kwargs:
    handle:                                     mld host handle
    action:                                     start/stop/join/leave/mld_send_specific_query
    start_group_addr:                           only used for mld_send_secific_query
    group_count:                                only used for mld_send_secific_query
    start_source_addr:                          only used for mld_send_secific_query
    source_count:                               only used for mld_send_secific_query
    :return:
    """
    action_param = dict()
    action_param['handle'] = kwargs['handle']
    if 'action' in kwargs:
        action_param['mode'] = kwargs['action']
    if 'start_group_addr' in kwargs:
        action_param['start_group_address'] = kwargs['start_group_addr']
    if 'group_count' in kwargs:
        action_param['group_count'] = kwargs['group_count']
    if 'start_source_addr' in kwargs:
        action_param['start_source_address'] = kwargs['start_source_addr']
    if 'source_count' in kwargs:
        action_param['source_count'] = kwargs['source_count']
    return self.ixiangpf.emulation_mld_control(**action_param)


def add_multicast_traffic(self):
    """
    :param self:
    :return:
    """
    pass


def add_application_traffic(self):
    """
    :param self:
    :return:
    """
    pass


def add_bgp(self, **kwargs):
    """

    :param self:
    :param kwargs:
    handle:                     ipv4 handle or ipv6 handle
    type:                       external/internal
    remote_ip:                  neighbor ip address
    local_as:                   Local as number
    hold_time:                  bgp hold time
    restart_time:               bgp restart time
    keepalive:                  bgp keepalive timer
    router_id:                  bgp router id
    stale_time:                 bgp stale time
    enable_flap:                bgp flap enable 1/0
    flap_down_time:             flap down time
    flap_up_time:               flap up time
    graceful_restart:           graceful restart 1/0
    prefix_group:               list of prefixes which was a dictionary include
                                network_prefix:             bgp network prefix
                                network_step:               bgp network prefix increment step
                                network_count:              bgp network counter
                                sub_prefix_length:      network sub prefix length
                                sub_prefix_count:       network sub prefix count

    :return:                    result dictionary: status, bgp_handle, network_group_handle,
    """
    result = dict()
    result['status'] = '1'
    result['network_group_handle'] = []
    bgp_params = dict()
    bgp_params['mode'] = 'enable'
    bgp_params['handle'] = kwargs['handle']
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+', kwargs['handle'])
    deviceGroup_handle = match.group(0)
    bgp_params['neighbor_type'] = kwargs['type']
    bgp_params['local_as'] = kwargs['local_as']
    if 'hold_time' in kwargs:
        bgp_params['hold_time'] = kwargs['hold_time']
    if 'restart_time' in kwargs:
        bgp_params['restart_time'] = kwargs['restart_time']
    if 'keepalive' in kwargs:
        bgp_params['keepalive_timer'] = kwargs['keepalive']
    if 'enable_flap' in kwargs:
        bgp_params['enable_flap'] = kwargs['enable_flap']
        bgp_params['flap_up_time'] = kwargs['flap_up_time']
        bgp_params['flap_down_time'] = kwargs['flap_down_time']
    if 'stale_time' in kwargs:
        bgp_params['stale_time'] = kwargs['stale_time']
    if 'graceful_restart' in kwargs:
        bgp_params['graceful_restart_enable'] = kwargs['graceful_restart']

    if 'v4' in kwargs['handle']:
        bgp_params['ip_version'] = '4'
        bgp_params['remote_ip_addr'] = kwargs['remote_ip']
        if 'router_id' in kwargs:
            bgp_params['router_id'] = kwargs['router_id']
    if 'v6' in kwargs['handle']:
        bgp_params['ip_version'] = '6'
        bgp_params['remote_ipv6_addr'] = kwargs['remote_ip']

    _result_ = self.ixiangpf.emulation_bgp_config(**bgp_params)
    if _result_['status'] == '1':
        bgp_handle = _result_['bgp_handle']
        self.bgp_handle.append(bgp_handle)
        result['bgp_handle'] = bgp_handle
    else:
        return _result_
    for prefix in kwargs['prefix_group']:

        _result_ = self.ixiangpf.multivalue_config(
            pattern="counter",
            counter_start=prefix['network_prefix'],
            counter_step=prefix['network_step'],
            counter_direction="increment",
        )

        multivalue_11_handle = _result_['multivalue_handle']

        network_params = dict()
        network_params['protocol_handle'] = deviceGroup_handle
        if 'network_count' in kwargs:
            network_params['multiplier'] = prefix['network_count']
        network_params['connected_to_handle'] = bgp_handle
        if 'v4' in kwargs['handle']:
            network_params['type'] = "ipv4-prefix"
            network_params['ipv4_prefix_network_address'] = multivalue_11_handle
            network_params['ipv4_prefix_length'] = prefix['sub_prefix_length']
            if 'sub_prefix_count' in prefix:
                network_params['ipv4_prefix_number_of_addresses'] = prefix['sub_prefix_count']
        if 'v6' in kwargs['handle']:
            network_params['type'] = "ipv6-prefix"
            network_params['ipv6_prefix_network_address'] = multivalue_11_handle
            network_params['ipv6_prefix_length'] = prefix['sub_prefix_length']
            if 'sub_prefix_count' in prefix:
                network_params['ipv6_prefix_number_of_addresses'] = prefix['sub_prefix_count']

        _result_ = self.ixiangpf.network_group_config(**network_params)
        if _result_['status'] == '1':
            network_group_handle = _result_['network_group_handle']
            result['network_group_handle'].append(network_group_handle)
        else:
            return _result_
        route_params = dict()
        if 'ipv4_prefix_pools_handle' in _result_:
            prefix_pool_handle = _result_['ipv4_prefix_pools_handle']
            route_params['ip_version'] = '4'
            route_params["ipv4_unicast_nlri"] = "1"
        if 'ipv6_prefix_pools_handle' in _result_:
            prefix_pool_handle = _result_['ipv6_prefix_pools_handle']
            route_params['ip_version'] = '6'
            route_params["ipv6_unicast_nlri"] = "1"
        route_params['handle'] = network_group_handle
        route_params['mode'] = 'create'
        route_params['prefix'] = multivalue_11_handle
        route_params['num_routes'] = prefix.get('sub_prefix_count','1')
        route_params['prefix_from'] = prefix['sub_prefix_length']
        route_params['max_route_ranges'] = prefix.get('network_count', '1')

        _result_ = self.ixiangpf.emulation_bgp_route_config(**route_params)
        if _result_['status'] != '1':
            result['status'] = '0'
    return result


def set_bgp(self, **kwargs):
    """
    :param self:
    :param kwargs:
    handle:
    :return:
    """
    pass

def bgp_action(self, **kwargs):
    """
    :param self:
    :param kwargs:
    handle:                                 bgp session handle
    action:                                 start/stop/restart/abort/restart_down/delete
    :return:
    """
    bgp_params = dict()
    bgp_params['mode'] = kwargs['action']
    bgp_params['handle'] = kwargs['handle']
    if 'delete' in kwargs['action']:
        match = re.match(r'\/topology:\d+\/deviceGroup:\d+', kwargs['handle'])
        deviceGroup_handle = match.group(0)
        self.ixiangpf.test_control(handle=deviceGroup_handle, action='stop_protocol')
        return self.ixiangpf.emulation_bgp_config(handle=kwargs['handle'], mode='delete')

    return self.ixiangpf.emulation_bgp_control(**kwargs)


def add_l2tp_server(self, **kwargs):
    """
    rt.ixiangpf.l2tp_config(mode='lns',port_handle='1/1/3',lns_host_name='ixia_lns',
    tun_auth='authenticate_hostname', secret='ixia', hostname='lac', l2_encap='ethernet_ii_vlan',
    l2tp_dst_addr='10.2.0.2', l2tp_src_addr='10.2.0.1', num_tunnels=1,auth_mode='pap_or_chap',
    username='test', password='pwd', l2tp_src_prefix_len=24)
    :param self:                                            RT object
    :param kwargs:
    port                                port(mandatory)
    tun_auth_enable:                    1 or 0, authentication method for tunnel('authenticate_hostname'/
                                        tunnel_authentication_disabled), default is 1
    tun_secret:                         tunnel secret
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    l2tp_dst_addr:                      l2tp destionation start address(mandatory)
    l2tp_src_addr:                      l2tp source start address(mandatory)
    hostname:                           lac hostname, default is 'lac'
    lns_host_name:                      lns hostname, default is 'ixia_lns'
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    l2tp_src_prefix_len:                l2tp source prefix length, default is 24
    auth_mode:                          authentication mode, none/pap/chap/pap_or_chap, default is none
    username:                           username for authentication
    password:                           password for authentication
    ip_cp:                              ip_cp mode, could be ipv4_cp/ipv6_cp/dual_stack, default is ipv4_cp
    vlan_id:                            interface vlan id
    :return:
    """

    lns_params = dict()
    lns_params['mode'] = 'lns'
    lns_params['num_tunnels'] = '1'
    lns_params['hostname'] = kwargs.get('hostname', 'mx_lac')
    lns_params['lns_host_name'] = kwargs.get('lns_host_name', 'ixia_lns')
    lns_params['vlan_id'] = kwargs.get('vlan_id', '1')
    lns_params['l2_encap'] = 'ethernet_ii_vlan'
    lns_params['port_handle'] = self.port_to_handle_map[kwargs['port']]
    lns_params['l2tp_src_addr'] = kwargs['l2tp_src_addr']
    lns_params['l2tp_dst_addr'] = kwargs['l2tp_dst_addr']
    if int(kwargs.get('tun_auth_enable', '1')):
        lns_params['tun_auth'] = 'authenticate_hostname'
    else:
        lns_params['tun_auth'] = 'tunnel_authentication_disabled'
    lns_params['secret'] = kwargs.get('tun_secret', 'secret')
    lns_params['l2tp_src_prefix_len'] = kwargs.get('l2tp_src_prefix_len', '24')
    lns_params['sessions_per_tunnel'] = kwargs.get('total_sessions', '32000')
    if 'tun_hello_req' in kwargs:
        lns_params['hello_req'] = kwargs['tun_hello_req']
    if 'tun_hello_interval' in kwargs:
        lns_params['hello_interval'] = kwargs['tun_hello_interval']
    if 'username' in kwargs:
        lns_params['username'] = kwargs['username']
    if 'password' in kwargs:
        lns_params['password'] = kwargs['password']
    if 'ip_cp' in kwargs:
        lns_params['ip_cp'] = kwargs['ip_cp']
        if 'dual' in kwargs['ip_cp'] or 'v6' in kwargs['ip_cp']:
            lns_params['dhcpv6_hosts_enable'] = '1'
    lns_params['auth_mode'] = kwargs.get('auth_mode', 'pap_or_chap')
    result = self.ixiangpf.l2tp_config(**lns_params)
    print(result)
    if result['status']:
        self.lns_handle.append(result['lns_handle'])
        self.l2tp_server_session_handle.append(result['pppox_server_sessions_handle'])
        if 'dhcpv6' in result:
            self.dhcpv6_server_handle.append(result['dhcpv6_server_handle'])
    return result


def set_l2tp_server(self, **kwargs):
    """
    can only change the l2tp layer params
    :param self:
    :param kwargs:
    handle:                                 lns handle
    hostname:                               lac hostname
    lns_host_name:                          lns hostname
    tun_auth_enable:                        tunnel authentication
    tun_secret:                             tunnel secret
    l2tp_src_addr:                          l2tp source address
    l2tp_dst_addr:                          l2tp gateway address
    l2tp_src_prefix_len:                    l2tp address prefix length
    :return:
    """
    lns_params = dict()
    lns_params['handle'] = kwargs['handle']
    lns_params['mode'] = 'lns'
    lns_params['action'] = 'modify'
    if 'hostname' in kwargs:
        lns_params['hostname'] = kwargs['hostname']
    if 'lns_host_name' in kwargs:
        lns_params['lns_host_name'] = kwargs['lns_host_name']
    if 'l2tp_src_addr' in kwargs:
        lns_params['l2tp_src_addr'] = kwargs['l2tp_src_addr']
    if 'l2tp_dst_addr' in kwargs:
        lns_params['l2tp_dst_addr'] = kwargs['l2tp_dst_addr']
    if 'tun_auth_enable' in kwargs:
        if kwargs['tun_auth_enable']:
            lns_params['tun_auth'] = 'authenticate_hostname'
        else:
            lns_params['tun_auth'] = 'tunnel_authentication_disabled'
    if 'tun_secret' in kwargs:
        lns_params['secret'] = kwargs['tun_secret']
    if 'l2tp_addr_mask' in kwargs:
        lns_params['l2tp_src_prefix_len'] = kwargs['l2tp_addr_mask']

    return self.ixiangpf.l2tp_config(**lns_params)


def l2tp_server_action(self, **kwargs):
    """
    :param self:
    :param kwargs:
    handle:                     lns handle
    action:                     start/stop
    :return:
    """
    param = dict()
    handle = kwargs['handle']
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+', kwargs['handle'])
    param['handle'] = match.group(0)
    param['action'] = kwargs['action']
    return self.ixiangpf.test_control(**param)


def add_l2tp_client(self, **kwargs):
    """
    maximum sessions per port is 32000
    :param self:                        RT Object from toby
    :param kwargs:
    port                                tester port(mandatory)
    num_tunnels_per_lac:                number of tunnels configured per LAC
    sessions_per_tunnel:                sessions per LAC, default is 5
    tun_auth_enable:                    1 or 0,       authentication method for tunnel('authenticate_hostname'/
                                        tunnel_authentication_disabled), default is 1
    tun_secret:                         tunnel secret
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    tun_hello_interval:                 tunnel hello interval, valid only when tun_hello_req is 1
    echo_req:                           enable/disable ppp keepalive request by RT
    echo_req_interval:                  ppp keepalive request interval
    l2tp_dst_addr:                      l2tp destionation start address, default is '100.0.0.1'
    l2tp_src_addr:                      l2tp source start address(mandatory)
    hostname:                           lac hostname, default is 'lac'
    l2tp_src_count:                     l2tp source address counts(same as lac count), default is 1
    l2tp_src_step:                      l2tp source address step, default is 0.0.1.0
    l2tp_src_gw:                        l2tp source gateway(mandatory)
    l2tp_src_gw_step:                   l2tp source gateway step, default is 0.0.1.0
    l2tp_src_prefix_len:                l2tp source prefix length, default is 24
    l2tp_dst_step:                      l2tp destintion address step
    vlan_id:                            start vlan id for the connection, default is 1
    vlan_id_step:                       vlan id step, default is 1
    auth_mode:                          authentication mode, none/pap/chap/pap_or_chap, default is none
    username:                           username for authentication
    password:                           password for authentication
    ip_cp:                              ip_cp mode, could be ipv4_cp/ipv6_cp/dual_stack, default is ipv4_cp
    dhcpv6_ia_type:                     can be iana/iapd/iana_iapd, default is iapd
    #domain_name:                        domain name, (eg. if you set this to abc?.com, the domain name will increase
                                        from 1, and repeat sessions_per_tunnel)
    :return:                            dictionary of status , ethernet_handle, ipv4_handle, lac_handle,
                                        pppox_client_handle, dhcpv6_client_handle
    """
    # rt.ixiangpf.l2tp_config(port_handle='1/1/2', num_tunnels='500', mode='lac', l2tp_dst_addr='100.0.0.3',
    #                         l2tp_src_addr='10.200.0.2', tun_auth='authenticate_hostname', sessions_per_tunnel='6',
    #                         l2_encap='ethernet_ii_vlan', hostname='lac{Inc:1,,,1}', l2tp_src_count=10,
    #                         l2tp_src_step='0.0.1.0', vlan_id='1', vlan_id_step='1', l2tp_src_gw='10.200.0.1',
    #                         l2tp_src_gw_step='0.0.1.0', l2tp_src_prefix_len='24', auth_mode='pap_or_chap',
    #                           username='DEFAULTUSER', password='passwd')

    lac_params = dict()
    lac_params['mode'] = 'lac'
    lac_params['vlan_id'] = kwargs.get('vlan_id', '1')
    lac_params['vlan_id_step'] = kwargs.get('vlan_id_step', '1')
    lac_params['l2_encap'] = 'ethernet_ii_vlan'
    lac_params['port_handle'] = self.port_to_handle_map[kwargs['port']]
    if int(kwargs.get('tun_auth_enable', '1')):
        lac_params['tun_auth'] = 'authenticate_hostname'
    else:
        lac_params['tun_auth'] = 'tunnel_authentication_disabled'
    if 'tun_secret' in kwargs:
        lac_params['secret'] = kwargs['tun_secret']
    lac_params['num_tunnels'] = kwargs.get('num_tunnels_per_lac', '1')
    lac_params['sessions_per_tunnel'] = kwargs.get('sessions_per_tunnel', '5')
    lac_params['l2tp_dst_addr'] = kwargs.get('l2tp_dst_addr', '100.0.0.1')
    lac_params['l2tp_src_addr'] = kwargs['l2tp_src_addr']
    lac_params['l2tp_src_gw'] = kwargs['l2tp_src_gw']
    lac_params['l2tp_src_count'] = kwargs.get('l2tp_src_count', '1')
    lac_params['l2tp_src_step'] = kwargs.get('l2tp_src_step', '0.0.1.0')
    lac_params['l2tp_src_gw_step'] = kwargs.get('l2tp_src_gw_step', lac_params['l2tp_src_step'])
    lac_params['l2tp_src_prefix_len'] = kwargs.get('l2tp_src_prefix_len', '24')
    lac_params['hostname'] = kwargs.get('hostname', 'lac')
    if 'echo_req' in kwargs:
        lac_params['echo_req'] = kwargs['echo_req']
        if 'echo_req_interval' in kwargs:
            lac_params['echo_req_interval'] = kwargs['echo_req_interval']
    if 'mode' in kwargs:
        lac_params['action'] = kwargs['mode']
    #lac_params['tun_distribution'] = kwargs.get('tun_distribution', 'next_tunnelfill_tunnel')
    if 'tun_hello_req' in kwargs:
        lac_params['hello_req'] = kwargs['tun_hello_req']
        if 'tun_hello_interval' in kwargs:
            lac_params['hello_interval'] = kwargs['tun_hello_interval']
    if 'l2tp_dst_step' in kwargs:
        lac_params['l2tp_dst_step'] = kwargs['l2tp_dst_step']
    if 'ip_cp' in kwargs:
        lac_params['ip_cp'] = kwargs['ip_cp']
        if 'ipv6' in kwargs['ip_cp'] or 'dual' in kwargs['ip_cp']:
            lac_params['dhcpv6_hosts_enable'] = '1'
            lac_params['dhcp6_pd_client_range_ia_type'] = kwargs.get('dhcpv6_ia_type', 'iapd')

    lac_params['auth_mode'] = kwargs.get('auth_mode', 'none')

    if 'username' in kwargs:
        lac_params['username'] = kwargs['username']
        if '?' in lac_params['username']:
            increment = '{Inc:' + '1,,,' + str(lac_params['sessions_per_tunnel']) +'}'
            lac_params['username'] = kwargs['username'].replace('?', increment)
    if 'password' in kwargs:
        lac_params['password'] = kwargs['password']

    if int(lac_params['l2tp_src_count']) > 1:
        ##increase the lac hostname
        lac_params['hostname'] = lac_params['hostname'] + '{Inc:1,,,' + str(lac_params['num_tunnels']) + '}'
        _result_ = self.ixiangpf.multivalue_config(
            pattern="counter",
            counter_start="1701",
            counter_step="1",
            counter_direction="increment"
        )
        lac_params['udp_src_port'] = _result_['multivalue_handle']

    result = self.ixiangpf.l2tp_config(**lac_params)
    if result['status'] == '1':
        self.lac_handle.append(result['lac_handle'])
        if 'dhcpv6_client_handle' in result:
            self.dhcpv6_client_handle.append(result['dhcpv6_client_handle'])
            self.l2tp_client_handle.append(result['dhcpv6_client_handle'])
        else:
            self.l2tp_client_handle.append(result['pppox_client_handle'])
        self.pppox_client_handle.append(result['pppox_client_handle'])
    return result


def set_l2tp_client(self, **kwargs):
    """
    only lac params can be modified
    :param self:                        RT Object from toby
    :param kwargs:
    handle                              lac handle(mandatory)
    num_tunnels_per_lac:                number of tunnels configured per LAC
    sessions_per_tunnel:                sessions per LAC, default is 5
    tun_auth:                           authentication method for tunnel('authenticate_hostname'/
                                        tunnel_authentication_disabled), default is authenticate_hostname
    tun_secret:                         tunnel secret
    tun_hello_req:                      send tunnel hello request , value could be 1/0
    tun_hello_interval:                 Tunnel hello interval, valid when tun_hello_req is 1
    l2tp_dst_addr:                      l2tp destionation start address, default is '100.0.0.1'
    l2tp_src_addr:                      l2tp source start address(mandatory)
    hostname:                           lac hostname, default is 'lac'
    l2tp_src_count:                     l2tp source address counts(same as lac count), default is 1
    l2tp_src_step:                      l2tp source address step, default is 0.0.1.0
    l2tp_src_gw:                        l2tp source gateway(mandatory)
    l2tp_src_gw_step:                   l2tp source gateway step, default is 0.0.1.0
    l2tp_src_prefix_len:                l2tp source prefix length, default is 24
    l2tp_dst_step:                      l2tp destintion address step

    :return:                            dictionary of status and info
    """
    lac_params = dict()
    lac_params['mode'] = 'lac'
    lac_params['action'] = 'modify'
    lac_params['handle'] = kwargs['handle']
    if 'tun_auth_enable' in kwargs:
        if int(kwargs['tun_auth_enable']):
            lac_params['tun_auth'] = 'authenticate_hostname'
        else:
            lac_params['tun_auth'] = 'tunnel_authentication_disabled'
    if 'secret' in kwargs:
        lac_params['secret'] = kwargs['tun_secret']
    if 'num_tunnels_per_lac' in kwargs:
        lac_params['num_tunnels'] = kwargs['num_tunnels_per_lac']
    if 'sessions_per_tunnel' in kwargs:
        lac_params['sessions_per_tunnel'] = kwargs['sessions_per_tunnel']
    if 'l2tp_dst_addr' in kwargs:
        lac_params['l2tp_dst_addr'] = kwargs['l2tp_dst_addr']
    if 'l2tp_src_addr' in kwargs:
        lac_params['l2tp_src_addr'] = kwargs['l2tp_src_addr']
    if 'l2tp_src_gw' in kwargs:
        lac_params['l2tp_src_gw'] = kwargs['l2tp_src_gw']
    if 'l2tp_src_count' in kwargs:
        lac_params['l2tp_src_count'] = kwargs['l2tp_src_count']
    if 'l2tp_src_step' in kwargs:
        lac_params['l2tp_src_step'] = kwargs['l2tp_src_step']
    if 'l2tp_src_gw_step' in kwargs:
        lac_params['l2tp_src_gw_step'] = kwargs['l2tp_src_gw_step']
    if 'l2tp_src_prefix_len' in kwargs:
        lac_params['l2tp_src_prefix_len'] = kwargs['l2tp_src_prefix_len']
    if 'hostname' in kwargs:
        lac_params['hostname'] = kwargs['hostname']
        if int(lac_params['num_tunnels']) > 1:
            ##increase the lac hostname
            lac_params['hostname'] = lac_params['hostname'] + '{Inc:1,,,' + str(lac_params['num_tunnels']) + '}'
    if 'mode' in kwargs:
        lac_params['action'] = kwargs['mode']
    #lac_params['tun_distribution'] = kwargs.get('tun_distribution', 'next_tunnelfill_tunnel')
    if 'tun_hello_req' in kwargs:
        lac_params['hello_req'] = kwargs['tun_hello_req']
    if 'tun_hello_interval' in kwargs:
        lac_params['hello_interval'] = kwargs['tun_hello_interval']
    if 'l2tp_dst_step' in kwargs:
        lac_params['l2tp_dst_step'] = kwargs['l2tp_dst_step']
    if 'auth_mode' in kwargs:
        lac_params['auth_mode'] = kwargs['auth_mode']

    if 'udp_src_port' in kwargs:
        _result_ = self.ixiangpf.multivalue_config(
            pattern="counter",
            counter_start="1701",
            counter_step="1",
            counter_direction="increment"
        )
        lac_params['udp_src_port'] = _result_['multivalue_handle']

    return self.ixiangpf.l2tp_config(**lac_params)


def l2tp_client_action(self, **kwargs):
    """
    :param self:                            RT object
    :param kwargs:
    handle:                                 l2tp client handle(pppox client handle/dhcpv6 client handle)
    action:                                 start/stop/abort/restart_down
    :return:                                status dictionary
    """
    param = dict()
    handle = kwargs['handle']
    match = re.match(r'\/topology:\d+\/deviceGroup:\d+\/deviceGroup:\d+', kwargs['handle'])
    print(match)
    param['handle'] = match.group(0)
    if 'restart' in kwargs['action']:
        param['action'] = 'restart_down'
    elif 'start' in kwargs['action']:
        param['action'] = 'start_protocol'
    elif 'stop' in kwargs['action']:
        param['action'] = 'stop_protocol'
    elif 'abort' in kwargs['action']:
        param['action'] = 'abort_protocol'
    return self.ixiangpf.test_control(**param)


def l2tp_client_stats(self, **kwargs):
    """

    :param self:
    :param kwargs:
    handle:                             l2tp client handle/ pppox client handle/ dhcpv6 client handle
    mode:                               aggregate/session/tunnel/session_all/session_dhcpv6pd
    :return:
    """
    if 'lac' in kwargs['handle']:
        return self.ixiangpf.l2tp_stats(**kwargs)
    elif 'dhcpv6' in kwargs['handle']:
        return self.dhcp_client_stats(handle=kwargs['handle'], mode='aggregate_stats')
    elif 'pppox' in kwargs['handle']:
        return self.pppoe_client_stats(**kwargs)

def add_dhcp_server(self, **kwargs):
    """
    :param self                            RT object
    :param kwargs:
    handle:                                ipv4 handle or ipv6 handle
    pool_size:                             server pool size
    pool_start_addr:                       pool start address
    pool_mask_length:                      pool prefix length
    pool_gateway:                          pool gateway address
    lease_time                             pool address lease time
    dhcpv6_ia_type:                        v6 IA type "iana, iapd, iana+iapd"
    pool_prefix_start:                     v6 PD start prefix
    pool_prefix_length:                    v6 prefix length
    pool_prefix_size:                      v6 prefix pool size

    # use_rapid_commit                       = "0",
    # subnet_addr_assign                     = "0",
    # subnet                                 = "relay",

    :param kwargs:
    :return:
    a dictionary of status dhcpv4_server_handle dhcpv6_server_handle
    """
    result = dict()
    result['status'] = '1'
    if 'handle' not in kwargs:
        raise Exception("ip handle must be provided ")
    dhcp_args = dict()
    dhcp_args['handle'] = kwargs['handle']
    dhcp_args['mode'] = 'create'
    if 'lease_time' in kwargs:
        dhcp_args['lease_time'] = kwargs['lease_time']
    if 'pool_start_addr' in kwargs:
        dhcp_args['ipaddress_pool'] = kwargs['pool_start_addr']
    if 'pool_mask_length' in kwargs:
        dhcp_args['ipaddress_pool_prefix_length'] = kwargs['pool_mask_length']
    if 'pool_size' in kwargs:
        dhcp_args['ipaddress_count'] = kwargs['pool_size']
    if 'pool_gateway' in kwargs:
        dhcp_args['dhcp_offer_router_address'] = kwargs['pool_gateway']
    if 'v4' in kwargs['handle']:
        dhcp_args['ip_version'] = '4'

    if 'v6' in kwargs['handle']:
        dhcp_args['ip_version'] = '6'
        if 'dhcpv6_ia_type' in kwargs:
            dhcp_args['dhcp6_ia_type'] = kwargs['dhcpv6_ia_type']
        if 'pool_prefix_start' in kwargs:
            dhcp_args['start_pool_prefix'] = kwargs['pool_prefix_start']
        if 'pool_prefix_length' in kwargs:
            dhcp_args['prefix_length'] = kwargs['pool_prefix_length']
        if 'pool_prefix_size' in kwargs:
            dhcp_args['pool_prefix_size'] = kwargs['pool_prefix_size']
    config_status = self.ixiangpf.emulation_dhcp_server_config(**dhcp_args)
    if config_status['status'] != '1':
        result['status'] = '0'
    else:
        if dhcp_args['ip_version'] == "4":
            self.dhcpv4_server_handle.append(config_status['dhcpv4server_handle'])
            result['dhcpv4_server_handle'] = config_status['dhcpv4server_handle']
        else:
            self.dhcpv6_server_handle.append(config_status['dhcpv6server_handle'])
            result['dhcpv6_server_handle'] = config_status['dhcpv6server_handle']
    return result


def set_dhcp_server(self, **kwargs):
    """
    change the dhcp server setting
    :param self:                    RT object
    :param kwargs:
    :return:
    status
    """
    config_status = self.ixiangpf.emulation_dhcp_server_config(**kwargs)
    print(config_status)
    return config_status['status']


def dhcp_server_action(self, **kwargs):
    """
    :param self:                    RT object
    :param kwargs:
     handle:                        dhcp server handle
     action:                        'start' or stop
    :return:
     status
    """
    dhcp_args = dict()
    if 'handle' in kwargs:
        dhcp_args['handle'] = kwargs['handle']
    if 'action' in kwargs:
        if 'start' in kwargs['action']:
            dhcp_args['action'] = 'start_protocol'
        if 'stop' in kwargs['action']:
            dhcp_args['action'] = 'stop_protocol'
    result = self.ixiangpf.test_control(**dhcp_args)
    return result['status']


def traffic_simulation(self, **kwargs):
    """
    simulation traffic
    :param self:
    src_port:                            source port
    dst_port:                            destination port
    encap_pppoe:                         pppoe simulation
    l3_protocol:                         ipv4/ipv6
    l4_protocol:                         icmp/igmp/ip/dhcp/udp/gre/tcp
    frame_size:                          frame size
    rate_pps:                            rate in pps
    rate_bps:                            rate in bps
    rate_percent:                        rate in percent
    message_type:                        message type used by igmp/dhcp
    vlan_id:                             start vlan id
    vlan_step:                           vlan step mode
    vlan_count:                          vlan counts
    svlan_id:                            start svlan id
    svlan_step:                          svlan step mode
    svlan_count:                         svlan counts
    src_mac:                             source mac address
    src_mac_step:                        source mac step
    src_mac_count:                       source mac count
    dst_mac:                             destination mac address
    dst_mac_step:                        destination mac step
    dst_mac_count:                       destination mac count
    src_ip:                              source ipv4 address
    src_ip_step:                         source ipv4 address step
    src_ip_count:                        source ipv4 count
    dst_ip:                              destination ipv4 address
    dst_ip_step:                         destination ipv4 address step
    dst_ip_count:                        destination ipv4 count
    src_ipv6:                            source ipv6 address
    src_ipv6_step:                       source ipv6 address step
    src_ipv6_count:                      source ipv6 address count
    dst_ipv6:                            destination ipv6 address
    dst_ipv6_step:                       destination ipv6 address step
    dst_ipv6_count:                      destination ipv6 address count
    :param kwargs:
    :return: result:                     dictionary of status/stream_id/traffic_item
    """
    traffic_args = dict()
    pppoe_args = dict()
    stack_index = 1
    traffic_args['traffic_generator'] = 'ixnetwork_540'
    traffic_args['circuit_type'] = 'raw'
    traffic_args['track_by'] = 'traffic_item'
    traffic_args['emulation_dst_handle'] = self.port_to_handle_map[kwargs['dst_port']]
    traffic_args['emulation_src_handle'] = self.port_to_handle_map[kwargs['src_port']]
    traffic_args['mode'] = 'create'
    traffic_args['frame_size'] = kwargs.get('frame_size', '1000')
    if 'rate_pps' in kwargs:
        traffic_args['rate_pps'] = kwargs['rate_pps']
    if 'rate_bps' in kwargs:
        traffic_args['rate_bps'] = kwargs['rate_bps']
    if 'rate_percent' in kwargs:
        traffic_args['rate_percent'] = kwargs['rate_percent']

    if 'vlan_id' in kwargs:
        stack_index += 1
        traffic_args['vlan'] = 'enable'
        traffic_args['vlan_id'] = kwargs['vlan_id']
        if 'vlan_step' in kwargs:
            traffic_args['vlan_id_step'] = kwargs['vlan_step']
        if 'vlan_count' in kwargs:
            traffic_args['vlan_id_count'] = kwargs['vlan_count']
        if 'svlan_id' in kwargs:
            traffic_args['vlan_id'] = [kwargs['svlan_id'], kwargs['vlan_id']]
            if 'svlan_step' in kwargs or 'vlan_step' in kwargs:
                traffic_args['vlan_id_step'] = [kwargs.get('svlan_step', 1), kwargs.get('vlan_step', 1)]
            if 'svlan_count' in kwargs or 'vlan_count' in kwargs:
                traffic_args['vlan_id_count'] = [kwargs.get('svlan_count', 1), kwargs.get('vlan_count', 1)]

    if 'src_mac' in kwargs:
        traffic_args['mac_src'] = kwargs['src_mac']
        if 'src_mac_step' in kwargs:
            traffic_args['mac_src_mode'] = 'increase'
            traffic_args['mac_src_step'] = kwargs['src_mac_step']
            traffic_args['mac_src_count'] = kwargs.get('src_mac_count', 1)
    if 'dst_mac' in kwargs:
        traffic_args['mac_dst'] = kwargs['dst_mac']
        if 'dst_mac_step' in kwargs:
            traffic_args['mac_dst_mode'] = 'increase'
            traffic_args['mac_dst_step'] = kwargs['dst_mac_step']
            traffic_args['mac_dst_count'] = kwargs.get('dst_mac_count', 1)
    if 'pppoe_encap' in kwargs and kwargs['pppoe_encap']:
        result = self.ixiangpf.traffic_config(**traffic_args)
        stack_index += 1
        if result['status'] != '1':
            return result
        else:
            traffic_handle = result['stream_id']
            stream_id = result['traffic_item']
            pppoe_args['mode'] = 'modify_or_insert'
            pppoe_args['traffic_generator'] = 'ixnetwork_540'
            pppoe_args['stream_id'] = stream_id
            pppoe_args['stack_index'] = stack_index
            pppoe_args['pt_handle'] = 'pppoESession'
            result = self.ixiangpf.traffic_config(**pppoe_args)
            if result['status'] != '1':
                return result
            pppoe_args.pop('pt_handle')
    if 'src_ip' in kwargs:
        traffic_args['ip_src_addr'] = kwargs['src_ip']
        if 'src_ip_step' in kwargs:
            traffic_args['ip_src_mode'] = 'increase'
            traffic_args['ip_src_step'] = kwargs['src_ip_step']
            traffic_args['ip_src_count'] = kwargs.get('src_ip_count', 1)

    if 'src_ipv6' in kwargs:
        traffic_args['ipv6_src_addr'] = kwargs['src_ipv6']
        pppoe_args['ipv6_src_addr'] = kwargs['src_ipv6']
        if 'src_ipv6_step' in kwargs:
            traffic_args['ipv6_src_mode'] = 'increase'
            traffic_args['ipv6_src_step'] = kwargs['src_ipv6_step']
            traffic_args['ipv6_src_count'] = kwargs.get('src_ipv6_count', 1)
            pppoe_args['ipv6_src_mode'] = 'increase'
            pppoe_args['ipv6_src_step'] = kwargs['src_ipv6_step']
            pppoe_args['ipv6_src_count'] = kwargs.get('src_ipv6_count', 1)
    if 'dst_ip' in kwargs:
        traffic_args['ip_dst_addr'] = kwargs['dst_ip']
        if 'dst_ip_step' in kwargs:
            traffic_args['ip_dst_mode'] = 'increase'
            traffic_args['ip_dst_step'] = kwargs['dst_ip_step']
            traffic_args['ip_dst_count'] = kwargs.get('dst_ip_count', 1)
    if 'dst_ipv6' in kwargs:
        traffic_args['ipv6_dst_addr'] = kwargs['dst_ipv6']
        pppoe_args['ipv6_dst_addr'] = kwargs['dst_ipv6']
        if 'dst_ipv6_step' in kwargs:
            traffic_args['ipv6_dst_mode'] = 'increase'
            traffic_args['ipv6_dst_step'] = kwargs['dst_ipv6_step']
            traffic_args['ipv6_dst_count'] = kwargs.get('dst_ipv6_count', 1)
            pppoe_args['ipv6_dst_mode'] = 'increase'
            pppoe_args['ipv6_dst_step'] = kwargs['dst_ipv6_step']
            pppoe_args['ipv6_dst_count'] = kwargs.get('dst_ipv6_count', 1)

    if 'l4_protocol' in kwargs:
        traffic_args['l4_protocol'] = kwargs['l4_protocol']
    if 'l3_protocol' in kwargs:
        traffic_args['l3_protocol'] = kwargs['l3_protocol']
        pppoe_args['l3_protocol'] = kwargs['l3_protocol']

    if 'pppoe_encap' in kwargs and kwargs['pppoe_encap']:
        if 'l3_protocol' in kwargs and 'v6' in kwargs['l3_protocol']:
            stack_index += 1
            pppoe_args['stack_index'] = stack_index
            ###l3 length = frame_size - pppoe header(8)-ethernet(14)-vlan(4/8)-CRC(4)
            if 'svlan_id' in kwargs:
                pppoe_args['l3_length'] = int(kwargs['frame_size']) - 34
            elif 'vlan_id' in kwargs:
                pppoe_args['l3_length'] = int(kwargs['frame_size']) - 30
            else:
                pppoe_args['l3_length'] = int(kwargs['frame_size']) - 26
            result = self.ixiangpf.traffic_config(**pppoe_args)
            if result['status'] != '1':
                self.traffic_action(handle=traffic_handle, action='delete')
                return result
            else:
                self.traffic_item.append(result['stream_id'])
                traffic_handle = result['stream_id']
                stream_id = result['traffic_item']
                headers = result[stream_id]['headers'].split(' ')
    else:
        result = self.ixiangpf.traffic_config(**traffic_args)
        if result['status'] != '1':
            return result
        else:
            self.traffic_item.append(result['stream_id'])
            stream_id = result['traffic_item']
            headers = result[stream_id]['headers'].split(' ')
    if 'l4_protocol' in kwargs and 'icmp' in kwargs['l4_protocol']:
        if 'pppoe_encap' in kwargs and kwargs['pppoe_encap']:
            stack_index += 1
            icmp_args = dict()
            icmp_args['traffic_generator'] = 'ixnetwork_540'
            icmp_args['mode'] = 'modify_or_insert'
            icmp_args['stream_id'] = stream_id
            icmp_args['stack_index'] = stack_index
            icmp_args['pt_handle'] = 'icmpv6'
            result = self.ixiangpf.traffic_config(**icmp_args)
            if result['status'] != '1':
                self.traffic_action(handle=traffic_handle, action='delete')
                return result
            else:
                headers = result[stream_id]['headers'].split(' ')

        if 'message_type' in kwargs and 'echo_req' in kwargs['message_type']:
            field_handle = "icmpv6.icmpv6Message.icmpv6MessegeType.echoRequestMessage.code-18"
        if 'message_type' in kwargs and 'echo_reply' in kwargs['message_type']:
            field_handle = "icmpv6.icmpv6Message.icmpv6MessegeType.echoReplyMessage.messageType-22"
        if 'message_type' in kwargs:
            result = self.ixiangpf.traffic_config(mode='set_field_values', traffic_generator='ixnetwork_540',
                                     pt_handle='icmpv6', header_handle=headers[-2], field_handle=field_handle,
                                     field_activeFieldChoice='1')
        if result['status'] != '1':
            self.traffic_action(handle=result['stream_id'], action='delete')
            return result

    return result

