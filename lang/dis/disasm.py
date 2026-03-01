import struct

from lang.parser.constants import Constants
from lang.parser.datatype import DataType
from lang.parser.opcodetype import OpCodeType
from exceptions import LanmoDisAsmError

OP_CHECK_CONSTANTS_TABLE = {
    OpCodeType.PUSH
}

OP_KEY_VALUE = {
    OpCodeType.CALL
}

class Disasm:
    def __init__(self, program: bytearray, path: str):
        self.program = program
        self.constants_table = list()
        self.pointer = 0
        self.fp = open(f"{path[:-len('.lmc')]}.dis.lm", 'w')

    def disasmble(self) -> None:
        header = self.__read_bytes(Constants.HEADER_FORMAT, 8)
        if header[1] != Constants.MAJOR_VERSION or header[2] != Constants.MINOR_VERSION:
            raise LanmoDisAsmError(f"mismatching version for disasmbing; supported version: {Constants.MAJOR_VERSION}.{Constants.MINOR_VERSION}")
        self.fp.write(f"// LANMO v{header[1]}.{header[2]}")
        self.__load_constants_table()
        self.__disasmble_functions()
        self.fp.close()

    def __disasmble_functions(self) -> None:
        function_count = self.__read_bytes(Constants.FUNCTION_LOOKUP_COUNT_SIZE_FORMAT, 2)[0]
        for _ in range(function_count):
            name_index = self.__read_bytes(Constants.FUNCTION_NAME_SIZE_FORMAT, 2)[0]
            name = self.constants_table[name_index]
            print(f"[INFO] Disasmbling {name} function")
            args_count = self.__read_bytes(Constants.FUNCTION_ARG_COUNT_FORMAT, 1)[0]
            _ = self.__read_bytes(Constants.FUNCTION_LOCAL_COUNT_FORMAT, 4)[0]
            _ = self.__read_bytes(Constants.FUNCTION_STACK_SIZE_FORMAT, 2)[0]
            self.fp.write(f"\n\n{name} {args_count} {{\n")
            self.__disasmble_op_codes()
            self.fp.write("}")
    
    def __disasmble_op_codes(self) -> None:
        op_code_count = self.__read_bytes(Constants.FUNCTION_CODE_LEN_FORMAT, 4)[0]
        for _ in range(op_code_count):
            op_code, value = self.__read_bytes(Constants.OP_CODE_SIZE_FORMAT, 3)
            op_code = OpCodeType(op_code)
            self.fp.write(f"    {op_code.name}")
            if op_code in OP_CHECK_CONSTANTS_TABLE:
                constant = str(self.constants_table[value])
                self.fp.write(f" {constant}")
            elif op_code in OP_KEY_VALUE:
                self.fp.write(f" {value}")
            self.fp.write("\n")

    def __load_constants_table(self) -> None:
        constants_count = self.__read_bytes(Constants.CONSTANT_LOOKUP_COUNT_SIZE_FORMAT, 2)
        for _ in range(constants_count[0]):
            data_type = self.__read_bytes(Constants.DATA_TYPE_FORMAT_TEMPLATE, 1)[0]
            if data_type == DataType.INTEGER.value:
                size = self.__read_bytes(f"<{Constants.INT_SIZE_FORMAT}", 4)[0]
                number = self.__read_bytes(f"<{Constants.INT_VALUE_FORMAT}", size)[0]
                self.constants_table.append(number)
            elif data_type == DataType.STRING.value:
                size = self.__read_bytes(f"<{Constants.STRING_SIZE_FORMAT}", 4)[0]
                string = self.__read_bytes(f"<{size}s", size)[0]
                self.constants_table.append(f'"{string.decode("utf-8")}"')
            elif data_type == DataType.IDENTIFIER.value:
                size = self.__read_bytes(f"<{Constants.STRING_SIZE_FORMAT}", 4)[0]
                string = self.__read_bytes(f"<{size}s", size)[0]
                self.constants_table.append(string.decode("utf-8"))
            else:
                assert False, "Unhandled DataType: " + str(data_type)
        print(f"[INFO] Unpacked {len(self.constants_table)} Constants")

    def __read_bytes(self, format: str, size: int) -> tuple:
        start_point = self.pointer
        self.pointer += size
        data = struct.unpack(format, self.program[start_point:self.pointer])
        return data
