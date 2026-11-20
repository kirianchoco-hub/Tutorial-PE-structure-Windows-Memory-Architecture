import pefile
import sys
import os

def dump_pe(file_path):
    try:
        # Tải file PE
        pe = pefile.PE(file_path)
    except pefile.PEFormatError as e:
        print(f"Error: Not a valid PE file - {e}")
        return
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return

    # ----- PE Headers ------
    print("----- PE Headers ------")
    print(f"Machine:                    {hex(pe.FILE_HEADER.Machine)}")
    print(f"Number of Sections:         {pe.FILE_HEADER.NumberOfSections}")
    print(f"Number of Symbols:          {pe.FILE_HEADER.NumberOfSymbols}")
    print(f"Characteristics:            {hex(pe.FILE_HEADER.Characteristics)}")
    print("")
    print(f"Image Base:                 0x{pe.OPTIONAL_HEADER.ImageBase:08x}")
    print(f"Image Size:                 0x{pe.OPTIONAL_HEADER.SizeOfImage:08x}")
    print(f"Address of Entry Point:     0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:08x}")
    print(f"Base of Code:               0x{pe.OPTIONAL_HEADER.BaseOfCode:08x}")
    # BaseOfData chỉ có trong PE32, không có trong PE32+
    if hasattr(pe.OPTIONAL_HEADER, 'BaseOfData'):
        print(f"Base of Data:               0x{pe.OPTIONAL_HEADER.BaseOfData:08x}")
    else:
        print(f"Base of Data:               N/A (PE32+)")
    print(f"File Alignment:             0x{pe.OPTIONAL_HEADER.FileAlignment:08x}")
    print(f"Section Alignment:          0x{pe.OPTIONAL_HEADER.SectionAlignment:08x}")
    print("-----------------------")
    print("")

    # ----- PE Sections ------
    print("---- PE Sections --------")
    for section in pe.sections:
        # Tên section thường chứa các byte null, cần decode và loại bỏ
        name = section.Name.decode('utf-8', errors='ignore').rstrip('\x00')
        print(f"    Name:               {name}")
        print(f"    Raw Address:        0x{section.PointerToRawData:08x}")
        print(f"    Raw Size:           0x{section.SizeOfRawData:08x}")
        print(f"    Virtual Address:    0x{section.VirtualAddress:08x}")
        print(f"    Virtual Size:       0x{section.Misc_VirtualSize:08x}")
        print("")
    print("-------------------------")

    # ----- PE Imports ------
    print("------ PE Imports -------")
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            print(f"  Library: {entry.dll.decode('utf-8', errors='ignore')}")
            for imp in entry.imports:
                # Tên hàm có thể là None nếu import bằng ordinal
                func_name = imp.name.decode('utf-8', errors='ignore') if imp.name else f"Ordinal {imp.ordinal}"
                print(f"\t\t{func_name}")
            print("")
    else:
        print("  No imports found.")
    print("-------------------------")

    # ----- PE Exports ------
    print("------ PE Exports -------")
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            name = exp.name.decode('utf-8', errors='ignore') if exp.name else None
            print(f"\tORD: {exp.ordinal} RVA: 0x{exp.address:08x} NAME: {name}")
    else:
        print("  No exports found.")
    print("-------------------------")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"{sys.argv[0]} [PE]")
        print("")
        sys.exit(1)

    dump_pe(sys.argv[1])
