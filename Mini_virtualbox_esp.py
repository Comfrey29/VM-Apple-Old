#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
cmd = "/home/usuari/qemu-1.7.7/qemu-system-i386 -m 1024 -hda macosx.img -boot c"
os.system(cmd)
import sys
import subprocess

def ejecutar_comando(comando):
    try:
        proc = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    except Exception, e:
        return -1, '', 'Excepción: ' + str(e)

def comprobar_vboxmanage():
    codigo, _, _ = ejecutar_comando(['which', 'VBoxManage'])
    if codigo != 0:
        print "Error: VBoxManage no está disponible en el PATH."
        sys.exit(1)

def existe_vm(nombre_vm):
    codigo, salida, err = ejecutar_comando(['VBoxManage', 'list', 'vms'])
    if codigo != 0:
        print "Error listando máquinas virtuales:", err
        sys.exit(1)
    return nombre_vm in salida

def crear_vm(nombre_vm):
    print "Creando VM:", nombre_vm
    codigo, _, err = ejecutar_comando(['VBoxManage', 'createvm', '--name', nombre_vm, '--register'])
    if codigo != 0:
        print "Error creando VM:", err
        sys.exit(1)

    codigo, _, err = ejecutar_comando(['VBoxManage', 'modifyvm', nombre_vm, '--memory', '1024', '--acpi', 'on', '--boot1', 'dvd'])
    if codigo != 0:
        print "Error modificando VM:", err
        sys.exit(1)

    codigo, _, err = ejecutar_comando(['VBoxManage', 'storagectl', nombre_vm, '--name', 'IDE Controller', '--add', 'ide'])
    if codigo != 0:
        print "Error creando controlador IDE:", err
        sys.exit(1)

    codigo, _, err = ejecutar_comando(['VBoxManage', 'storageattach', nombre_vm,
                                       '--storagectl', 'IDE Controller',
                                       '--port', '0', '--device', '0',
                                       '--type', 'dvddrive', '--medium', 'emptydrive'])
    if codigo != 0:
        print "Error asignando unidad DVD vacía:", err
        sys.exit(1)

def asignar_iso(nombre_vm, ruta_iso):
    print "Asignando ISO:", ruta_iso
    codigo, _, err = ejecutar_comando(['VBoxManage', 'storageattach', nombre_vm,
                                       '--storagectl', 'IDE Controller',
                                       '--port', '0', '--device', '0',
                                       '--type', 'dvddrive', '--medium', ruta_iso])
    if codigo != 0:
        print "Error asignando ISO:", err
        sys.exit(1)

def iniciar_vm(nombre_vm):
    print "Iniciando VM:", nombre_vm
    codigo, _, err = ejecutar_comando(['VBoxManage', 'startvm', nombre_vm, '--type', 'gui'])
    if codigo != 0:
        print "Error iniciando VM:", err
        sys.exit(1)

def ayuda():
    print """
Uso: %s <Nombre_VM> <Ruta_a_ISO>

Este script crea (si no existe), asigna la ISO e inicia la VM.
""" % sys.argv[0]

def main():
    if len(sys.argv) != 3:
        ayuda()
        sys.exit(1)

    comprobar_vboxmanage()

    nombre_vm = sys.argv[1]
    ruta_iso = sys.argv[2]

    if not os.path.isfile(ruta_iso):
        print "Error: La ISO indicada no existe:", ruta_iso
        sys.exit(1)

    if not existe_vm(nombre_vm):
        crear_vm(nombre_vm)
    else:
        print "La VM '%s' ya existe. Reutilizándola." % nombre_vm

    asignar_iso(nombre_vm, ruta_iso)
    iniciar_vm(nombre_vm)

if __name__ == '__main__':
    main()
