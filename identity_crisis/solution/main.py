import lief
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TAMPERED_BINARY = f"{SCRIPT_PATH}/../attachments/identity_crisis.dll"
UNTAMPERED_BINARY = f"{SCRIPT_PATH}/solution.exe"

binary = lief.parse(TAMPERED_BINARY)
print(f"PE characteristics before: {binary.header.characteristics_list}")
binary.header.remove_characteristic(lief.PE.Header.CHARACTERISTICS.DLL)
print(f"PE characteristics after: {binary.header.characteristics_list}")

builder = lief.PE.Builder(binary)
builder.build_resources(True)
builder.build()
builder.write(UNTAMPERED_BINARY)
