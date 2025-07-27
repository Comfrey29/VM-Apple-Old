#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
cmd = "/home/usuari/qemu-1.7.7/qemu-system-i386 -m 1024 -hda macosx.img -boot c"
os.system(cmd)
import sys
import subprocess

def executar_comanda(comanda):
    try:
        proc = subprocess.Popen(comanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
    except Exception, e:
        return -1, '', 'Exception: ' + str(e)

def comprovar_vboxmanage():
    codi, _, _ = executar_comanda(['which', 'VBoxManage'])
    if codi != 0:
        print "Error: VBoxManage no està disponible al PATH."
        sys.exit(1)

def existeix_vm(nom_vm):
    codi, sortida, err = executar_comanda(['VBoxManage', 'list', 'vms'])
    if codi != 0:
        print "Error llistant màquines virtuals:", err
        sys.exit(1)
    return nom_vm in sortida

def crear_vm(nom_vm):
    print "Creant VM:", nom_vm
    codi, _, err = executar_comanda(['VBoxManage', 'createvm', '--name', nom_vm, '--register'])
    if codi != 0:
        print "Error creant VM:", err
        sys.exit(1)

    codi, _, err = executar_comanda(['VBoxManage', 'modifyvm', nom_vm, '--memory', '1024', '--acpi', 'on', '--boot1', 'dvd'])
    if codi != 0:
        print "Error modificant VM:", err
        sys.exit(1)

    codi, _, err = executar_comanda(['VBoxManage', 'storagectl', nom_vm, '--name', 'IDE Controller', '--add', 'ide'])
    if codi != 0:
        print "Error creant controladora IDE:", err
        sys.exit(1)

    codi, _, err = executar_comanda(['VBoxManage', 'storageattach', nom_vm,
                                    '--storagectl', 'IDE Controller',
                                    '--port', '0', '--device', '0',
                                    '--type', 'dvddrive', '--medium', 'emptydrive'])
    if codi != 0:
        print "Error assignant drive DVD buit:", err
        sys.exit(1)

def assignar_iso(nom_vm, ruta_iso):
    print "Assignant ISO:", ruta_iso
    codi, _, err = executar_comanda(['VBoxManage', 'storageattach', nom_vm,
                                     '--storagectl', 'IDE Controller',
                                     '--port', '0', '--device', '0',
                                     '--type', 'dvddrive', '--medium', ruta_iso])
    if codi != 0:
        print "Error assignant ISO:", err
        sys.exit(1)

def iniciar_vm(nom_vm):
    print "Iniciant VM:", nom_vm
    codi, _, err = executar_comanda(['VBoxManage', 'startvm', nom_vm, '--type', 'gui'])
    if codi != 0:
        print "Error iniciant VM:", err
        sys.exit(1)

def ajuda():
    print """
Ús: %s <Nom_VM> <Ruta_a_ISO>

Aquest script crea (si no existeix), assigna la ISO i inicia la VM.
""" % sys.argv[0]

def main():
    if len(sys.argv) != 3:
        ajuda()
        sys.exit(1)

    comprovar_vboxmanage()

    nom_vm = sys.argv[1]
    ruta_iso = sys.argv[2]

    if not os.path.isfile(ruta_iso):
        print "Error: La ISO indicada no existeix:", ruta_iso
        sys.exit(1)

    if not existeix_vm(nom_vm):
        crear_vm(nom_vm)
    else:
        print "La VM '%s' ja existeix. Reutilitzant-la." % nom_vm

    assignar_iso(nom_vm, ruta_iso)
    iniciar_vm(nom_vm)

if __name__ == '__main__':
    main()
