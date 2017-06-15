import os
import larissa
from larissa.Loader.ELF import ELF

# Where are we
here = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(here,"..","bin")

def test_loader_main_64_simple_nopic_nopie():
    proj = larissa.Project(os.path.join(bin_path,"amd64","simple_nopic_nopie"))
    state = proj.factory.entry_state()
    main = proj.loader.main_bin.symbols['main']
    b = state.memory[main.addr:main.addr+32]
    assert str(b) == 'UH\x89\xe5H\x83\xec \x89}\xfcH\x89u\xf0H\x89U\xe8\xe8\xd2\xff\xff\xff\xb8\x00\x00\x00\x00\xc9\xc3\x0f'

def test_loader_main_32_simple_nopic_nopie():
    proj = larissa.Project(os.path.join(bin_path,"ia32","simple_nopic_nopie"))
    state = proj.factory.entry_state()
    main = proj.loader.main_bin.symbols['main']
    b = state.memory[main.addr:main.addr+32]
    assert str(b) == '\x8dL$\x04\x83\xe4\xf0\xffq\xfcU\x89\xe5Q\x83\xec\x04\xe8\xd1\xff\xff\xff\xb8\x00\x00\x00\x00\x83\xc4\x04Y]'
    
def test_loader_basic_page_permissions():
    proj = larissa.Project(os.path.join(bin_path,"ia32","simple_nopic_nopie"))
    state = proj.factory.entry_state()
    main = proj.loader.main_bin.symbols['main']
    assert state.memory[main.addr].page.mapped == True
    assert state.memory[main.addr].page.read == True
    assert state.memory[main.addr].page.execute == True
    assert state.memory[main.addr].page.write == False

    bss = proj.loader.main_bin.symbols['.bss']
    assert state.memory[bss.addr].page.mapped == True
    assert state.memory[bss.addr].page.read == True
    assert state.memory[bss.addr].page.write == True
    assert state.memory[bss.addr].page.execute == False

def test_loader_triton_elf():
    for arch in ["amd64","ia32"]:
        for binary in ["simple_pic_pie","simple_nopic_nopie"]:
            print("Loading {0} {1}".format(arch, binary))
            proj = larissa.Project(os.path.join(bin_path,arch,binary))
            
            # Main bin
            proj.loader.main_bin.triton_elf.getSize()

            # Shared libs
            for lib in proj.loader.shared_objects.values():
                lib.triton_elf.getSize()
