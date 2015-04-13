#!/usr/bin/python3

import dbus

system_bus = dbus.SystemBus()
object_path = '/org/freedesktop/UDisks2/drives/Lexar_USB_Flash_Drive_AA95BA6ORWWKIB8O'
well_known_name = 'org.freedesktop.UDisks2'

properties_interface = 'org.freedesktop.DBus.Properties'

main_object_interface = 'org.freedesktop.DBus.ObjectManager'
main_object_path = '/org/freedesktop/UDisks2' # implements interface

global_state_interface = 'org.freedesktop.UDisks2.Manager'
global_state_object_path = '/org/freedesktop/UDisks2/Manager' # implements interface

file_system_interface = 'org.freedesktop.UDisks2.Filesystem'

introspection_interface = 'org.freedesktop.DBus.Introspectable'

# Eject, PowerOff
disk_drive_interface = 'org.freedesktop.UDisks2.Drive'
# Format
block_device_interface = 'org.freedesktop.UDisks2.Drive'

main_object_proxy = system_bus.get_object(well_known_name,
                                          main_object_path)

object_manager = dbus.Interface(main_object_proxy, main_object_interface)

diskproxy = system_bus.get_object(well_known_name,
                                  object_path)

# result = diskproxy.Mount(dbus_interface=file_system_interface)

# result = dir(diskproxy)

# ['DeferredMethodClass', 'INTROSPECT_STATE_DONT_INTROSPECT',
# 'INTROSPECT_STATE_INTROSPECT_DONE',
# 'INTROSPECT_STATE_INTROSPECT_IN_PROGRESS', 'ProxyMethodClass',
# '_Introspect', '__class__', '__dbus_object_path__', '__delattr__',
# '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
# '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__',
# '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
# '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
# '__subclasshook__', '__weakref__', '_bus',
# '_introspect_add_to_queue', '_introspect_block',
# '_introspect_error_handler', '_introspect_execute_queue',
# '_introspect_lock', '_introspect_method_map',
# '_introspect_reply_handler', '_introspect_state', '_named_service',
# '_pending_introspect', '_pending_introspect_queue',
# '_requested_bus_name', 'bus_name', 'connect_to_signal',
# 'get_dbus_method', 'object_path', 'requested_bus_name']

# result = main_object_proxy.Introspect(dbus_interface=introspection_interface)

managed_objects = object_manager.GetManagedObjects()

for k, v in managed_objects.items():
    if k == object_path:
        print('oi--------------')
        print(
        for ke, va in v.items():
            print(va)
            for key, val in va.items():
                print(key)


# print(result)
# props = diskproxy.getProperties(dbus_interface='org.freedesktop.UDisks2'
