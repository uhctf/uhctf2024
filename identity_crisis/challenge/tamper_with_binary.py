import lief
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
UNTAMPERED_BINARY = f"{SCRIPT_PATH}/application_code/x64/Release/identity_crisis.exe"
TAMPERED_BINARY = f"{SCRIPT_PATH}/../attachments/identity_crisis.dll"

binary = lief.parse(UNTAMPERED_BINARY)
print(f"PE characteristics before: {binary.header.characteristics_list}")
binary.header.add_characteristic(lief.PE.Header.CHARACTERISTICS.DLL)
print(f"PE characteristics after: {binary.header.characteristics_list}")

builder = lief.PE.Builder(binary)
builder.build_resources(True)
builder.build()
builder.write(TAMPERED_BINARY)
